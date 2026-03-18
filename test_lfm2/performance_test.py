import requests
import time
import csv
import subprocess
import threading
import os
from datetime import datetime

MODEL_NAME = "lfm2"
TEST_STEPS = [128, 512, 1024, 2048]
PROMPT = "請詳細解釋量子力學與廣義相對論的衝突點，並嘗試給出三種可能的統一理論。請盡量擴充內容以達到字數要求。"
URL = "http://localhost:11434/api/generate"
OUTPUT_FILE = "ollama_tps_summary.csv"
MONITOR_FILE = "ollama_monitor.csv"

monitor_data = []
stop_monitoring = False

def monitor_system():
    """背景監控 CPU 和 RAM"""
    global monitor_data, stop_monitoring
    
    with open(MONITOR_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Time', 'CPU_Percent', 'RAM_GB'])
        writer.writeheader()
        
        start_time = time.time()
        while not stop_monitoring:
            # 抓取 ollama 程序的資源使用
            result = subprocess.run(
                "ps -eo pcpu,rss,comm | grep -i 'ollama' | grep -v 'grep' | awk '{cpu+=$1; mem+=$2} END {print cpu \",\" mem/1024/1024}'",
                shell=True,
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                parts = result.stdout.strip().split(',')
                if len(parts) == 2:
                    try:
                        elapsed = round(time.time() - start_time, 2)
                        row = {
                            'Time': elapsed,
                            'CPU_Percent': float(parts[0]),
                            'RAM_GB': float(parts[1])
                        }
                        monitor_data.append(row)
                        writer.writerow(row)
                        f.flush()
                    except ValueError:
                        pass
            
            time.sleep(1)

# 啟動背景監控
print(f"🚀 開始整合效能測試 模型: {MODEL_NAME}")
monitor_thread = threading.Thread(target=monitor_system, daemon=True)
monitor_thread.start()

# 執行壓力測試
stress_results = []
time.sleep(1)  # 等待監控啟動

for tokens in TEST_STEPS:
    print(f"測試長度: {tokens} tokens...")
    start_time = time.time()
    
    try:
        res = requests.post(URL, json={
            "model": MODEL_NAME,
            "prompt": PROMPT,
            "stream": False,
            "options": {"num_predict": tokens}
        })
        
        if res.status_code == 200:
            data = res.json()
            eval_duration_sec = data.get("eval_duration", 1) / 1e9
            tps = data.get("eval_count", 0) / eval_duration_sec if eval_duration_sec > 0 else 0
            
            stress_results.append({
                "target_tokens": tokens,
                "actual_tokens": data.get("eval_count"),
                "duration_sec": round(time.time() - start_time, 2),
                "tps": round(tps, 2)
            })
            print(f"✅ 完成！TPS: {round(tps, 2)}")
        else:
            print(f"❌ 錯誤: {res.status_code}")
    
    except Exception as e:
        print(f"❌ 請求失敗: {e}")

# 停止監控
stop_monitoring = True
monitor_thread.join(timeout=2)

# 儲存壓力測試結果
if stress_results:
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=stress_results[0].keys())
        writer.writeheader()
        writer.writerows(stress_results)
    print(f"\n📊 壓力測試結果已儲存至 {OUTPUT_FILE}")

print(f"📊 系統監控資料已儲存至 {MONITOR_FILE}")
