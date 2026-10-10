import asyncio
import json
import random
import os
import websockets
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

PORT = 8080
WS_PORT = 8765

# Path to OpenFang trader-hand portfolio
PORTFOLIO_PATH = "/home/deck/.openfang/workspaces/trader-hand/data/portfolio.json"

# Wall Street base coordinates for Cesium
BASE_LON = -74.0090
BASE_LAT = 40.7070

STRATEGIES = ["Scalping", "Momentum", "Grid Trading", "DCA", "Mean Reversion", "Swing"]
SYMBOLS = ["BTC/USDT", "ETH/USDT", "NVDA", "AAPL", "MSFT", "SPY", "SOL/USDT"]

# Initialize simulated fleet of 18 daytraders in the city
traders = []
for i in range(18):
    traders.append({
        "id": f"trader_{i+1:02d}",
        "name": f"DeskBot-{i+1:02d}",
        "lon": BASE_LON + (random.random() - 0.5) * 0.0035,
        "lat": BASE_LAT + (random.random() - 0.5) * 0.0035,
        "alt": random.uniform(10.0, 75.0),
        "symbol": random.choice(SYMBOLS),
        "strategy": random.choice(STRATEGIES),
        "pnl": round(random.uniform(-150.0, 480.0), 2),
        "equity": round(10000.0 + random.uniform(-300.0, 1200.0), 2),
        "winRate": round(random.uniform(55.0, 82.0), 1),
        "sharpe": round(random.uniform(1.2, 2.8), 2),
        "confidence": random.randint(65, 96),
        "status": "ACTIVE"
    })

def read_openfang_metrics():
    """Sync with real openfang trader-hand workspace if available"""
    if os.path.exists(PORTFOLIO_PATH):
        try:
            with open(PORTFOLIO_PATH, 'r') as f:
                data = json.load(f)
                traders[0]["equity"] = round(data.get("cash", 10000.0), 2)
                traders[0]["strategy"] = data.get("strategy_style", "scalping").capitalize()
                traders[0]["name"] = "OpenFang-Leader"
        except Exception as e:
            pass

async def trader_feed(websocket):
    print(f"Client connected to Trader City WebSocket")
    try:
        while True:
            read_openfang_metrics()
            
            # Simulate real-time market action per tick
            for t in traders:
                delta_pnl = round((random.random() - 0.47) * 4.5, 2)
                t["pnl"] = round(t["pnl"] + delta_pnl, 2)
                t["equity"] = round(t["equity"] + delta_pnl, 2)
                
                # occasional position switch
                if random.random() < 0.08:
                    t["symbol"] = random.choice(SYMBOLS)
                    t["confidence"] = random.randint(68, 98)

            payload = {
                "type": "FLEET_UPDATE",
                "timestamp": int(asyncio.get_event_loop().time()),
                "traders": traders,
                "summary": {
                    "totalTraders": len(traders),
                    "totalEquity": round(sum(t["equity"] for t in traders), 2),
                    "activePnL": round(sum(t["pnl"] for t in traders), 2),
                    "winRate": round(sum(t["winRate"] for t in traders) / len(traders), 1),
                    "avgSharpe": round(sum(t["sharpe"] for t in traders) / len(traders), 2)
                }
            }
            await websocket.send(json.dumps(payload))
            await asyncio.sleep(1.0)
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")

def run_http_server():
    os.chdir('/home/deck/daytrader_city_repo')
    server = HTTPServer(('127.0.0.1', PORT), SimpleHTTPRequestHandler)
    print(f"Serving DayTrader 3D City at http://127.0.0.1:{PORT}")
    server.serve_forever()

async def main():
    threading.Thread(target=run_http_server, daemon=True).start()
    async with websockets.serve(trader_feed, "127.0.0.1", WS_PORT):
        print(f"DayTrader WebSocket streaming on ws://127.0.0.1:{WS_PORT}")
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
