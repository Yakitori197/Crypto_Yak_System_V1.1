# -*- coding: utf-8 -*-
# auto_predict.py - 批次預測多幣種並推播圖文
import os
from predict_future import predict
from utils.telegram_notify import send_telegram_message_with_plot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL_FILE = os.path.join(os.path.dirname(BASE_DIR), "symbols.txt")
IMG_DIR = os.path.join(BASE_DIR, "..", "predict", "img")

def load_symbols():
    if not os.path.exists(SYMBOL_FILE):
        print("❌ 找不到 symbols.txt")
        return []
    with open(SYMBOL_FILE, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]

def auto_predict_all(interval="15m"):
    symbols = load_symbols()
    if not symbols:
        print("⚠️ 沒有任何幣種可預測")
        return

    summary = []
    for symbol in symbols:
        try:
            # 執行預測（內部會儲存圖）
            predict(symbol, interval)

            # 圖表路徑
            img_path = os.path.join(IMG_DIR, f"{symbol}_{interval}.png")

            # 發送圖＋訊息
            message = f"📊 {symbol} {interval} 自動預測完成"
            if os.path.exists(img_path):
                send_telegram_message_with_plot(message, img_path)
            else:
                send_telegram_message_with_plot(message, None)

            summary.append(f"✅ {symbol} 預測完成")
        except Exception as e:
            summary.append(f"❌ {symbol} 預測失敗: {e}")

    # 最後彙總文字推播
    from utils.telegram_notify import send_telegram_message
    send_telegram_message("📡 預測總結報告：\n" + "\n".join(summary))

if __name__ == "__main__":
    auto_predict_all("15m")
