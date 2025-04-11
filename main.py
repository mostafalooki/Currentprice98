import asyncio
import websockets
import json
import schedule
import time
from telegram import Bot
from telegram.error import TelegramError

# اطلاعات تلگرام (توکن ربات و آیدی کانال)
TG_BOT_TOKEN = '7913278142:AAFreLlsi9pMI6zh8yxjSqT4ItOsHKUd1yk'
TG_CHANNEL_ID = '@Currentprice98'

# URL وب‌ساکت نوبیتکس
WS_URL = 'wss://wss.nobitex.ir/connection/websocket'

# تابع ارسال پیام به تلگرام
def send_to_telegram(message):
    bot = Bot(token=TG_BOT_TOKEN)
    try:
        bot.send_message(chat_id=TG_CHANNEL_ID, text=message)
    except TelegramError as e:
        print(f"Error sending message: {e}")

# تابع برای دریافت قیمت تتر از نوبیتکس
async def get_tether_price():
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                # اشتراک در کانال قیمت تتر
                subscribe_message = {
                    "connect": {"name": "js"},
                    "subscribe": {
                        "channel": "public:orderbook-USDTIRT",  # کانال قیمت تتر
                        "recover": True,
                        "offset": 0,
                        "epoch": '0',
                        "delta": 'fossil'
                    },
                    "id": 4
                }

                await ws.send(json.dumps(subscribe_message))  # ارسال پیام اشتراک

                while True:
                    # ارسال پینگ هر 30 ثانیه برای حفظ اتصال
                    await ws.ping()
                    await asyncio.sleep(30)

                    response = await ws.recv()
                    message = json.loads(response)

                    if 'id' in message and message['id'] == 4:
                        if 'subscribe' in message and 'publications' in message['subscribe']:
                            publication = message['subscribe']['publications'][0]
                            if publication.get('data'):
                                data = json.loads(publication['data'])
                                if data.get('asks') and len(data['asks']) > 0:
                                    tether_price = data['asks'][0][0]  # قیمت تتر
                                    print(f"Current Tether Price: {tether_price}")
                                    formatted_price = f"💵 قیمت تتر: {tether_price} تومان"
                                    send_to_telegram(formatted_price)  # ارسال قیمت به تلگرام
                                    break  # پس از ارسال قیمت، اتصال WebSocket را قطع می‌کنیم

        except websockets.exceptions.ConnectionClosedError as e:
            print("WebSocket connection closed, reconnecting...")
            await asyncio.sleep(5)  # تلاش مجدد برای اتصال بعد از 5 ثانیه

# تابع ارسال قیمت به صورت دوره‌ای (هر دقیقه)
def job():
    print("Getting Tether price and sending to Telegram...")
    asyncio.run(get_tether_price())

# تنظیم برنامه برای ارسال قیمت هر 1 دقیقه
schedule.every(1).minute.do(job)

# اجرای برنامه به صورت مداوم
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
