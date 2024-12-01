# Dataset Builder & Evaluator Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dataset Builder & Evaluator Proは、機械学習モデルのトレーニングに使用する高品質なデータセットを作成、評価、管理するためのGUIアプリケーションです。
このツールは、質問応答データセットの作成に特に焦点を当てており、入力、出力、思考過程（CoT）、参照テキストなどのフィールドを備えています。Gemini APIとの統合により、データ品質の自動評価と改善提案が可能になります。


## 特徴

* **GUIによる直感的なデータ入力と管理:** ユーザーフレンドリーなインターフェースで、データ入力が容易になります。
* **思考過程（CoT）の記録:** モデルの推論プロセスを理解し、改善に役立ちます。
* **参照テキストの追加:** 正解データや関連情報を参照テキストとして追加できます。
* **Gemini APIによる自動評価:** データ品質を自動評価し、改善点を提案します。
* **JSON形式でのデータ入出力:** データセットを簡単にエクスポート・インポートできます。
* **データの検索、フィルタリング、ソート:** 大規模なデータセットでも効率的に管理できます。
* **未入力データの確認:** データセットの完成度を把握できます。
* **PandasGUIによるテーブル形式表示:** データセット全体をテーブル形式で確認できます。
* **柔軟なデータクリア機能:** 現在のデータ、または全データをクリアする機能を提供します。



## ファイル構成

```
dataset_builder_pro/
├── gui/
│   ├── __init__.py
│   ├── components.py
│   ├── dialogs.py
│   └── main_window.py
├── tests/
│   ├── __init__.py
│   └── test_evaluator.py
├── show_gui.py
├── config.py
├── data_manager.py
├── evaluator.py
├── main.py
├── utils.py
└── README.md
```

## インストール

```bash
git clone https://github.com/yf591/dataset_builder_pro.git
cd dataset_builder_pro
pip install -r requirements.txt
```

`requirements.txt` ファイルには、以下の依存関係を含めてください。

```
tiktoken
requests
pandas
pandasgui
tk
```

## 使い方

1. `config.py` ファイルで、Gemini APIキーを設定します。
2. `main.py` を実行してアプリケーションを起動します。
3. データを入力し、「評価」ボタンをクリックして評価結果を確認します。
4. 必要に応じてデータを修正し、JSONファイルに保存します。

## ライセンス

このプロジェクトはMITライセンスで公開されています。詳しくは、[LICENSE](LICENSE)ファイルをご覧ください。


## 開発者向け情報
作成中

### テストの実行


```bash
python tests/test_evaluator.py
```


### その他

* `show_gui.py`: PandasGUIを使ってデータを表示するためのヘルパースクリプトです。メインアプリケーションから呼び出されます。
* `gui` ディレクトリ: GUIコンポーネントのコードが含まれています。
*  `utils.py`: トークン数や文字数のカウント、未入力IDの確認など、ユーティリティ関数が含まれています。
