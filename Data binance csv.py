import asyncio
import json
import ssl
import websockets
import csv

# Desactivar la verificación del certificado SSL (¡No recomendado para producción!)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_NONE

async def on_message(ws, message, csv_writer):
    data = json.loads(message)

    # Verificar el tipo de evento
    if 'e' in data and data['e'] == 'kline':
        # Verificar si es un mensaje de Kline/candlestick data
        if 'k' in data:
            kline_data = data['k']
            csv_writer.writerow([kline_data['t'], kline_data['o'], kline_data['h'], kline_data['l'], kline_data['c'], kline_data['v']])

    elif 'e' in data and data['e'] == '24hrTicker':
        # Verificar si es un mensaje de 24hrTicker
        csv_writer.writerow([
            data['E'], data['s'], data['p'], data['P'], data['w'], data['x'], data['c'], data['Q'],
            data['b'], data['B'], data['a'], data['A'], data['o'], data['h'], data['l'], data['v'],
            data['q'], data['O'], data['C'], data['F'], data['L'], data['n']
        ])

async def connect():
    url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"
    async with websockets.connect(url, ssl=ssl_context) as ws:
        print("Conexión WebSocket abierta")

        # Crear archivo CSV y escribir la cabecera
        with open('datos_binance.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Escribir los nombres de las columnas en la cabecera
            csv_writer.writerow([
                'Event time', 'Symbol', 'Price change', 'Price change percent', 'Weighted average price',
                'First trade(F)-1 price', 'Last price', 'Last quantity', 'Best bid price', 'Best bid quantity',
                'Best ask price', 'Best ask quantity', 'Open price', 'High price', 'Low price', 'Total traded base asset volume',
                'Total traded quote asset volume', 'Statistics open time', 'Statistics close time', 'First trade ID',
                'Last trade ID', 'Total number of trades'
            ])

            # Suscribirse a los streams de Kline/candlestick data y 24hrTicker para el símbolo BTCUSDT
            subscribe_kline = {
                "method": "SUBSCRIBE",
                "params": [f"btcusdt@kline_1m"],
                "id": 1
            }

            subscribe_24hr_ticker = {
                "method": "SUBSCRIBE",
                "params": ["btcusdt@ticker"],
                "id": 2
            }

            await ws.send(json.dumps(subscribe_kline))
            await ws.send(json.dumps(subscribe_24hr_ticker))

            async for message in ws:
                await on_message(ws, message, csv_writer)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())
