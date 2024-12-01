# gui/dialogs.py
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
import tkinter.ttk as ttk
from utils import find_missing_ids
import textwrap
from pandasgui import show
import pandas as pd
import threading
import subprocess
import json
import os


def show_all_data(data):
    top = Toplevel()
    top.title("全データ一覧")

    text = scrolledtext.ScrolledText(top, wrap=tk.WORD)
    text.pack(expand=True, fill="both")

    for entry in data:
        text.insert(tk.END, str(entry) + "\n\n")
    text.config(state=tk.DISABLED)  # 編集不可にする


def show_missing_data(data):
    entered_count, missing_ids = find_missing_ids(data)
    total_count = 100
    if entered_count < total_count:

        remaining_count = total_count - entered_count
        message = f"入力済みID数: {entered_count}\n100IDまであと: {remaining_count} ID"

    elif missing_ids:
        message = f"未入力のIDが {len(missing_ids)} 件あります:\n{', '.join(map(str, missing_ids))}"
    else:
        message = "すべてのIDが入力済みです。"

    messagebox.showinfo("未入力ID", message)


def show_table_data(data):
    """
    PandasGUIを別プロセスで実行してTkinterとの競合を防ぐ

    Args:
        data (list of dict): 表示するデータ
    """
    # JSONファイルに一時保存
    temp_file = "temp_data.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    # `show_gui.py` の絶対パスを取得
    script_path = os.path.join(os.path.dirname(__file__), "show_gui.py")

    # 別プロセスでPandasGUIを起動
    subprocess.Popen(["python", script_path, temp_file])
