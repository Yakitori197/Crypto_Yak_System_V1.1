@echo off
chcp 65001 >nul
cd /d "%~dp0src"
echo 🔮 開始自動預測...
python auto_predict.py
echo ✅ 預測完成
pause
