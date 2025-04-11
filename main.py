export default {
  async fetch(request, env, ctx) {
    return handleRequest(env);
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil(handleRequest(env));
  },
};

async function handleRequest(env) {
  const wsUrl = 'wss://wss.nobitex.ir/connection/websocket';

  const symbols = [
    { symbol: "USDTIRT", title: " تتر ", unit: "تومان", factor: 0.1 },
    { symbol: "BTCIRT", title: "بیتکوین", unit: "تومان", factor: 0.1 },
    { symbol: "BTCUSDT", title: "بیتکوین", unit: "دلار", factor: 1 },
    { symbol: "ETHUSDT", title: "اتریوم", unit: "دلار", factor: 1 },
    { symbol: "XAUT", title: "انس جهانی", unit: "دلار", factor: 1 },
  ];

  const tgBotToken = 'توکن_ربات';
  const tgChannel = '@کانال_تلگرام';

  const sendToTelegram = async (messages) => {
    const tgApiUrl = `https://api.telegram.org/bot${tgBotToken}/sendMessage`;
    const body = {
      chat_id: tgChannel,
      text: messages.join("\n"),
    };

    try {
      const response = await fetch(tgApiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        console.error('Failed to send message to Telegram:', await response.text());
      }
    } catch (error) {
      console.error('Error sending message to Telegram:', error);
    }
  };

  const savePriceToKV = async (key, price) => {
    await env.gheymat_link.put(key, price.toString());
  };

  const getLastPriceFromKV = async (key) => {
    const lastPrice = await env.gheymat_link.get(key);
    return lastPrice ? parseFloat(lastPrice) : null;
  };

  const fetchTalineGoldPrice = async () => {
    try {
      const res = await fetch("https://taline.ir/");
      const text = await res.text();
      const match = text.match(/قیمت خرید طلا\s*<\/[^>]+>\s*([\d,]+)/);
      if (match && match[1]) {
        return parseInt(match[1].replace(/,/g, ""));
      }
    } catch (err) {
      console.error("Error fetching Taline gold price:", err);
    }
    return null;
  };

  const messages = [];

  // قیمت طلای آب‌شده از طلاین
  const talinePrice = await fetchTalineGoldPrice();
  if (talinePrice) {
    const formatted = new Intl.NumberFormat('fa-IR').format(talinePrice);
    messages.push(`🟡 طلای آب‌شده طلاین: ${formatted} تومان`);
  }

  for (const { symbol, title, unit, factor } of symbols) {
    await new Promise((resolve, reject) => {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        ws.send(JSON.stringify({ connect: { name: 'js' }, id: 3 }));
        ws.send(JSON.stringify({
          subscribe: {
            channel: `public:orderbook-${symbol}`,
            recover: true,
            offset: 0,
            epoch: '0',
            delta: 'fossil',
          },
          id: 4,
        }));
      };

      ws.onmessage = async (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.id === 4 && message.subscribe?.publications) {
            const publication = message.subscribe.publications[0];
            if (publication?.data) {
              const parsedData = JSON.parse(publication.data);
              if (parsedData.asks?.length > 0) {
                let current_price = parsedData.asks[0][0] * factor;
                const lastPrice = await getLastPriceFromKV(symbol);
                let trend = '';

                if (lastPrice !== null) {
                  trend = current_price > lastPrice ? '🟢' : current_price < lastPrice ? '🔴' : '⚪️';
                }

                await savePriceToKV(symbol, current_price);
                const formatted = new Intl.NumberFormat('fa-IR').format(current_price);
                messages.push(`${trend} ${title}: ${formatted} ${unit}`);
                ws.close();
                resolve();
              }
            }
          }
        } catch (error) {
          console.error(`Error parsing message for ${symbol}:`, error);
          ws.close();
          reject();
        }
      };

      ws.onerror = (error) => {
        console.error(`WebSocket error for ${symbol}:`, error);
        reject();
      };

      ws.onclose = () => {
        console.log(`WebSocket closed for ${symbol}`);
      };
    });
  }

  if (messages.length > 0) {
    await sendToTelegram(messages);
  }

  return new Response(`Prices sent to Telegram (${messages.length})`);
}
