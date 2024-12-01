# data_manager.py
import json
from config import DATASET_FILE

class DataManager:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """JSONファイルからデータを読み込み"""
        try:
            with open(DATASET_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self):
        """データをJSONファイルに保存"""
        with open(DATASET_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_entry(self, id_):
        """指定したIDのエントリを取得"""
        if 0 < id_ <= len(self.data):
            return self.data[id_ - 1]
        return None

    def update_entry(self, id_, entry):
        """指定したIDのエントリを更新"""
        if 0 < id_ <= len(self.data):
            self.data[id_ - 1] = entry
        elif id_ == len(self.data) + 1:
            self.data.append(entry)
        self.save_data()

    def import_data(self, file_path):
        """JSONデータをインポート"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                new_data = json.load(f)
                # IDの重複を避けるための処理を追加
                max_id = max(entry.get("id", 0) for entry in self.data)
                for entry in new_data:
                    if "id" not in entry:
                        entry["id"] = max_id + 1
                        max_id += 1
                    elif entry["id"] <= max(entry.get("id", 0) for entry in self.data):
                        entry["id"] = max_id + 1
                        max_id += 1


                self.data.extend(new_data)
                self.save_data()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"インポートエラー: {e}")
