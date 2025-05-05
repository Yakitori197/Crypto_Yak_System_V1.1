@echo off
chcp 65001 >nul
cd /d "%~dp0src"
python yak_gui.py
pause
