import asyncio
import json
import ssl
import websockets

# Desactivar la verificación del certificado SSL (¡No recomendado para producción!)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_NONE

async def on_message(message):
    data = json.loads(message)
    
    # Verificar si es un mensaje de Kline/candlestick data
    if 'k' in data:
        kline_data = data['k']
        print(f"Kline Data - Time: {kline_data['t']}, Open: {kline_data['o']}, High: {kline_data['h']}, Low: {kline_data['l']}, Close: {kline_data['c']}, Volume: {kline_data['v']}")

    # Verificar si es un mensaje de Mini-Ticker data
    elif 's' in data and 'c' in data:
        print(f"Mini-Ticker Data - Symbol: {data['s']}, Close Price: {data['c']}, Volume: {data['v']}")

async def connect():
    url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"
    async with websockets.connect(url, ssl=ssl_context) as ws:
        print("Conexión WebSocket abierta")

        # Suscribirse a los streams de Kline/candlestick data y Mini-Ticker data para el símbolo BTCUSDT
        subscribe_kline = {
            "method": "SUBSCRIBE",
            "params": [f"btcusdt@kline_1m"],
            "id": 1
        }

        subscribe_mini_ticker = {
            "method": "SUBSCRIBE",
            "params": ["!miniTicker@arr"],
            "id": 2
        }

        await ws.send(json.dumps(subscribe_kline))
        await ws.send(json.dumps(subscribe_mini_ticker))

        async for message in ws:
            await on_message(message)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())
