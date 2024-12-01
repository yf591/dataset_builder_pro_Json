# gui/components.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from utils import count_tokens, count_characters
from config import MAX_TOKENS


class ResizableScrolledText(scrolledtext.ScrolledText):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.bind("<Button-1><B1-Motion>", self.on_resize)

    def on_resize(self, event):
        try:
            # マウスの位置から行数を計算
            height = int(event.y / self.font.metrics("linespace"))
            if height <= 0 : # 最小の高さを１行に制限
                height = 1


            self.configure(height=height)
        except Exception as e:
            print(f"リサイズエラー: {e}") # エラー発生時の処理を追加


def create_labeled_textbox(parent, label_text, row, height):
    frame = tk.Frame(parent, bg="white", bd=1, relief="solid", highlightbackground="black", highlightthickness=1, padx=5, pady=5)
    frame.grid(row=row, column=0, columnspan=4, pady=5, sticky="we")

    label = tk.Label(frame, text=label_text, bg="white")
    label.pack(anchor="nw")

    text = ResizableScrolledText(frame, height=height, width=80, wrap="word", bd=0, relief="flat")
    text.pack(side=tk.LEFT, fill="both", expand=True)

    def clear_text():
        if messagebox.askyesno("確認", f"{label_text} をクリアしますか？"):  # 確認ダイアログを追加
            text.delete("1.0", tk.END)

    clear_button = tk.Button(frame, text="クリア", command=clear_text, bg="#b0c4de")
    clear_button.pack(side=tk.RIGHT, anchor="se")

    add_token_counter(frame, text)

    return text


def add_token_counter(parent, textbox):
    """トークンと文字数をリアルタイムで表示"""
    counter_label = tk.Label(parent, text="文字数: 0, トークン数: 0", bg="white", fg="gray", anchor="e")
    counter_label.pack(anchor="e")

    def update_counter(event):
        text = textbox.get("1.0", "end-1c")
        char_count = count_characters(text)
        token_count = count_tokens(text)
        counter_label.config(text=f"文字数: {char_count}, トークン数: {token_count}")
        if "Input" in str(textbox) or "Output" in str(textbox): # textbox._name は非推奨なので str(textbox) を使用
            if token_count > MAX_TOKENS:
                counter_label.config(fg="red")
            else:
                counter_label.config(fg="gray")

    textbox.bind("<KeyRelease>", update_counter)