import requests
import time
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# توکن ربات تلگرام و شناسه کانال
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "@Currentprice98"  # آیدی کانالت با @ شروع میشه

# دریافت قیمت‌ها از نوبیتکس
def get_nobitex_prices():
    url = "https://api.nobitex.ir/market/stats"
    response = requests.post(url, data={"srcCurrency": "usdt", "dstCurrency": "rls"})
    data = response.json()
    
    # چاپ داده‌ها برای بررسی
    print
