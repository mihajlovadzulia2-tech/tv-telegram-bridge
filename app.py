import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    r.raise_for_status()

@app.post("/tv")
def tv_webhook():
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    if not text:
        symbol = data.get("symbol", "SYMBOL")
        tf = data.get("tf", "TF")
        side = data.get("side", "SIGNAL")
        price = data.get("price", "PRICE")
        text = f"{side} {symbol} {tf} @ {price}"
    send_telegram(text)
    return jsonify({"ok": True})

@app.get("/")
def home():
    return "OK", 200
