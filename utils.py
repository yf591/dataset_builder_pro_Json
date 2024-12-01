# utils.py
import tiktoken

def count_tokens(text, encoding_name="cl100k_base"):
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def count_characters(text):
    return len(text)


def find_missing_ids(data):
    """
    入力済みのIDを判定し、未入力IDの情報を返す。

    Args:
        data (list): データセットのリスト

    Returns:
        tuple: 入力済みID数, 未入力IDリスト
    """

    entered_ids = set()
    for entry in data:
        if all(len(entry.get(key, "")) >= 3 for key in ["input", "output", "cot"]):
            entered_ids.add(entry["id"])

    max_id = max((entry.get("id", 0) for entry in data), default=0)
    all_ids = set(range(1, max_id + 1))

    missing_ids = sorted(list(all_ids - entered_ids))
    return len(entered_ids), missing_ids