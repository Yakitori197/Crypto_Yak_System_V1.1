# -*- coding: utf-8 -*-

import os
import time
import subprocess

# 可自行擴充的幣種與週期清單
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
intervals = ["15m", "1h", "4h"]

print("🚀 開始批次訓練模型...")

for symbol in symbols:
    for interval in intervals:
        print(f"\n🛠️ 訓練模型：{symbol} - {interval}")
        try:
            result = subprocess.run(
                ["python", "train.py", symbol, interval],
                cwd=os.path.dirname(__file__),
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print("⚠️ 錯誤訊息：", result.stderr)
            time.sleep(1)
        except Exception as e:
            print(f"❌ 執行失敗：{symbol}-{interval}：{e}")

print("\n✅ 批次訓練完成！")
