# -*- coding: utf-8 -*-
# train.py - 訓練模型並儲存 + 儲存訓練圖表

import os
import sys
import joblib
import traceback
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from utils.binance_api import fetch_binance_kline
from utils.indicators import get_technical_indicators
from utils.telegram_notify import send_telegram_message

def label_data(df):
    df['target'] = 0
    df.loc[df['close'].shift(-1) > df['close'] * 1.01, 'target'] = 1
    df.loc[df['close'].shift(-1) < df['close'] * 0.99, 'target'] = -1
    df.dropna(inplace=True)
    return df

def save_training_chart(df, symbol, interval):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 4))

    df_plot = df.copy().tail(100)
    df_plot["timestamp"] = pd.to_datetime(df_plot["timestamp"], unit='ms')
    ax.plot(df_plot["timestamp"], df_plot["close"], color='cyan', label='Close')
    ax.set_title(f"{symbol}-{interval} 訓練資料（最後100根）")
    ax.set_xlabel("時間")
    ax.set_ylabel("價格")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 儲存至 train_img 資料夾
    img_dir = os.path.join(os.path.dirname(__file__), "..", "train_img")
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, f"{symbol}_{interval}_train.png")
    plt.savefig(img_path)
    plt.close()
    print(f"📊 訓練圖已儲存：{img_path}")

def train(symbol, interval):
    try:
        print(f"🚀 開始訓練模型：{symbol}-{interval}")
        df = fetch_binance_kline(symbol, interval=interval, limit=500)

        if df is None or df.empty or len(df) < 100:
            raise ValueError("資料不足，無法訓練")

        df, feature_cols = get_technical_indicators(df)
        df = label_data(df)
        df.dropna(subset=feature_cols + ['target'], inplace=True)

        X = df[feature_cols]
        y = df['target']
        if len(X) < 50:
            raise ValueError("樣本數過少")

        # 畫圖（儲存圖表）
        save_training_chart(df, symbol, interval)

        # 模型訓練
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)

        model_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f"{symbol}_{interval}_model.pkl")
        joblib.dump({"model": model, "features": feature_cols}, model_path)

        print(f"✅ 模型已儲存至：{model_path}")
        send_telegram_message(f"✅ 模型訓練完成：{symbol}-{interval}，準確率：{acc:.2%}")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        traceback.print_exc()
        send_telegram_message(f"❌ 訓練失敗：{symbol}-{interval}\n錯誤：{e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("⚠️ 用法：python train.py BTCUSDT 15m")
        sys.exit(1)
    train(sys.argv[1].upper(), sys.argv[2])
