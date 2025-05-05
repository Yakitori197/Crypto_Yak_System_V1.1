# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_macd(df, fast=12, slow=26, signal=9):
    df['EMA_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    return df

def calculate_bollinger_bands(df, window=20):
    df['BB_middle'] = df['close'].rolling(window=window).mean()
    df['BB_std'] = df['close'].rolling(window=window).std()
    df['BB_upper'] = df['BB_middle'] + 2 * df['BB_std']
    df['BB_lower'] = df['BB_middle'] - 2 * df['BB_std']
    df['BB_width'] = df['BB_upper'] - df['BB_lower']
    return df

def get_technical_indicators(df):
    use_rsi = os.getenv("USE_RSI", "1") == "1"
    use_macd = os.getenv("USE_MACD", "1") == "1"
    use_bb = os.getenv("USE_BB", "1") == "1"

    features = []

    if use_rsi:
        df = calculate_rsi(df)
        features.append('RSI')

    if use_macd:
        df = calculate_macd(df)
        features.extend(['MACD', 'MACD_Signal'])

    if use_bb:
        df = calculate_bollinger_bands(df)
        features.extend(['BB_upper', 'BB_middle', 'BB_lower'])

    df.dropna(inplace=True)
    return df, features
