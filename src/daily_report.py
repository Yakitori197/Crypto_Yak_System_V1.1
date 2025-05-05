# -*- coding: utf-8 -*-
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from utils.telegram_notify import send_telegram_message

load_dotenv()
log_dir = Path("logs")
today = datetime.now().strftime("%Y%m%d")
log_file = log_dir / f"log_{today}.txt"
error_file = log_dir / f"error_{today}.txt"

report_lines = []
if log_file.exists():
    report_lines.append(f"📈 預測紀錄（{today}）\n")
    with open(log_file, encoding="utf-8") as f:
        report_lines.extend(f.readlines())
else:
    report_lines.append("⚠️ 今日無預測紀錄\n")

if error_file.exists():
    report_lines.append("\n❌ 錯誤紀錄：\n")
    with open(error_file, encoding="utf-8") as f:
        report_lines.extend(f.readlines())

msg = "".join(report_lines).strip()
if len(msg) > 3900:
    msg = msg[:3900] + "\n...（已截斷）"

send_telegram_message(msg)