import requests
from bs4 import BeautifulSoup

# تابع برای گرفتن قیمت تتر از نوبیتکس
def get_tether_price():
    url = 'https://www.nobitex.ir'  # آدرس سایت نوبیتکس
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # استخراج قیمت تتر از سایت نوبیتکس (فرض می‌کنیم داخل یک div با کلاس 'price' است)
    tether_price_tag = soup.find('span', {'class': 'price'})
    if tether_price_tag:
        return tether_price_tag.text.strip()
    else:
        return "اطلاعات در دسترس نیست"

# تابع برای گرفتن قیمت بیت‌کوین از نوبیتکس
def get_bitcoin_price():
    url = 'https://www.nobitex.ir'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # فرض می‌کنیم که قیمت بیت‌کوین داخل یک span با کلاس 'price' است
    bitcoin_price_tag = soup.find('span', {'class': 'price'})
    if bitcoin_price_tag:
        return bitcoin_price_tag.text.strip()
    else:
        return "اطلاعات در دسترس نیست"

# تابع برای گرفتن قیمت اتریوم از نوبیتکس
def get_ethereum_price():
    url = 'https://www.nobitex.ir'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # فرض می‌کنیم که قیمت اتریوم داخل یک span با کلاس 'price' است
    ethereum_price_tag = soup.find('span', {'class': 'price'})
    if ethereum_price_tag:
        return ethereum_price_tag.text.strip()
    else:
        return "اطلاعات در دسترس نیست"

# تابع برای گرفتن قیمت آب‌شده از طلاین
def get_gold_price():
    url = 'https://www.talineh.com'  # آدرس سایت طلاین
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # فرض می‌کنیم که قیمت آب‌شده داخل یک div با کلاس 'gold-price' است
    gold_price_tag = soup.find('span', {'class': 'gold-price'})
    if gold_price_tag:
        return gold_price_tag.text.strip()
    else:
        return "اطلاعات در دسترس نیست"

# تابع برای گرفتن انس جهانی طلا از TradingView
def get_gold_ounce_price():
    url = 'https://www.tradingview.com'  # آدرس سایت تریدینگ ویو
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # فرض می‌کنیم که قیمت انس جهانی طلا داخل یک span با کلاس 'ounce-price' است
    gold_ounce_price_tag = soup.find('span', {'class': 'ounce-price'})
    if gold_ounce_price_tag:
        return gold_ounce_price_tag.text.strip()
    else:
        return "اطلاعات در دسترس نیست"

# اصلی: دریافت همه قیمت‌ها
def get_all_prices():
    tether_price = get_tether_price()
    bitcoin_price = get_bitcoin_price()
    ethereum_price = get_ethereum_price()
    gold_price = get_gold_price()
    gold_ounce_price = get_gold_ounce_price()

    # نمایش قیمت‌ها
    print(f"💵 **تتر**: {tether_price} تومان")
    print(f"₿ **بیت‌کوین**: {bitcoin_price} تومان")
    print(f"Ξ **اتریوم**: {ethereum_price} تومان")
    print(f"🪙 **آب‌شده ۱۸ عیار**: {gold_price} تومان")
    print(f"🏅 **انس جهانی طلا**: {gold_ounce_price} دلار")

# اجرا
get_all_prices()
