# -*- coding: utf-8 -*-
# auto_scheduler.py - 自動排程每日預測

import schedule
import time
import os

def run_prediction():
    print("⏳ 執行預測任務...")
    os.system("python C:\\Users\\Yak\\Desktop\\Crypto_Yak_System_V1.1\\src\\auto_predict.py")

# 每天兩次
schedule.every().day.at("08:00").do(run_prediction)
schedule.every().day.at("20:00").do(run_prediction)

print("✅ Crypto_Yak 自動預測排程器啟動中...")

while True:
    schedule.run_pending()
    time.sleep(60)
