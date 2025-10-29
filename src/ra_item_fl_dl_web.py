# src/ra_item_fl_dl_web.py
import time
from pathlib import Path
import sys

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------
import os
from dotenv import load_dotenv

# 親ディレクトリの .env パスを取得
env_path = Path(__file__).resolve().parent.parent / ".env"
# .env を読み込む
load_dotenv(dotenv_path=env_path)

# 環境変数から取得
RAKUTEN_NAME = os.getenv("RAKUTEN_NAME")
RAKUTEN_PW = os.getenv("RAKUTEN_PW")
RAKUTEN_LOGIN_NAME = os.getenv("RAKUTEN_LOGIN_NAME")
RAKUTEN_LOGIN_PASS = os.getenv("RAKUTEN_LOGIN_PASS")

# 値の確認（デバッグ用）
print(RAKUTEN_NAME, RAKUTEN_PW, RAKUTEN_LOGIN_NAME, RAKUTEN_LOGIN_PASS)
# ------------------------------------

# download dir
dldir_name = '.'
dldir_path = Path(dldir_name)
dldir_path.mkdir(exist_ok=True)
download_dir = str(dldir_path.resolve())

# Chrome options
options = Options()
prefs = {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)
# options.add_argument("--headless=new")  # ヘッドレス実行したい場合はコメント解除
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# start driver (webdriver-manager を利用して chromedriver を自動取得)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# wait & actions
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

try:
    # rakuten にアクセス
    driver.get("https://glogin.rms.rakuten.co.jp/?sp_id=1")

    # 店舗認証フォーム入力（待機してから操作）
    el_login_id = wait.until(EC.presence_of_element_located((By.NAME, "login_id")))
    el_login_id.send_keys(RAKUTEN_NAME)

    el_passwd = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
    el_passwd.send_keys(RAKUTEN_PW)

    el_submit = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
    el_submit.click()

    # 次のページの user_id / user_passwd 入力（適宜待機）
    el_user_id = wait.until(EC.presence_of_element_located((By.NAME, "user_id")))
    el_user_id.send_keys(RAKUTEN_LOGIN_NAME)

    el_user_passwd = wait.until(EC.presence_of_element_located((By.NAME, "user_passwd")))
    el_user_passwd.send_keys(RAKUTEN_LOGIN_PASS)

    # submit を待ってクリック（同じ name の submit が複数ある可能性があるため element_to_be_clickable）
    el_submit2 = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
    el_submit2.click()

    # もしページ遷移後にさらにクリックが必要なら待機してクリック
    # ここでは例として次々クリックしている元の処理に合わせる
    time.sleep(1)  # 必要なら短い sleep を残す（ページ遷移のため）
    # 余分な submit 押下（サイトの仕様に合うなら）
    try:
        el_submit3 = wait.until(EC.element_to_be_clickable((By.NAME, "submit")), timeout=3)
        el_submit3.click()
    except Exception:
        # 見つからなければ無視
        pass
    
    # btn-red をクリック
    el_btn_red = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-red")))
    el_btn_red.click()

    # 画面上をクリック（マウスオフセット）
    actions.move_by_offset(50, 50).click().perform()
    actions.reset_actions()

    # 店舗設定クリック
    el_setting = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "rms-icon-setting")))
    el_setting.click()

    # 受注・問い合わせ管理をクリック（href を含む a を待つ）
    el_menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'https://mainmenu.rms.rakuten.co.jp/?left_navi=11')]")
    ))
    el_menu.click()

    # 次のリンク（商品管理ページへ）
    el_item_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'https://item.rms.rakuten.co.jp/rms/mall/rsf/item/vc?__event=RI00_001_002&shop_bid=200686')]")
    ))
    el_item_link.click()

    # [詳細タイプ] ラジオボタンにチェック
    el_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='file_type'][@value='7']")))
    el_radio.click()

    # ボタンまでスクロールしてクリック（CSVダウンロード）
    target = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@value='　CSVファイルをダウンロード　']")))
    actions.move_to_element(target).perform()
    target.click()

    # ダウンロード完了を短く待つ（必要に応じてより厳密に確認）
    time.sleep(3)

    # ログアウトボタンクリック
    el_logout = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'https://mainmenu.rms.rakuten.co.jp/?act=logout')]")))
    el_logout.click()

    # ログイン画面へ戻る
    el_back_login = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'https://glogin.rms.rakuten.co.jp/?module=BizAuth&action=BizAuthCustomerAttest&sp_id=1')]")))
    el_back_login.click()

    # 少し待って終了
    time.sleep(2)

finally:
    driver.quit()

print("ra_item_fl_dl_web.py】 処理が終了致しました。")
