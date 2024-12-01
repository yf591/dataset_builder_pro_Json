# gui/main_window.py
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, Toplevel
import json
from data_manager import DataManager
from evaluator import evaluate_entry
from utils import count_tokens, count_characters, find_missing_ids
from config import BUTTON_COLORS, MAX_TOKENS
from .components import create_labeled_textbox
from .dialogs import show_all_data, show_missing_data, show_table_data


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("DatasetBuilder & Evaluator Pro")
        self.master.geometry("900x800")
        self.master.configure(bg="white")

        self.data_manager = DataManager()
        self.current_index = 0

        self.build_gui()
        self.load_entry(1)
        self.update_entered_count() # 初期表示      


    def show_pyqt_table(self):
        show_table_data(self.data_manager.data)


    def center_window(self, event=None):  # Configure イベントを受け取る
        # ===ウィンドウを中央に配置===
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"+{x}+{y}")


    def build_gui(self):
        """GUI全体を構築"""

        canvas = tk.Canvas(self.master, bg="white")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)




        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        main_frame = tk.Frame(canvas, bg="white", padx=20, pady=20)
        canvas.create_window(0, 0, window=main_frame, anchor="nw")

        self.id_label = tk.Label(main_frame, text="ID: 1", bg="white", font=("Arial", 14, "bold"))
        self.id_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.entered_count_label = tk.Label(main_frame, text=f"入力済みID数: 0 / 100", bg="white", font=("Arial", 10, "bold"))
        self.entered_count_label.grid(row=0, column=1, sticky="w")

        search_frame = tk.Frame(main_frame, bg="white")
        search_frame.grid(row=0, column=2, sticky="e", pady=(0, 10))
        self.search_label = tk.Label(search_frame, text="IDで検索:", bg="white", font=("Arial", 10, "bold"))
        self.search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=10)
        self.search_entry.pack(side=tk.LEFT)
        self.search_button = tk.Button(search_frame, text="検索", bg=BUTTON_COLORS["navigate"], command=self.search_by_id)
        self.search_button.pack(side=tk.LEFT, padx=(5, 0))

        self.missing_button = tk.Button(main_frame, text="未入力IDの確認", bg=BUTTON_COLORS["navigate"], command=self.show_missing_data)
        self.missing_button.grid(row=0, column=3, sticky="e")

        # テキストボックスウィジェットを先に作成
        self.input_text = create_labeled_textbox(main_frame, "Input (質問):", 1, 10)
        self.output_text = create_labeled_textbox(main_frame, "Output (回答):", 2, 10)
        self.cot_text = create_labeled_textbox(main_frame, "CoT (思考過程):", 3, 10)
        self.reference_text = create_labeled_textbox(main_frame, "Reference (参照):", 4, 5)


        self.score_label = tk.Label(main_frame, text="評価点数: N/A", bg="white", fg="blue", font=("Arial", 12))
        self.score_label.grid(row=5, column=0, columnspan=4, pady=10, sticky="w")
        self.reason_label = tk.Label(main_frame, text="理由: N/A", bg="white", fg="black", wraplength=800, justify="left")
        self.reason_label.grid(row=6, column=0, columnspan=4, pady=5, sticky="w")

        top_button_frame = tk.Frame(main_frame, bg="white", pady=10)
        top_button_frame.grid(row=7, column=0, columnspan=4, sticky="we")

        bottom_button_frame = tk.Frame(main_frame, bg="white", pady=10)
        bottom_button_frame.grid(row=8, column=0, columnspan=4, sticky="we")

        self.export_button = tk.Button(top_button_frame, text="JSONデータをエクスポート", bg=BUTTON_COLORS["file_operations"], command=self.export_data)
        self.export_button.pack(side="left", padx=10)

        self.import_button = tk.Button(top_button_frame, text="JSONデータをインポート", bg=BUTTON_COLORS["file_operations"], command=self.import_data)
        self.import_button.pack(side="left", padx=10)

        self.save_button = tk.Button(top_button_frame, text="データをJSONファイル保存", bg=BUTTON_COLORS["file_operations"], command=self.save_data)
        self.save_button.pack(side="left", padx=10)


        self.evaluate_button = tk.Button(bottom_button_frame, text="評価", bg=BUTTON_COLORS["evaluate"], command=self.evaluate_entry)
        self.evaluate_button.pack(side="left", padx=10)

        self.all_data_button = tk.Button(bottom_button_frame, text="全データ一覧", bg=BUTTON_COLORS["navigate"], command=self.show_all_data)
        self.all_data_button.pack(side="left", padx=10)

        self.table_view_button = tk.Button(bottom_button_frame, text="テーブル形式で表示", bg=BUTTON_COLORS["navigate"], command=lambda: show_table_data(self.data_manager.data))
        self.table_view_button.pack(side="left", padx=10)   

        self.clear_current_button = tk.Button(bottom_button_frame, text="現在のデータクリア", command=self.clear_current_data, bg="#b0c4de")  # 色を変更
        self.clear_current_button.pack(side="left", padx=10)

        self.clear_all_button = tk.Button(bottom_button_frame, text="全データクリア", command=self.clear_all_data, bg="#FFC0CB")  # 色を変更
        self.clear_all_button.pack(side="left", padx=10)


        nav_frame = tk.Frame(bottom_button_frame, bg="white")
        nav_frame.pack(side="right")

        self.temp_save_button = tk.Button(nav_frame, text="一時保存", bg=BUTTON_COLORS["navigate"], command=lambda: self.save_entry(save_to_file=False))  # save_to_file=False を指定
        self.temp_save_button.pack(side="left", padx=10)

        self.prev_button = tk.Button(nav_frame, text="前のデータ", bg=BUTTON_COLORS["navigate"], command=self.prev_entry)
        self.prev_button.pack(side="left", padx=10)

        self.next_button = tk.Button(nav_frame, text="次のデータ", bg=BUTTON_COLORS["navigate"], command=self.next_entry)
        self.next_button.pack(side="left", padx=10)


        main_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))        
        

    def update_entered_count(self):
        """入力済みID数を更新"""
        entered_count, _ = find_missing_ids(self.data_manager.data)
        self.entered_count_label.config(text=f"入力済みID数: {entered_count} / 100")

    def load_entry(self, id_):
        """指定IDのエントリをロード"""
        entry = self.data_manager.get_entry(id_)
        if entry:
            self.id_label.config(text=f"ID: {entry['id']}")
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", entry.get("input", ""))
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", entry.get("output", ""))
            self.cot_text.delete("1.0", tk.END)
            self.cot_text.insert("1.0", entry.get("cot", ""))
            self.reference_text.delete("1.0", tk.END)
            self.reference_text.insert("1.0", entry.get("reference", "無し"))
            self.score_label.config(text=f"評価点数: {entry.get('score', 'N/A')}")  # スコアもロード
            self.reason_label.config(text=f"理由: {entry.get('reason', 'N/A')}\n改善点: {entry.get('suggestion', 'N/A')}")  # 理由と改善点もロード
        else:
            self.id_label.config(text=f"ID: {id_}")
            self.input_text.delete("1.0", tk.END)
            self.output_text.delete("1.0", tk.END)
            self.cot_text.delete("1.0", tk.END)
            self.reference_text.delete("1.0", tk.END)
            self.score_label.config(text="評価点数: N/A")
            self.reason_label.config(text="理由: N/A")
        self.update_entered_count()


    def save_entry(self, save_to_file=True): # save_to_file 引数を追加
        """現在のエントリを保存"""
        entry = {
            "id": self.current_index + 1,
            "input": self.input_text.get("1.0", tk.END).strip(),
            "output": self.output_text.get("1.0", tk.END).strip(),
            "cot": self.cot_text.get("1.0", tk.END).strip(),
            "reference": self.reference_text.get("1.0", tk.END).strip() or "無し",
            # "score": self.score_label.cget("text").split(": ")[1] if "評価点数:" in self.score_label.cget("text") else "N/A",
            # "reason": self.reason_label.cget("text").split(": ")[1].split("\n")[0] if "理由:" in self.reason_label.cget("text") else "N/A",
            # "suggestion": self.reason_label.cget("text").split("改善点: ")[1] if "改善点:" in self.reason_label.cget("text") else "N/A"
        }
        self.data_manager.update_entry(self.current_index + 1, entry)
        self.update_entered_count()

        if save_to_file:
            self.data_manager.save_data()
        else: # --- 変更点: 一時保存時のアナウンス
            messagebox.showinfo("一時保存", "現在の入力内容を一時保存しました。")


    def next_entry(self):
        """次のエントリに移動"""
        self.save_entry()
        self.current_index += 1
        self.load_entry(self.current_index + 1)


    def prev_entry(self):
        """前のエントリに移動"""
        if self.current_index > 0:
            self.save_entry()
            self.current_index -= 1
            self.load_entry(self.current_index + 1)

    def search_by_id(self):
        """IDでエントリを検索"""
        try:
            target_id = int(self.search_entry.get())
            if target_id < 1:
                raise ValueError("無効なIDです。")
            self.save_entry()
            self.current_index = target_id - 1
            self.load_entry(target_id)
        except ValueError:
            messagebox.showerror("エラー", "無効なIDが入力されました。")
            

    def evaluate_entry(self):
        """Gemini APIでエントリを評価"""
        self.save_entry()  # 評価前に現在のエントリを保存
        entry = self.data_manager.get_entry(self.current_index + 1)

        if entry:
            try:
                score, reason, suggestion = evaluate_entry(entry)

                if score is None:  # APIからのレスポンスがない場合の処理を追加
                    messagebox.showerror("エラー", "評価に失敗しました。APIからのレスポンスがありません。")
                    return

                self.score_label.config(text=f"評価点数: {score}")
                self.reason_label.config(text=f"理由: {reason}\n改善点: {suggestion}")



                # --- 変更点: 保存先を選択 ---
                choice = messagebox.askyesnocancel("評価結果の保存", "評価結果をどのように保存しますか？\n\n[はい]: 現在のファイルに追記\n[いいえ]: 別ファイルに保存\n[キャンセル]: 保存しない")

                if choice is True:  # 現在のファイルに追記
                    self.save_entry()
                    messagebox.showinfo("保存完了", "現在のファイルに評価結果を追記しました。")

                elif choice is False:  # 別ファイルに保存
                    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSONファイル", "*.json")])
                    if file_path:
                        try:
                            with open(file_path, "w", encoding="utf-8") as f:
                                evaluated_data = self.data_manager.get_entry(self.current_index + 1)
                                json.dump([evaluated_data], f, ensure_ascii=False, indent=4)  # リストで保存
                            messagebox.showinfo("保存完了", f"評価結果を {file_path} に保存しました。")
                        except Exception as e:
                            messagebox.showerror("エラー", f"保存に失敗しました: {e}")


            except Exception as e:
                messagebox.showerror("エラー", f"評価に失敗しました: {e}")


    def save_data(self):
        """データをJSONファイルに保存"""
        self.save_entry()
        self.data_manager.save_data()
        messagebox.showinfo("保存完了", "データを保存しました。")


    def export_data(self):
        """JSONデータをエクスポート"""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSONファイル", "*.json")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.data_manager.data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("エクスポート完了", "データをエクスポートしました。")
            except Exception as e:
                messagebox.showerror("エラー", f"エクスポートに失敗しました: {e}")


    def import_data(self):
        """JSONデータをインポート"""
        file_path = filedialog.askopenfilename(filetypes=[("JSONファイル", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    new_data = json.load(f)

                # --- 変更点1: 上書き確認のポップアップ表示 ---
                if self.data_manager.data: # 既存データがある場合のみ確認
                    if messagebox.askyesno("確認", "既存のデータが上書きされます。よろしいですか？"):
                        self.data_manager.data = [] # 既存データをクリア
                    else:
                        return # インポート中止

                # --- 変更点2: ID重複チェックを import_data 内に移動 ---
                max_id = max((entry.get("id", 0) for entry in self.data_manager.data), default=0)
                for entry in new_data:
                    if "id" not in entry or entry["id"] <= max_id:
                        max_id += 1
                        entry["id"] = max_id

                self.data_manager.data.extend(new_data) # 連結 (または上書き)
                self.data_manager.save_data()
                self.load_entry(1)
                messagebox.showinfo("インポート完了", "データをインポートしました。")

            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror("エラー", f"インポートエラー: {e}")
            except Exception as e:
                messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {e}")


    def show_all_data(self):
        """全データを表示"""
        show_all_data(self.data_manager.data) # dialogs.py の関数を呼び出す

    def show_missing_data(self):
        """未入力項目を表示"""
        show_missing_data(self.data_manager.data) # dialogs.py の関数を呼び出す

    def clear_all_data(self):
        """全データをクリア"""
        # --- 変更点: 全データクリア機能追加 ---
        if messagebox.askyesno("確認", "すべてのデータをクリアします。よろしいですか？"):
            self.data_manager.data = []
            self.data_manager.save_data()
            self.current_index = 0
            self.load_entry(1)
            messagebox.showinfo("クリア完了", "すべてのデータをクリアしました。")

    def clear_current_data(self):
        """現在のデータのみクリア"""
        if messagebox.askyesno("確認", "現在のデータを入力欄からクリアします。よろしいですか？"):
            self.input_text.delete("1.0", tk.END)
            self.output_text.delete("1.0", tk.END)
            self.cot_text.delete("1.0", tk.END)
            self.reference_text.delete("1.0", tk.END)
            self.score_label.config(text="評価点数: N/A")
            self.reason_label.config(text="理由: N/A")  