#!/bin/bash

# 設定輸出的檔名（包含時間戳記）
OUTPUT_FILE="ollama_test_$(date +%Y%m%d_%H%M%S).csv"

# 寫入 CSV 的標題列
echo "Time,CPU_Percent,RAM_GB" > "$OUTPUT_FILE"

echo "開始監控 Ollama... (請在另一個視窗開始 run 模型)"
echo "測試結束後，請按 Ctrl+C 停止監控並產出報告。"

# 開始循環監控
while true; do
    # 抓取所有 ollama 相關程序的數據並加總
    # ps -eo pcpu,rss,comm 抓取 CPU%, 記憶體(KB), 指令名稱
    DATA=$(ps -eo pcpu,rss,comm | grep -i "ollama" | grep -v "grep" | awk '{cpu+=$1; mem+=$2} END {print cpu "," mem/1024/1024}')
    
    # 取得目前時間
    CURRENT_TIME=$(date +%H:%M:%S)
    
    # 如果有抓到數據就寫入檔案
    if [[ ! -z "$DATA" && "$DATA" != "," ]]; then
        echo "$CURRENT_TIME,$DATA" >> "$OUTPUT_FILE"
        # 同時顯示在畫面上讓你確認正在跑
        echo "[$CURRENT_TIME] CPU: $(echo $DATA | cut -d',' -f1)% | RAM: $(echo $DATA | cut -d',' -f2) GB"
    fi
    
    sleep 1
done