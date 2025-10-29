# Python Selenium Automation

このリポジトリは、Python と Selenium を使った **Webデータ取得自動化スクリプト** をまとめたものです。  
主に **Rakuten 店舗のログインからCSVダウンロードまでの自動化** を目的としています。

---

## 概要
- ChromeDriver は `webdriver-manager` により自動取得
- ダウンロード先やログイン情報は `.env` で管理
- `.env.sample` を参考にして自分用の `.env` を作成
- Python 3.9 以上で動作確認済み

### python src/ra_item_fl_dl_web.py
- Rakuten 店舗認証 & ログイン → 商品データ CSV ダウンロードを自動化

### python src/ra_odr_web.py
- Rakuten 店舗認証 & ログイン → 受注データ CSV ダウンロードを自動化

---

## ディレクトリ構成（例）

```bash
python-selenium-automation/
├── .gitignore
├── .env.sample
├── requirements.txt
├── src/
│ └── ra_item_fl_dl_web.py
│ └── ra_odr_web.py 
└── pyenv/
└── .venv/
```

---

## 🛠 使用技術
- Python 3.9 以上
- Chrome ブラウザ（最新推奨）
- 仮想環境（推奨）
- 必要パッケージは `requirements.txt` 参照

---

## 🚀 セットアップ

### 1️⃣ リポジトリをクローン
```bash
git clone https://github.com/Rnsystem/python-selenium-automation.git
cd python-selenium-automation
```

### 2️⃣ 仮想環境を作成して有効化
```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ 必要パッケージをインストール
```bash
pip install -r requirements.txt
```

### 4️⃣ .env.sample をコピーして .env を作成し、ログイン情報を設定
```bash
cp .env.sample .env
```

---

## 使い方

### python src/ra_item_fl_dl_web.py
1. python src/ra_item_fl_dl_web.py
2. CSV がプロジェクト直下にダウンロードされます
3. スクリプト実行後は自動でログアウトされます
4. ヘッドレスモードでの実行も可能（スクリプト内 options.add_argument("--headless=new") のコメントを解除）

### python src/ra_odr_web.py
1. python src/ra_odr_web.py を実行
2. 昨日の受注データ CSV がプロジェクト直下にダウンロードされます
3. スクリプト実行後は自動でログアウトされます
4. 認証が必要な場合は、楽天受注用アカウントで自動ログインされます
5. ヘッドレスモードでの実行も可能（スクリプト内 options.add_argument("--headless=new") のコメントを解除）

---

## 🔐 環境変数（.env）

以下の環境変数（または .env ファイル）を設定してください
```bash
# Rakuten 店舗ログイン情報
RAKUTEN_NAME=your_rakuten_account
RAKUTEN_PW=your_rakuten_password
RAKUTEN_LOGIN_NAME=your_shop_login_email
RAKUTEN_LOGIN_PASS=your_shop_login_password

# Rakuten 受注データ用ログイン情報
RAKUTEN_ORDER_NAME=your_rakuten_order_account
RAKUTEN_ORDER_PASS=your_rakuten_order_password
```

### 注意事項
- .env に直接ログイン情報を書かないこと
- ChromeDriver は自動でダウンロードされますが、古いブラウザや OS によっては動作しない場合があります
- 実行中はブラウザ操作が走るので、他作業の妨げになる可能性があります

---

## 🧑‍💻 作者

**Ryohma U.**  
ポートフォリオ：[https://www.rnsystem.jp](https://www.rnsystem.jp)

---

> 💡 **補足**  
> 本システムの利用には各ECモールAPIの使用ルール遵守が必要です。
> また、商用利用の場合は利用者側で適切なセキュリティ対策をご検討ください。
