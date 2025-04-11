import requests
import asyncio
import telegram
import schedule
import time

# توکن تلگرام و شناسه چت
TOKEN = '7913278142:AAFreLlsi9pMI6zh8yxjSqT4ItOsHKUd1yk'
CHAT_ID = '7913278142'  # شناسه چت تلگرام خود را اینجا وارد کنید

# توکن نوبیتکس
NOBITEX_API_TOKEN = '01e14a6bcc2183c23869833cafbc08d5721291ce'

# ساخت شیء بات تلگرام
bot = telegram.Bot(token=TOKEN)

# گرفتن قیمت بیت‌کوین، اتریوم و تتر از نوبیتکس با استفاده از API
def get_nobitex_prices():
    try:
        url = "https://api.nobitex.ir/v2/orderbook/BTCIRT"
        headers = {
            'Authorization': f'Bearer {NOBITEX_API_TOKEN}'  # توکن API نوبیتکس
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        btc_price = data['data']['bids'][0][0]  # قیمت خرید بیت‌کوین
        eth_price = data['data']['bids'][0][0]  # قیمت خرید اتریوم
        teth_price = data['data']['bids'][0][0]  # قیمت خرید تتر

        return teth_price, btc_price, eth_price
    except Exception as e:
        print(f"خطا در دریافت قیمت‌ها از نوبیتکس: {e}")
        return "اطلاعات در دسترس نیست", "اطلاعات در دسترس نیست", "اطلاعات در دسترس نیست"

# ارسال پیام به تلگرام
async def send_message():
    try:
        teth, btc, eth = get_nobitex_prices()

        message = f"""
        📊 قیمت لحظه‌ای:

        💵 **تتر**: {teth} تومان
        ₿ **بیت‌کوین**: {btc} تومان
        Ξ **اتریوم**: {eth} تومان
        """

        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

# زمان‌بندی ارسال پیام هر 1 دقیقه
def job():
    asyncio.run(send_message())  # اجرای تابع غیر همزمان با asyncio.run

# زمان‌بندی برای ارسال هر دقیقه
schedule.every(1).minute.do(job)

# اجرای حلقه زمان‌بندی
while True:
    schedule.run_pending()
    time.sleep(1)
