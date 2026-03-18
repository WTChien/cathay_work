import requests, time, csv

MODEL_NAME = "lfm2"
TEST_STEPS = [128, 512, 1024, 2048]
PROMPT = "請詳細解釋量子力學與廣義相對論的衝突點，並嘗試給出三種可能的統一理論。請盡量擴充內容以達到字數要求。"
URL = "http://localhost:11434/api/generate"

results = []
print(f"🚀 開始階梯式測試 模型: {MODEL_NAME}")

for tokens in TEST_STEPS:
    print(f"測試長度: {tokens} tokens...")
    start_time = time.time()
    res = requests.post(URL, json={"model": MODEL_NAME, "prompt": PROMPT, "stream": False, "options": {"num_predict": tokens}})
    
    if res.status_code == 200:
        data = res.json()
        tps = data.get("eval_count", 0) / (data.get("eval_duration", 1) / 1e9)
        results.append({
            "target_tokens": tokens,
            "actual_tokens": data.get("eval_count"),
            "duration_sec": round(time.time() - start_time, 2),
            "tps": round(tps, 2)
        })
        print(f"✅ 完成！TPS: {round(tps, 2)}")

with open('ollama_tps_summary.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
print("📊 TPS 摘要已儲存至 ollama_tps_summary.csv")