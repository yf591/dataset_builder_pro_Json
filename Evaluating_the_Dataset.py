import tkinter as tk
from tkinter import messagebox, filedialog
import json
import requests

# Gemini APIのURLとキー（適宜設定）
GEMINI_API_URL = "https://api.gemini.com/evaluate"
API_KEY = "your_api_key_here"


class EvaluationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LLM学習用データセット評価アプリ")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        # データを格納するリスト
        self.data = []

        # 現在のインデックス
        self.current_index = 0

        # GUI構築
        self.build_gui()

    def build_gui(self):
        # ID表示
        self.id_label = tk.Label(self.root, text="ID: 1", bg="white", font=("Arial", 12, "bold"))
        self.id_label.pack()

        # 各種ラベルとテキストボックス
        self.input_label = tk.Label(self.root, text="Input (質問):", bg="white")
        self.input_label.pack()
        self.input_text = tk.Text(self.root, height=5, wrap="word", width=80)
        self.input_text.pack()

        self.output_label = tk.Label(self.root, text="Output (回答):", bg="white")
        self.output_label.pack()
        self.output_text = tk.Text(self.root, height=5, wrap="word", width=80)
        self.output_text.pack()

        self.cot_label = tk.Label(self.root, text="CoT (思考過程):", bg="white")
        self.cot_label.pack()
        self.cot_text = tk.Text(self.root, height=5, wrap="word", width=80)
        self.cot_text.pack()

        self.reference_label = tk.Label(self.root, text="Reference (参照):", bg="white")
        self.reference_label.pack()
        self.reference_text = tk.Text(self.root, height=5, wrap="word", width=80)
        self.reference_text.pack()

        # 評価結果表示
        self.score_label = tk.Label(self.root, text="評価点数: N/A", bg="white", fg="blue")
        self.score_label.pack()

        # 機能ボタン
        self.evaluate_button = tk.Button(self.root, text="Geminiで評価", bg="yellow", command=self.evaluate_data)
        self.evaluate_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="データをJSONで保存", bg="yellow", command=self.save_to_json)
        self.save_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="次のデータ", bg="yellow", command=self.next_index)
        self.next_button.pack(side="right", padx=10)

        self.prev_button = tk.Button(self.root, text="前のデータ", bg="yellow", command=self.prev_index)
        self.prev_button.pack(side="right", padx=10)

        # ID検索用
        self.search_label = tk.Label(self.root, text="ID番号で検索:", bg="white")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root, width=10)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="検索", bg="yellow", command=self.search_by_id)
        self.search_button.pack()

    def evaluate_data(self):
        """Gemini APIで評価"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        output_text = self.output_text.get("1.0", tk.END).strip()
        cot_text = self.cot_text.get("1.0", tk.END).strip()
        reference_text = self.reference_text.get("1.0", tk.END).strip()

        # APIに送信するデータ
        payload = {
            "input": input_text,
            "output": output_text,
            "cot": cot_text,
            "reference": reference_text
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}

        try:
            response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            score = result.get("score", "N/A")

            # スコアを表示
            self.score_label.config(text=f"評価点数: {score}")

            # 現在のデータにスコアを追加
            self.update_current_data(payload, score)
        except Exception as e:
            messagebox.showerror("エラー", f"評価に失敗しました: {e}")

    def update_current_data(self, payload, score):
        """現在のインデックスのデータを更新"""
        payload["id"] = self.current_index + 1  # IDは1から始める
        if self.current_index >= len(self.data):
            self.data.append(payload)
        else:
            self.data[self.current_index] = payload
        self.data[self.current_index]["score"] = score

    def next_index(self):
        """次のインデックスに移動"""
        self.save_current_entry()
        self.current_index += 1
        self.display_current_data()

    def prev_index(self):
        """前のインデックスに移動"""
        self.save_current_entry()
        if self.current_index > 0:
            self.current_index -= 1
        self.display_current_data()

    def save_current_entry(self):
        """現在のエントリを保存"""
        if self.current_index >= len(self.data):
            self.data.append({})
        self.data[self.current_index] = {
            "id": self.current_index + 1,
            "input": self.input_text.get("1.0", tk.END).strip(),
            "output": self.output_text.get("1.0", tk.END).strip(),
            "cot": self.cot_text.get("1.0", tk.END).strip(),
            "reference": self.reference_text.get("1.0", tk.END).strip()
        }

    def display_current_data(self):
        """現在のインデックスのデータを表示"""
        if self.current_index < len(self.data):
            current_data = self.data[self.current_index]
            self.id_label.config(text=f"ID: {current_data.get('id', self.current_index + 1)}")
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", current_data.get("input", ""))
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", current_data.get("output", ""))
            self.cot_text.delete("1.0", tk.END)
            self.cot_text.insert("1.0", current_data.get("cot", ""))
            self.reference_text.delete("1.0", tk.END)
            self.reference_text.insert("1.0", current_data.get("reference", ""))
        else:
            self.id_label.config(text=f"ID: {self.current_index + 1}")
            self.input_text.delete("1.0", tk.END)
            self.output_text.delete("1.0", tk.END)
            self.cot_text.delete("1.0", tk.END)
            self.reference_text.delete("1.0", tk.END)

    def search_by_id(self):
        """IDでデータを検索して表示"""
        try:
            target_id = int(self.search_entry.get())
            if target_id < 1 or target_id > len(self.data):
                raise ValueError("範囲外のIDです。")
            self.current_index = target_id - 1
            self.display_current_data()
        except ValueError as e:
            messagebox.showerror("エラー", f"無効なID: {e}")

    def save_to_json(self):
        """データをJSON形式で保存"""
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSONファイル", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("保存完了", "データを保存しました")


if __name__ == "__main__":
    root = tk.Tk()
    app = EvaluationApp(root)
    root.mainloop()
