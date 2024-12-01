# evaluator.py
import requests
from tkinter import messagebox
from config import API_KEY, GEMINI_API_URL

def evaluate_entry(entry):
    """
    Gemini APIを使用してエントリを評価する。
    入力データ、思考過程、出力の精度を1～5段階で評価し、理由と改善点を返す。

    Args:
        entry (dict): エントリデータ。input, output, cot, referenceを含む辞書。

    Returns:
        tuple: 評価スコア、理由、改善点 (いずれかが抽出に失敗した場合はNoneを返す)。
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 必須項目を取得
    input_text = entry.get("input", "")
    output_text = entry.get("output", "")
    cot_text = entry.get("cot", "")
    reference_text = entry.get("reference", "無し")  # 空欄時は「無し」をデフォルト値に

    # プロンプトの作成
    prompt = f"""以下の入力、思考過程、出力、参照テキストに基づいて、出力の精度と思考過程を1から5の5段階で評価してください。
また、評価の理由と改善点を具体的に記述してください。

入力:
{input_text}

思考過程:
{cot_text}

出力:
{output_text}

参照テキスト:
{reference_text}

評価: (1-5)
理由:
改善点:
"""

    # リクエストデータの作成
    request_data = {
        "model": "gemini-1.5-flash-latest",
        "prompt": prompt,
        "temperature": 0.7,  # 応答の安定性を調整（適宜変更可能）
        "max_tokens": 512   # 応答のトークン制限
    }

    try:
        # APIリクエスト送信
        response = requests.post(GEMINI_API_URL, headers=headers, json=request_data)
        response.raise_for_status()  # ステータスコードの確認

        # API応答データの処理
        result = response.json()
        generated_text = result.get("candidates", [{}])[0].get("output", "")

        # 評価、理由、改善点を抽出
        try:
            score = int(generated_text.split("評価: ")[1].split("\n")[0].strip())
            reason = generated_text.split("理由: ")[1].split("\n改善点: ")[0].strip()
            suggestion = generated_text.split("改善点: ")[1].strip()

            # 評価スコアが1～5の範囲外の場合エラー
            if not 1 <= score <= 5:
                raise ValueError("評価スコアは1から5の間でなければなりません。")

            return score, reason, suggestion

        except (IndexError, ValueError) as e:  # 抽出失敗時
            messagebox.showerror(
                "解析エラー",
                f"Gemini APIの応答から評価結果を解析できませんでした: {e}\n\n応答全文:\n{generated_text}"
            )
            return None, None, None

    except requests.exceptions.RequestException as e:
        # APIリクエストエラー時の処理
        messagebox.showerror("APIエラー", f"Gemini APIのリクエストに失敗しました: {e}")
        return None, None, None
