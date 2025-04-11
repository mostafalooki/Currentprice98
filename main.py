import requests
import schedule
import time
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# توکن تلگرام و ID چت
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# آدرس API نوبیتکس برای قیمت‌ها
NOBITEX_API_URL = "https://api.nobitex.ir/v2/orderbook/"

# ساخت بات تلگرام
bot = Bot(token=TOKEN)

# تابع برای دریافت قیمت‌ها
def get_prices():
    try:
        # دریافت قیمت تتر
        teth_response = requests.get(NOBITEX_API_URL + 'USDTIRR')
        teth_price = teth_response.json()['last_price'] if teth_response.status_code == 200 else 'اطلاعات در دسترس نیست'

        # دریافت قیمت بیتکوین
        btc_response = requests.get(NOBITEX_API_URL + 'BTCIRR')
        btc_price = btc_response.json()['last_price'] if btc_response.status_code == 200 else 'اطلاعات در دسترس نیست'

        # دریافت قیمت اتریوم
        eth_response = requests.get(NOBITEX_API_URL + 'ETHIRR')
        eth_price = eth_response.json()['last_price'] if eth_response.status_code == 200 else 'اطلاعات در دسترس نیست'

        # در اینجا می‌توانی قیمت‌های دیگری هم اضافه کنی، مثل آب‌شده و انس طلا

        return teth_price, btc_price, eth_price

    except Exception as e:
        print(f"Error: {e}")
        return 'اطلاعات در دسترس نیست', 'اطلاعات در دسترس نیست', 'اطلاعات در دسترس نیست'

# ارسال پیام به تلگرام
async def send_message():
    teth, btc, eth = get_prices()
    message = f"""
    💵 **تتر**: {teth} تومان
    ₿ **بیت‌کوین**: {btc} تومان
    Ξ **اتریوم**: {eth} تومان
    """
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")

# برنامه‌ریزی برای ارسال پیام‌ها
def job():
    asyncio.run(send_message())

# زمانبندی برای ارسال پیام هر 1 دقیقه
schedule.every(1).minute.do(job)

# اجرای زمانبندی
while True:
    schedule.run_pending()
    time.sleep(1)
