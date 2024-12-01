# show_gui.py
import pandas as pd
import subprocess
import json
import os

if __name__ == "__main__":
    import sys
    from pandasgui import show

    # JSONファイルからデータを読み取る
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    # データフレームに変換して表示
    df = pd.DataFrame(data)
    show(df)

    # 終了時に一時ファイルを削除
    os.remove(sys.argv[1])