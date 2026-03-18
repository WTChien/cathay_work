import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# 1. 自動抓取最新的一份 CSV 檔案
monitor_files = glob.glob('ollama_monitor.csv')
summary_files = glob.glob('ollama_tps_summary.csv')

if monitor_files:
    latest_file = max(monitor_files, key=os.path.getmtime)
    print(f"正在分析監控檔案: {latest_file}")
    df = pd.read_csv(latest_file)
    
    # 2. 繪圖設定
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 繪製 CPU 曲線 (左軸)
    color = 'tab:blue'
    ax1.set_xlabel('Time (Seconds)')
    ax1.set_ylabel('CPU Usage (%)', color=color)
    ax1.plot(df['Time'], df['CPU_Percent'], color=color, linewidth=2, label='CPU %')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 繪製 RAM 曲線 (右軸)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('RAM Usage (GB)', color=color)
    ax2.plot(df['Time'], df['RAM_GB'], color=color, linewidth=2, linestyle='--', label='RAM GB')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # 3. 裝飾圖表
    plt.title(f'Ollama Performance Monitoring\nSource: {latest_file}')

elif summary_files:
    latest_file = max(summary_files, key=os.path.getmtime)
    print(f"正在分析摘要檔案: {latest_file}")
    df = pd.read_csv(latest_file)
    
    # 2. 繪圖設定
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 繪製 TPS 曲線 (左軸)
    color = 'tab:blue'
    ax1.set_xlabel('Test Iteration')
    ax1.set_ylabel('TPS (Tokens/Second)', color=color)
    ax1.plot(df.index, df['tps'], color=color, marker='o', linewidth=2, label='TPS')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 繪製 Duration 曲線 (右軸)
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Duration (Seconds)', color=color)
    ax2.plot(df.index, df['duration_sec'], color=color, marker='s', linewidth=2, linestyle='--', label='Duration')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # 3. 裝飾圖表
    plt.title(f'Ollama TPS Analysis\nSource: {latest_file}')

else:
    print("❌ 找不到 CSV 檔案")
    exit(1)
fig.tight_layout()
plt.show()