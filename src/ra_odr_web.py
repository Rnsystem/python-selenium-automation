# src/ra_odr_web.py
import time
import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
import os
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
RAKUTEN_ORDER_NAME = os.getenv("RAKUTEN_ORDER_NAME")
RAKUTEN_ORDER_PASS = os.getenv("RAKUTEN_ORDER_PASS")

# 入力/出力ファイル初期化
output_dir = '.'

# Chrome options
dldir_path = Path(output_dir)
dldir_path.mkdir(exist_ok=True)
download_dir = str(dldir_path.resolve())

options = Options()
prefs = {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)
# options.add_argument("--headless=new")  # ヘッドレス実行したい場合はコメント解除
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# start driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

try:
    # 楽天ログインページ
    driver.get("https://glogin.rms.rakuten.co.jp/?sp_id=1")
    
    # 店舗認証
    el_login_id = wait.until(EC.presence_of_element_located((By.NAME, "login_id")))
    el_login_id.send_keys(RAKUTEN_NAME)
    el_passwd = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
    el_passwd.send_keys(RAKUTEN_PW)
    wait.until(EC.element_to_be_clickable((By.NAME, "submit"))).click()
    
    # 次ページのユーザ認証
    el_user_id = wait.until(EC.presence_of_element_located((By.NAME, "user_id")))
    el_user_id.send_keys(RAKUTEN_LOGIN_NAME)
    el_user_passwd = wait.until(EC.presence_of_element_located((By.NAME, "user_passwd")))
    el_user_passwd.send_keys(RAKUTEN_LOGIN_PASS)
    wait.until(EC.element_to_be_clickable((By.NAME, "submit"))).click()
    
    # 余分な submit があればクリック
    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "submit")), timeout=3).click()
    except:
        pass
    
    # btn-red をクリック
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-red"))).click()
    
    # お知らせがあれば進む
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'RMSメインメニューへ進む')]")
        )).click()
    except:
        print("お知らせはありませんでした。")
    
    # 画面クリック
    actions.move_by_offset(50,50).click().perform()
    actions.reset_actions()
    
    # CSVダウンロードページへアクセス
    driver.get("https://csvdl-rp.rms.rakuten.co.jp/rms/mall/csvdl/CD02_01_001?dataType=opp_order#result")
    time.sleep(1)
    
    # 日付設定（昨日）
    today = datetime.date.today()
    order_date = today + relativedelta(days=-1)
    order_date_str = order_date.strftime('%Y-%m-%d')
    
    el_from = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='fromYmd']")))
    Select(el_from).select_by_value(order_date_str)
    
    # CSV作成ボタン
    target = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@value,'データを作成する')]")
    ))
    actions.move_to_element(target).perform()
    target.click()
    
    
    # 認証フラグ待機
    while True:
        time.sleep(5)
        try:
            driver.find_element(By.NAME, 'user').send_keys(RAKUTEN_ORDER_NAME)
            driver.find_element(By.NAME, 'passwd').send_keys(RAKUTEN_ORDER_PASS)
        except:
            print('待機中...')
        else:
            print('認証成功')
            break
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[contains(@value,'ダウンロードする')]")
    )).click()
    time.sleep(10)
    
    # ログアウト
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'https://mainmenu.rms.rakuten.co.jp/?act=logout')]")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'https://glogin.rms.rakuten.co.jp/?module=BizAuth&action=BizAuthCustomerAttest&sp_id=1')]")
    )).click()
    time.sleep(2)
    
    
finally:
    driver.quit()
