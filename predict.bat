
@echo off
cd /d %~dp0
echo 啟動 Crypto Yak 預測功能中...
python predict_future.py
pause
