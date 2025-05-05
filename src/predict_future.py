# -*- coding: utf-8 -*-
import os
import sys
import joblib
import traceback
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from utils.binance_api import fetch_binance_kline
from utils.indicators import get_technical_indicators
from utils.telegram_notify import send_telegram_message, send_telegram_image

# 清理 5 天前的圖片
def cleanup_old_images(days=5):
    img_dir = os.path.join(os.path.dirname(__file__), "..", "predict", "img")
    if not os.path.exists(img_dir):
        return
    cutoff_time = datetime.now() - timedelta(days=days)
    for filename in os.listdir(img_dir):
        file_path = os.path.join(img_dir, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_time:
                os.remove(file_path)
                print(f"🧹 已刪除舊圖表：{filename}")

def plot_prediction_chart(df, symbol, interval, pred_label, confidence):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 5))
    df_plot = df.copy().tail(100)

    if "timestamp" in df_plot.columns:
        df_plot["timestamp"] = pd.to_datetime(df_plot["timestamp"], unit='ms')
    elif "time" in df_plot.columns:
        df_plot["timestamp"] = pd.to_datetime(df_plot["time"], unit='ms')
    else:
        df_plot["timestamp"] = pd.to_datetime(df_plot.index, unit='ms')

    ax.plot(df_plot["timestamp"], df_plot["close"], label="Close", color='cyan')
    ax.set_title(f"{symbol}-{interval}\n{pred_label}（信心 {confidence:.2%}）", fontsize=14)
    ax.set_xlabel("時間")
    ax.set_ylabel("價格")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    img_dir = os.path.join(os.path.dirname(__file__), "..", "predict", "img")
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, f"{symbol}_{interval}.png")
    plt.savefig(img_path)
    plt.close()
    return img_path

def predict(symbol, interval, return_result=False):
    try:
        print(f"🔮 開始預測：{symbol}-{interval}")

        # 清理舊圖表
        cleanup_old_images()

        raw_df = fetch_binance_kline(symbol, interval=interval, limit=100)
        if raw_df is None or raw_df.empty:
            raise ValueError("❌ 無法取得資料")

        df_with_indicators, _ = get_technical_indicators(raw_df)

        model_path = os.path.join(os.path.dirname(__file__), "models", f"{symbol}_{interval}_model.pkl")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ 找不到模型：{symbol}_{interval}_model.pkl")

        model_data = joblib.load(model_path)
        model = model_data["model"]
        features = model_data["features"]

        df = df_with_indicators[features].dropna()
        X = df.tail(1)

        pred = model.predict(X)[0]
        proba_array = model.predict_proba(X)[0]
        proba_dict = {label: prob for label, prob in zip(model.classes_, proba_array)}

        label_map = {-1: "🔴 注意下跌", 0: "⚠️ 盤整", 1: "🟢 注意上漲"}
        pred_label = label_map.get(pred, "❓ 未知")
        confidence = proba_dict.get(pred, 0)

        message = (
            f"{pred_label}\n"
            f"幣種：{symbol}\n"
            f"週期：{interval}\n"
            f"預測機率：{confidence:.2%}"
        )
        print(message)
        send_telegram_message(message)

        chart_path = plot_prediction_chart(raw_df, symbol, interval, pred_label, confidence)
        send_telegram_image(chart_path)

        if return_result:
            return pred, proba_dict

    except Exception as e:
        error_msg = f"❌ 預測錯誤：{symbol}-{interval}\n{e}"
        print(error_msg)
        traceback.print_exc()
        send_telegram_message(error_msg)
        if return_result:
            return None, None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("⚠️ 用法：python predict_future.py BTCUSDT 15m")
        sys.exit(1)
    predict(sys.argv[1].upper(), sys.argv[2])
