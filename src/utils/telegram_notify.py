# -*- coding: utf-8 -*-

import os
import requests
from dotenv import load_dotenv

# 載入 .env 設定
load_dotenv()

# 從 .env 讀取 Telegram 機器人資訊
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_CHAT_ID = os.getenv("TELEGRAM_USER_CHAT_ID")
GROUP_CHAT_ID = os.getenv("TELEGRAM_GROUP_CHAT_ID")

# 發送純文字訊息（支援個人與群組）
def send_telegram_message(message):
    for chat_id in [USER_CHAT_ID, GROUP_CHAT_ID]:
        if chat_id:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": chat_id, "text": message}
            try:
                response = requests.post(url, data=data)
                response.raise_for_status()
                print(f"✅ 已發送文字訊息至 chat_id={chat_id}")
            except Exception as e:
                print(f"❌ 發送文字訊息至 chat_id={chat_id} 失敗: {e}")

# 發送圖片訊息（支援個人與群組）
def send_telegram_image(image_path):
    for chat_id in [USER_CHAT_ID, GROUP_CHAT_ID]:
        if chat_id:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            try:
                with open(image_path, "rb") as photo:
                    data = {"chat_id": chat_id}
                    files = {"photo": photo}
                    response = requests.post(url, data=data, files=files)
                    response.raise_for_status()
                    print(f"✅ 已發送圖片至 chat_id={chat_id}")
            except Exception as e:
                print(f"❌ 發送圖片至 chat_id={chat_id} 失敗: {e}")

# 圖＋文字一起推播
def send_telegram_message_with_plot(message, image_path):
    send_telegram_message(message)
    send_telegram_image(image_path)

# 測試用
if __name__ == "__main__":
    send_telegram_message("🧪 測試文字訊息：Crypto_Yak_System")
    send_telegram_image("predict_BTCUSDT_15m.png")  # ⚠️ 確保此圖檔存在
