import asyncio
import websockets
import requests
import schedule
import time
from telegram import Bot
from dotenv import load_dotenv
import os

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# توکن تلگرام و شناسه کانال تلگرام از فایل .env
TG_TOKEN = os.getenv('TG_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# توکن برای اتصال به نوبیتکس
ws_url = "wss://wss.nobitex.ir/connection/websocket"

# برای ارسال پیام به تلگرام
bot = Bot(token=TG_TOKEN)

# قیمت‌ها
symbols = [
    {"symbol": "USDTIRT", "title": "تتر", "unit": "تومان", "factor": 0.1},
    {"symbol": "BTCIRT", "title": "بیت‌کوین", "unit": "تومان", "factor": 0.1},
    {"symbol": "BTCUSDT", "title": "بیت‌کوین", "unit": "دلار", "factor": 1},
    {"symbol": "ETHUSDT", "title": "اتریوم", "unit": "دلار", "factor": 1},
    {"symbol": "XAUT", "title": "انس جهانی", "unit": "دلار", "factor": 1},
]

async def get_price_from_nobitex(symbol, factor):
    async with websockets.connect(ws_url) as ws:
        await ws.send('{"connect": {"name": "js"}, "id": 3}')
        await ws.send(f'{{"subscribe": {{"channel": "public:orderbook-{symbol}","recover": true}}}}')

        while True:
            msg = await ws.recv()
            try:
                data = eval(msg)  # تبدیل پیام به دیکشنری
                if 'data' in data and 'asks' in data['data']:
                    price = data['data']['asks'][0][0] * factor
                    return price
            except Exception as e:
                print(f"Error parsing message: {e}")
                continue

def send_to_telegram(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def job():
    messages = []
    for symbol in symbols:
        try:
            price = asyncio.run(get_price_from_nobitex(symbol["symbol"], symbol["factor"]))
            if price:
                formatted_price = "{:,.0f}".format(price)
                messages.append(f"{symbol['title']}: {formatted_price} {symbol['unit']}")
        except Exception as e:
            messages.append(f"Error fetching price for {symbol['title']}: {e}")

    if messages:
        send_to_telegram("\n".join(messages))

# زمان‌بندی هر 1 دقیقه
schedule.every(1).minute.do(job)

# اجرای زمان‌بندی
while True:
    schedule.run_pending()
    time.sleep(1)
