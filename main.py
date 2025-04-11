import asyncio
import websockets
import requests
import json

# اطلاعات تلگرام
TG_BOT_TOKEN = 'توکن_ربات_تلگرام'
TG_CHANNEL = '@کانال_تلگرام'

# URL WebSocket نوبیتکس
WS_URL = 'wss://wss.nobitex.ir/connection/websocket'

# نمادها و اطلاعات مربوط به هر کدام
symbols = [
    {'symbol': 'USDTIRT', 'title': 'تتر', 'unit': 'تومان', 'factor': 0.1},
    {'symbol': 'BTCIRT', 'title': 'بیتکوین', 'unit': 'تومان', 'factor': 0.1},
    {'symbol': 'BTCUSDT', 'title': 'بیتکوین', 'unit': 'دلار', 'factor': 1},
    {'symbol': 'ETHUSDT', 'title': 'اتریوم', 'unit': 'دلار', 'factor': 1},
    {'symbol': 'XAUT', 'title': 'انس جهانی', 'unit': 'دلار', 'factor': 1}
]

# تابع ارسال پیام به تلگرام
def send_to_telegram(messages):
    tg_api_url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    body = {
        'chat_id': TG_CHANNEL,
        'text': '\n'.join(messages)
    }
    try:
        response = requests.post(tg_api_url, json=body)
        if not response.ok:
            print(f"Error sending message to Telegram: {response.text}")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

# تابع دریافت قیمت طلای آب‌شده از طلاین
async def fetch_taline_gold_price():
    try:
        res = requests.get('https://taline.ir/')
        text = res.text
        match = re.search(r'قیمت خرید طلا\s*<\/[^>]+>\s*([\d,]+)', text)
        if match:
            return int(match.group(1).replace(',', ''))
    except Exception as e:
        print(f"Error fetching Taline gold price: {e}")
    return None

# تابع دریافت قیمت‌ها از نوبیتکس
async def fetch_prices():
    messages = []
    
    # دریافت قیمت طلا از طلاین
    taline_price = await fetch_taline_gold_price()
    if taline_price:
        formatted = f'{taline_price:,}'
        messages.append(f"🟡 طلای آب‌شده طلاین: {formatted} تومان")
    
    # برقراری ارتباط WebSocket با نوبیتکس
    async with websockets.connect(WS_URL) as websocket:
        # ارسال درخواست اتصال و اشتراک به هر یک از نمادها
        await websocket.send(json.dumps({'connect': {'name': 'js'}, 'id': 3}))
        for symbol in symbols:
            await websocket.send(json.dumps({
                'subscribe': {
                    'channel': f'public:orderbook-{symbol["symbol"]}',
                    'recover': True,
                    'offset': 0,
                    'epoch': '0',
                    'delta': 'fossil'
                },
                'id': 4
            }))
        
        while True:
            try:
                # دریافت پیام از WebSocket
                message = await websocket.recv()
                data = json.loads(message)
                
                if 'subscribe' in data and 'publications' in data['subscribe']:
                    publication = data['subscribe']['publications'][0]
                    if 'data' in publication:
                        parsed_data = json.loads(publication['data'])
                        if parsed_data.get('asks') and len(parsed_data['asks']) > 0:
                            current_price = parsed_data['asks'][0][0] * symbol['factor']
                            formatted_price = f'{current_price:,.2f}'
                            messages.append(f"{symbol['title']}: {formatted_price} {symbol['unit']}")
            except Exception as e:
                print(f"Error processing WebSocket message: {e}")
                break
    
    return messages

# تابع اصلی برای ارسال قیمت‌ها
async def main():
    messages = await fetch_prices()
    if messages:
        send_to_telegram(messages)

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(main())
