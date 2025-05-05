# -*- coding: utf-8 -*-
# main.py
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 加入 utils 模組路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from indicators import *
from binance_api import fetch_binance_kline

# ====== 畫 Feature Importance 函數 ======
def plot_feature_importance(model, feature_names, symbol):
    importance = model.feature_importances_
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values(by='importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance, palette="viridis")
    plt.title(f'{symbol} - Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.savefig(f'logs/{symbol}_feature_importance.png')
    plt.close()

# ====== 設定 ======
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
model_dir = "./saved_models"
os.makedirs(model_dir, exist_ok=True)
os.makedirs("logs", exist_ok=True)

for symbol in symbols:
    print(f"\n===== 處理 {symbol} 資料 =====")

    # 抓資料
    df = fetch_binance_kline(symbol, interval="1h")

    # 計算技術指標
    df = calculate_rsi(df)
    df = calculate_macd(df)
    df = calculate_sma(df, 5)
    df = calculate_sma(df, 20)
    df = calculate_ema(df, 5)
    df = calculate_ema(df, 20)
    df = calculate_bollinger_bands(df)
    df = calculate_atr(df)
    df = calculate_adx(df)
    df = calculate_momentum(df)

    # 斐波那契
    lookback = 24
    high = df["high"].iloc[-lookback:].max()
    low = df["low"].iloc[-lookback:].min()
    fib_levels = calculate_fibonacci_levels(high, low)
    print("\n斐波那契回撤點位:")
    for level, price in fib_levels.items():
        print(f"{level}: {price:.2f}")

    # 整理訓練資料
    df.dropna(inplace=True)
    df["future_close"] = df["close"].shift(-1)
    df["price_change_pct"] = df["close"].pct_change() * 100
    df["volume_change_pct"] = df["volume"].pct_change() * 100
    df.dropna(inplace=True)

    features = [
        "close", "RSI", "MACD", "Signal",
        "SMA_5", "SMA_20", "EMA_5", "EMA_20",
        "BB_upper", "BB_middle", "BB_lower", "BB_width",
        "ATR", "ADX", "Momentum",
        "price_change_pct", "volume_change_pct"
    ]

    X = df[features]
    y = (df["future_close"] > df["close"]).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # 建 Random Forest 模型
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 評估模型
    y_pred = model.predict(X_test)
    print(f"\n{symbol} 模型分類表現:")
    print(classification_report(y_test, y_pred))
    print("\n混淆矩陣:")
    print(confusion_matrix(y_test, y_pred))

    # 儲存模型
    model_path = os.path.join(model_dir, f"{symbol}_model.pkl")
    joblib.dump(model, model_path)
    print(f"模型已儲存至: {model_path}")

    # 畫出 Feature Importance
    plot_feature_importance(model, X_train.columns, symbol)
    print(f"特徵重要性圖已儲存至: logs/{symbol}_feature_importance.png")

print("\n✅ 所有模型已完成訓練與儲存，Feature Importance 也已完成。")

