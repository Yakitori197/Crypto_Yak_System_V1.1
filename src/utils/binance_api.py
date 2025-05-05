# -*- coding: utf-8 -*-

import pandas as pd
import requests

def fetch_binance_kline(symbol, interval='15m', limit=100):
    print(f"🔄 從 Binance 抓取 K 線資料: {symbol} {interval}")
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("❌ 無法取得 Binance 資料")
        return pd.DataFrame()

    data = response.json()
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms")

    print("📊 Binance 回傳資料筆數：", len(df))
    print(df.head())
    return df[["timestamp", "open", "high", "low", "close", "volume"]]
