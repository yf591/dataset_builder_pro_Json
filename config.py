# config.py

# Gemini API設定 (APIキーなどは各自設定)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"  # 仮のURL
API_KEY = "GOOGLE_APPLICATION_CREDENTIALS"

# 入力制限
MAX_TOKENS = 1024

# 色設定
BUTTON_COLORS = {
    "evaluate": "yellow",
    "navigate": "#e0e0e0",
    "file_operations": "#f0f0f0"
}

# ファイルパス
DATASET_FILE = "dataset.json"