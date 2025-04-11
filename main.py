import requests
import schedule
import time
import telegram
import asyncio

# توکن و آیدی ربات تلگرام شما
TOKEN = "7913278142:AAFreLlsi9pMI6zh8yxjSqT4ItOsHKUd1yk"
CHAT_ID = "@Currentprice98"  # یا آیدی چت تلگرام

# ساخت ربات تلگرام
bot = telegram.Bot(token=TOKEN)

# تابع برای دریافت قیمت‌ها
def get_prices():
    # قیمت تتر
    try:
        url_teth = "https://api.nobitex.ir/v2/orderbook/USDT-IRR"
        response_teth = requests.get(url_teth)
        data_teth = response_teth.json()
        teth_price = data_teth["data"]["asks"][0][0]  # قیمت خرید آخر
    except:
        teth_price = "اطلاعات در دسترس نیست"

    # قیمت بیت کوین
    try:
        url_btc = "https://api.nobitex.ir/v2/orderbook/BTC-IRR"
        response_btc = requests.get(url_btc)
        data_btc = response_btc.json()
        btc_price = data_btc["data"]["asks"][0][0]  # قیمت خرید آخر
    except:
        btc_price = "اطلاعات در دسترس نیست"

    # قیمت اتریوم
    try:
        url_eth = "https://api.nobitex.ir/v2/orderbook/ETH-IRR"
        response_eth = requests.get(url_eth)
        data_eth = response_eth.json()
        eth_price = data_eth["data"]["asks"][0][0]  # قیمت خرید آخر
    except:
        eth_price = "اطلاعات در دسترس نیست"

    # قیمت آب‌شده ۱۸ عیار
    try:
        url_gold = "https://www.talineh.com/api/v1/products/30"  # باید لینک صحیح محصول آب‌شده ۱۸ عیار رو قرار بدید
        response_gold = requests.get(url_gold)
        data_gold = response_gold.json()
        gold_price = data_gold["data"]["price"]  # قیمت آب‌شده ۱۸ عیار
    except:
        gold_price = "اطلاعات در دسترس نیست"

    # قیمت انس جهانی طلا
    try:
        url_ounce = "https://api.exchangerate-api.com/v4/latest/USD"
        response_ounce = requests.get(url_ounce)
        data_ounce = response_ounce.json()
        ounce_price = data_ounce["rates"]["XAU"]  # قیمت انس جهانی طلا به دلار
    except:
        ounce_price = "اطلاعات در دسترس نیست"

    # چاپ مقادیر برای بررسی
    print(f"تتر: {teth_price}, بیت‌کوین: {btc_price}, اتریوم: {eth_price}, آب‌شده: {gold_price}, انس جهانی: {ounce_price}")

    return teth_price, btc_price, eth_price, gold_price, ounce_price

# ارسال پیام به تلگرام
async def send_message():
    teth, btc, eth, gold, ounce = get_prices()

    # ساخت متن پیام
    message = f"""
    📊 قیمت لحظه‌ای:

    💵 **تتر**: {teth} تومان
    ₿ **بیت‌کوین**: {btc} تومان
    Ξ **اتریوم**: {eth} تومان

    🪙 **آب‌شده ۱۸ عیار**: {gold} تومان
    🏅 **انس جهانی طلا**: {ounce} دلار
    """

    # ارسال پیام به تلگرام به صورت غیرهمزمان
    await bot.send_message(chat_id=CHAT_ID, text=message)

# برنامه‌ریزی ارسال هر 1 دقیقه
schedule.every(1).minute.do(lambda: asyncio.run(send_message()))

# اجرای برنامه
while True:
    schedule.run_pending()
    time.sleep(1)

