import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import schedule
import os

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHANNEL_ID = '@Currentprice98'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_nobitex_price(symbol):
    try:
        url = f"https://api.nobitex.ir/market/stats?symbol={symbol}-irt"
        res = requests.get(url)
        data = res.json()
        return int(float(data['stats'][f'{symbol}-irt']['latest']))
    except:
        return None

def get_talain_gold():
    try:
        res = requests.get("https://talain.ir")
        soup = BeautifulSoup(res.text, 'html.parser')
        tag = soup.find('div', string="قیمت گرم ۱۸ عیار").find_next('div')
        price_text = tag.text.strip().replace(',', '')
        return int(price_text)
    except:
        return None

def get_ounce_price():
    try:
        res = requests.get("https://api.metals.live/v1/spot")
        data = res.json()
        for item in data:
            if 'gold' in item:
                return float(item['gold'])
    except:
        return None

def send_to_telegram(message):
    bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)

def job():
    usdt = get_nobitex_price('usdt')
    btc = get_nobitex_price('btc')
    eth = get_nobitex_price('eth')
    gold_18 = get_talain_gold()
    ounce = get_ounce_price()

    msg = "📊 قیمت لحظه‌ای:"
    
    if usdt: msg += f"💵 تتر (نوبیتکس): {usdt:,} تومان
"
    if btc: msg += f"₿ بیت‌کوین: {btc:,} تومان
"
    if eth: msg += f"Ξ اتریوم: {eth:,} تومان
"
    if gold_18: msg += f"🏅 طلا ۱۸ عیار: {gold_18:,} تومان
"
    if ounce: msg += f"🌍 انس جهانی: {ounce} دلار
"
    msg += "\n#بروزرسانی_خودکار"

    send_to_telegram(msg)

schedule.every(1).minutes.do(job)
print("✅ ربات فعال شد...")

while True:
    schedule.run_pending()
    time.sleep(1)
