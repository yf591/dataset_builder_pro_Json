# tests/test_evaluator.py
import sys
import os

# プロジェクトのルートディレクトリをモジュール検索パスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from evaluator import evaluate_entry

def run_test():
    """テスト用のエントリデータを評価"""
    # テスト用エントリデータ
    entry = {
        "input": "ユーザーがAIについて質問した内容です。",
        "output": "AIとは人工知能のことで、コンピュータが人間の知能を模倣する技術です。",
        "cot": "質問内容を解析し、人工知能の定義に基づいて回答を生成。",
        "reference": "人工知能: コンピュータ科学分野の一つで、人間の知能を模倣する技術。"
    }

    # Gemini APIで評価
    score, reason, suggestion = evaluate_entry(entry)

    # 結果を出力
    if score is not None:
        print(f"評価スコア: {score}")
        print(f"理由: {reason}")
        print(f"改善点: {suggestion}")
    else:
        print("評価に失敗しました。")

if __name__ == "__main__":
    run_test()
