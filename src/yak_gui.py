# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from predict_future import predict
from utils.telegram_notify import send_telegram_message, send_telegram_image# ✅ 同步引入

def save_env_settings():
    with open(".env", "w") as f:
        f.write(f"USE_RSI={'1' if var_rsi.get() else '0'}\n")
        f.write(f"USE_MACD={'1' if var_macd.get() else '0'}\n")
        f.write(f"USE_BB={'1' if var_bb.get() else '0'}\n")
    messagebox.showinfo("設定儲存", "✅ 技術指標設定已更新")

def run_prediction():
    save_env_settings()
    symbol = entry_symbol.get().upper()
    interval = combo_interval.get()
    try:
        pred_label, proba_dict = predict(symbol, interval, return_result=True)
        if pred_label is None or proba_dict is None:
            messagebox.showerror("錯誤", "❌ 預測失敗，請確認模型是否存在或資料是否可用。")
            return

        label_map = {-1: "🔴 注意下跌", 0: "⚠️ 盤整", 1: "🟢 注意上漲"}
        result_str = f"📈 {symbol} 預測（{interval}）\n"
        result_str += f"預測結果：{label_map.get(pred_label, pred_label)}\n\n信心比例：\n"

        sorted_proba = sorted(proba_dict.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_proba:
            result_str += f"{label_map.get(k, k)} → {v:.2%}\n"

        messagebox.showinfo(f"{symbol} 預測", result_str)
        send_telegram_message(result_str)

        # ✅ 傳送預測圖像（路徑由 predict() 生成，例如 charts/BTCUSDT_1h.png）
        image_path = f"charts/{symbol}_{interval}.png"
        if os.path.exists(image_path):
            send_telegram_image(image_path)

    except Exception as e:
        messagebox.showerror("錯誤", f"預測失敗：\n{e}")

def run_batch_prediction():
    save_env_settings()
    success_count = 0
    fail_count = 0
    models_folder = "models"
    model_files = [f for f in os.listdir(models_folder) if f.endswith("_model.pkl")]

    if not model_files:
        messagebox.showwarning("無模型", "❗ models 資料夾中找不到任何模型檔案。")
        return

    summary = "📊 批次預測摘要：\n"
    for model_file in model_files:
        try:
            parts = model_file.replace("_model.pkl", "").split("_")
            if len(parts) < 2:
                continue
            symbol = parts[0]
            interval = parts[1]
            pred_label, _ = predict(symbol, interval, return_result=True)
            if pred_label is not None:
                success_count += 1
                summary += f"✅ {symbol}-{interval}：{pred_label}\n"
                # 傳送每張圖
                image_path = f"charts/{symbol}_{interval}.png"
                if os.path.exists(image_path):
                    send_telegram_image(image_path)
            else:
                fail_count += 1
                summary += f"❌ {symbol}-{interval}：預測失敗\n"
        except Exception:
            fail_count += 1
            summary += f"❌ {model_file}：例外錯誤\n"
            continue

    summary += f"\n總結：成功 {success_count} 筆，失敗 {fail_count} 筆"
    messagebox.showinfo("批次預測完成", summary)
    send_telegram_message(summary)

# 建立 GUI
load_dotenv()
root = tk.Tk()
root.title("Yak 設定助手 - Crypto_Yak_System")
root.configure(bg="#1e1e1e")
root.geometry("420x480")

tk.Label(root, text="輸入幣種（如 BTCUSDT）", bg="#1e1e1e", fg="white").pack()
entry_symbol = tk.Entry(root)
entry_symbol.insert(0, "BTCUSDT")
entry_symbol.pack()

tk.Label(root, text="選擇 K 線間隔", bg="#1e1e1e", fg="white").pack()
combo_interval = tk.StringVar()
combo_menu = tk.OptionMenu(root, combo_interval, "15m", "1h", "4h")
combo_interval.set("1h")
combo_menu.pack()

tk.Label(root, text="選擇技術指標：", bg="#1e1e1e", fg="white").pack()
var_rsi = tk.BooleanVar(value=os.getenv("USE_RSI", "1") == "1")
tk.Checkbutton(root, text="✅ RSI", variable=var_rsi, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack()
var_macd = tk.BooleanVar(value=os.getenv("USE_MACD", "1") == "1")
tk.Checkbutton(root, text="✅ MACD", variable=var_macd, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack()
var_bb = tk.BooleanVar(value=os.getenv("USE_BB", "1") == "1")
tk.Checkbutton(root, text="✅ Bollinger Band", variable=var_bb, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack()

tk.Label(root, text="", bg="#1e1e1e").pack()
tk.Button(root, text="💾 儲存設定", command=save_env_settings).pack(pady=5)
tk.Button(root, text="🔍 單一幣種預測", command=run_prediction).pack(pady=5)
tk.Button(root, text="📊 批次模型預測", command=run_batch_prediction).pack(pady=5)

tk.Label(root, text="© Crypto Yak System V1.1", bg="#1e1e1e", fg="#888888").pack(side="bottom", pady=10)
root.mainloop()
