from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
from threading import Lock
from datetime import datetime, timezone

BASE = Path(__file__).parent
app = FastAPI(title="AKILLI TRADE AI Demo")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

lock = Lock()
state = {
    "cash": 7500.0,
    "initial_cash": 7500.0,
    "positions": {},
    "trades": [],
    "mode": "PAPER",
}
# Demo fiyatlarıdır; canlı piyasa verisi değildir.
prices = {
    "BTC/USDT": 64238.0,
    "ETH/USDT": 1811.0,
    "ASELS": 185.0,
    "TUPRS": 172.0,
    "ASTOR": 98.0,
}
class Order(BaseModel):
    symbol: str
    side: str
    amount_tl: float = Field(gt=0, le=7500)

@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/api/state")
def get_state():
    with lock:
        positions = []
        invested = 0.0
        market_value = 0.0
        for symbol, p in state["positions"].items():
            value = p["qty"] * prices[symbol]
            invested += p["cost"]
            market_value += value
            positions.append({
                "symbol": symbol, "qty": round(p["qty"], 8),
                "avg_price": round(p["cost"] / p["qty"], 4) if p["qty"] else 0,
                "last_price": prices[symbol], "value": round(value, 2),
                "pnl": round(value - p["cost"], 2)
            })
        equity = state["cash"] + market_value
        return {
            "mode": state["mode"], "cash": round(state["cash"], 2),
            "equity": round(equity, 2),
            "pnl": round(equity - state["initial_cash"], 2),
            "prices": prices, "positions": positions,
            "trades": state["trades"][-20:][::-1],
            "signals": [
                {"symbol": "BTC/USDT", "signal": "BEKLE", "reason": "Demo prototipinde canlı mum verisi ve doğrulanmış strateji bağlı değil."},
                {"symbol": "ASELS", "signal": "BEKLE", "reason": "Midas Menkul veri bağlantısı henüz doğrulanmadı."},
            ],
        }

@app.post("/api/order")
def paper_order(order: Order):
    if order.symbol not in prices:
        raise HTTPException(400, "Desteklenmeyen demo sembolü")
    side = order.side.upper()
    if side not in ("BUY", "SELL"):
        raise HTTPException(400, "İşlem BUY veya SELL olmalı")
    with lock:
        p = state["positions"].setdefault(order.symbol, {"qty": 0.0, "cost": 0.0})
        price = prices[order.symbol]
        qty = order.amount_tl / price
        if side == "BUY":
            if order.amount_tl > state["cash"]:
                raise HTTPException(400, "Yetersiz sanal bakiye")
            state["cash"] -= order.amount_tl
            p["qty"] += qty
            p["cost"] += order.amount_tl
        else:
            if p["qty"] <= 0:
                raise HTTPException(400, "Satılacak sanal pozisyon bulunmuyor")
            qty = min(qty, p["qty"])
            proceeds = qty * price
            avg_cost = p["cost"] / p["qty"]
            p["qty"] -= qty
            p["cost"] -= qty * avg_cost
            state["cash"] += proceeds
            order.amount_tl = proceeds
        state["trades"].append({
            "time": datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M:%S"),
            "symbol": order.symbol, "side": side,
            "amount_tl": round(order.amount_tl, 2), "price": price,
            "qty": round(qty, 8), "status": "SANAL GERÇEKLEŞTİ"
        })
    return {"ok": True, "message": "Sanal emir işlendi. Gerçek hesaba emir gönderilmedi."}

@app.post("/api/reset")
def reset():
    with lock:
        state["cash"] = state["initial_cash"]
        state["positions"] = {}
        state["trades"] = []
    return {"ok": True}
