import os
import requests
import asyncio
import websockets
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
import json

# بارگزاری اطلاعات از فایل .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NOBITEX_API_KEY = os.getenv("NOBITEX_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)

# WebSocket URL نوبیتکس
wsUrl = 'wss://wss.nobitex.ir/connection/websocket'

symbols = [
    { 'symbol': "USDTIRT", 'title': "تتر", 'unit': "تومان", 'factor': 0.1 },
    { 'symbol': "BTCIRT", 'title': "بیتکوین", 'unit': "تومان", 'factor': 0.1 },
    { 'symbol': "BTCUSDT", 'title': "بیتکوین", 'unit': "دلار", 'factor': 1 },
    { 'symbol': "ETHUSDT", 'title': "اتریوم", 'unit': "دلار", 'factor': 1 },
    { 'symbol': "XAUT", 'title': "انس جهانی", 'unit': "دلار", 'factor': 1 }
]

# ارسال پیام به تلگرام
async def send_message(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
    except TelegramError as e:
        print(f"Error sending message: {e.message}")

# گرفتن قیمت از نوبیتکس
async def get_prices():
    messages = []
    async with websockets.connect(wsUrl) as ws:
        for symbol in symbols:
            await ws.send(json.dumps({
                "subscribe": {
                    "channel": f"public:orderbook-{symbol['symbol']}",
                    "recover": True,
                    "offset": 0,
                    "epoch": '0',
                    "delta": 'fossil',
                },
                "id": 4,
            }))

            response = await ws.recv()
            data = json.loads(response)
            if 'data' in data:
                price = data['data']['asks'][0][0] * symbol['factor']
                formatted_price = f"{price} {symbol['unit']}"
                messages.append(f"{symbol['title']}: {formatted_price}")

    return messages

# زمانبندی ارسال پیام
async def job():
    prices = await get_prices()
    if prices:
        message = "\n".join(prices)
        await send_message(message)

# اجرای برنامه
def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(job())

if __name__ == '__main__':
    run()
