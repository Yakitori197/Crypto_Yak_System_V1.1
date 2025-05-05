@echo off
chcp 65001 >nul
cd /d "%~dp0src"
echo 🔁 開始執行模型訓練與清理...
python auto_train.py
python auto_cleanup.py
echo ✅ 執行完畢
pause
