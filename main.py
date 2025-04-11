import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "@Currentprice98"  # آیدی کانالت با @ شروع میشه

def get_nobitex_prices():
    url = "https://api.nobitex.ir/market/stats"
    response = requests.post(url, data={"srcCurrency": "usdt", "dstCurrency": "rls"})
    data = response.json()
    tether_price = int(float(data['stats']['usdt-rls']['latest'])) if isinstance(data['stats']['usdt-rls']['latest'], (int, float)) else 0

    btc = requests.post(url, data={"srcCurrency": "btc", "dstCurrency": "rls"})
    btc_price = int(float(btc.json()['stats']['btc-rls']['latest'])) if isinstance(btc.json()['stats']['btc-rls']['latest'], (int, float)) else 0

    eth = requests.post(url, data={"srcCurrency": "eth", "dstCurrency": "rls"})
    eth_price = int(float(eth.json()['stats']['eth-rls']['latest'])) if isinstance(eth.json()['stats']['eth-rls']['latest'], (int, float)) else 0

    return tether_price, btc_price, eth_price

def get_abshode_price():
    try:
        response = requests.get("https://api.tala.in/api/v1/live")
        data = response.json()
        abshode_price = int(data['data']['geram18']['price']) if isinstance(data['data']['geram18']['price'], (int, float)) else 0
        return abshode_price
    except:
        return 0

def get_ons_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd")
        ons = float(response.json()['tether-gold']['usd']) if isinstance(response.json()['tether-gold']['usd'], (int, float)) else 0
        return ons
    except:
        return 0

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def main():
    while True:
        try:
            tether_price, btc_price, eth_price = get_nobitex_prices()
            abshode_price = get_abshode_price()
            ons_price = get_ons_price()

            msg = f"""📊 قیمت لحظه‌ای:
💵 تتر: {int(tether_price):,} تومان
₿ بیت‌کوین: {int(btc_price):,} تومان
Ξ اتریوم: {int(eth_price):,} تومان
🪙 آب‌شده ۱۸ عیار: {int(abshode_price):,} تومان
🏅 انس جهانی طلا: {float(ons_price):,.2f} دلار
"""

            send_message(msg)
        except Exception as e:
            send_message(f"⚠️ خطا در دریافت قیمت: {e}")

        time.sleep(60)

if __name__ == "__main__":
    main()
