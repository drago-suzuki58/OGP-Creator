# OGP Creator

[English README](README.md)

OGP Creatorは、DiscordやTwitterなどのプラットフォーム向けにOpen Graph Protocol(OGP)画像を簡単に生成し、共有するためのツールになっています。このプロジェクトは、魅力的なOGP画像を作成し、コンテンツの共有を強化するプロセスを簡素化します。

## 特徴

- カスタマイズ可能なOGPを生成
- DiscordやTwitterなどのソーシャルメディアプラットフォームでOGPを共有
- OGPの作成と共有が簡単なユーザーフレンドリーなインターフェース

## 構築

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/OGP-Creator.git
cd OGP-Creator
```

2. 依存関係のインストール

```bash
pip install .
```

3. 環境変数の設定

`.env.example`をコピーして`.env`にリネームし、必要な変数を設定

1. 実行

```bash
python main.py
```

## 使用方法

1. ブラウザで`http://localhost:8000`にアクセス
2. インターフェースを使用してOGPの要素を入力
3. `Create OGP`を押下
4. 真下に出てくるURLをコピーして共有
