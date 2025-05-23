
# 🐮 Crypto_Yak_System_V1.0.1

> 機器學習加密貨幣預測系統，支援 RSI、MACD、Bollinger Band 指標、三分類預測、自選幣種與 Telegram 中文通知。

## 📦 功能特色

- ✅ 自選幣種 + 自選 K 線區間
- ✅ 特徵選擇（RSI、MACD、BB）自由控制
- ✅ 三分類模型（上漲=1、下跌=-1、震盪=0）
- ✅ 自動畫圖推播至 Telegram（含中文提示）
- ✅ GUI Yak 設定助手快速操作
- ✅ 可選擇模型訓練與預測流程

## 🖱 快速使用

### 執行訓練
```
點兩下 train.bat
```

### 執行預測（使用模型並自動推播訊息）
```
點兩下 predict.bat
```

### 執行圖形介面 Yak 設定助手
```
點兩下 yak_gui.bat
```

## 🧠 預測標籤說明

- 預測為 `1` ➜ 預期下一根 K 棒上漲
- 預測為 `-1` ➜ 預期下一根 K 棒下跌
- 預測為 `0` ➜ 預期價格震盪不明

## 📬 Telegram 中文通知

- 當漲跌超過 ±5% 會自動附加提醒訊息：
  - 🔥 注意飆漲！
  - 🔴 注意下跌！

## 📁 模型儲存路徑

模型會自動儲存在 `/models/{symbol}_{interval}_model.pkl` 中。
