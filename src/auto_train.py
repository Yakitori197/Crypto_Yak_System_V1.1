# -*- coding: utf-8 -*-
# auto_train.py - 批次訓練多幣種與多週期模型，並清除過期圖表

import os
import traceback
from datetime import datetime, timedelta
from train import train
from utils.telegram_notify import send_telegram_message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL_FILE = os.path.join(os.path.dirname(BASE_DIR), "symbols.txt")
TRAIN_IMG_DIR = os.path.join(BASE_DIR, "..", "train_img")
INTERVALS = ["15m", "1h", "4h", "1d"]

def load_symbols():
    if not os.path.exists(SYMBOL_FILE):
        print("❌ 找不到 symbols.txt")
        return []
    with open(SYMBOL_FILE, "r") as f:
        symbols = [line.strip().upper() for line in f if line.strip()]
    return symbols

def cleanup_old_images(folder_path, days=5):
    if not os.path.exists(folder_path):
        return
    cutoff_time = datetime.now() - timedelta(days=days)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_time:
                os.remove(file_path)
                print(f"🧹 已刪除舊訓練圖：{filename}")

def auto_train_all():
    # 清理舊圖
    cleanup_old_images(TRAIN_IMG_DIR)

    symbols = load_symbols()
    if not symbols:
        print("⚠️ 沒有任何幣種可供訓練")
        return

    summary = []
    for symbol in symbols:
        for interval in INTERVALS:
            try:
                train(symbol, interval)
                summary.append(f"✅ {symbol}-{interval} 模型完成")
            except Exception as e:
                error_msg = f"❌ {symbol}-{interval} 失敗: {e}"
                print(error_msg)
                traceback.print_exc()
                summary.append(error_msg)

    report = "\n".join(summary)
    send_telegram_message(f"📊 自動訓練報告：\n{report}")

if __name__ == "__main__":
    auto_train_all()
