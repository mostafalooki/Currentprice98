import requests
from bs4 import BeautifulSoup
import schedule
import time
from telegram import Bot
from dotenv import load_dotenv
import os

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# توکن و شناسه کانال تلگرام
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# تابع ارسال پیام به کانال تلگرام
def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHANNEL_ID, text=message)

# تابع دریافت قیمت از نوبیتکس
def get_prices():
    try:
        url = "https://api.nobitex.ir/v2/ticker"
        response = requests.get(url)
        data = response.json()

        teth_price = data['Tether']['last']
        btc_price = data['BTC']['last']
        eth_price = data['ETH']['last']
        
        return teth_price, btc_price, eth_price
    except Exception as e:
        return f"خطا در دریافت قیمت: {str(e)}"

# ارسال قیمت‌ها هر دقیقه
def job():
    teth, btc, eth = get_prices()
    message = f"""
📊 قیمت لحظه‌ای:

💵 **تتر**: {teth} تومان
₿ **بیت‌کوین**: {btc} تومان
Ξ **اتریوم**: {eth} تومان
"""
    send_to_telegram(message)

# برنامه زمانبندی برای ارسال قیمت‌ها هر 1 دقیقه
schedule.every(1).minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
