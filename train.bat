
@echo off
cd /d %~dp0
echo 啟動 Crypto Yak 模型訓練中...
python train.py
pause
