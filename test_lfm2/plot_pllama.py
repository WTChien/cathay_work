import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# 1. 自動抓取最新的一份 CSV 檔案
# list_of_files = glob.glob('ollama_test_*.csv')
list_of_files = glob.glob('ollama_tps_summary.csv')
latest_file = max(list_of_files, key=os.path.getmtime)
print(f"正在分析檔案: {latest_file}")

# 2. 讀取數據
df = pd.read_csv(latest_file)

# 3. 繪圖設定
fig, ax1 = plt.subplots(figsize=(12, 6))

# 繪製 CPU 曲線 (左軸)
color = 'tab:blue'
ax1.set_xlabel('Time (Seconds)')
ax1.set_ylabel('CPU Usage (%)', color=color)
ax1.plot(df.index, df['CPU_Percent'], color=color, linewidth=2, label='CPU %')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.6)

# 繪製 RAM 曲線 (右軸)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('RAM Usage (GB)', color=color)
ax2.plot(df.index, df['RAM_GB'], color=color, linewidth=2, linestyle='--', label='RAM GB')
ax2.tick_params(axis='y', labelcolor=color)

# 4. 裝飾圖表
plt.title(f'Ollama Performance Analysis\nSource: {latest_file}')
fig.tight_layout()
plt.show()