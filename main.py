import os
import threading
import time
import requests
from flask import Flask

TOKEN = "360729900:nkuhQxqh3Xt0fLqgo-9ABBbxWBbgi8yobsE"  # ← توکن ربات بله
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

app = Flask(__name__)


# -----------------------------
#      Bale API FUNCTIONS
# -----------------------------
def get_updates(offset=None, timeout=20):
    url = BASE_URL + "getUpdates"
    params = {"timeout": timeout}
    if offset:
        params["offset"] = offset

    try:
        r = requests.get(url, params=params, timeout=timeout + 5)
        return r.json().get("result", [])
    except Exception as e:
        print("get_updates error:", e)
        return []


def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
        if r.status_code != 200:
            print("send_message failed:", r.status_code, r.text)
    except Exception as e:
        print("send_message error:", e)


def handle_text(text):
    t = text.strip().lower()

    if t in ["سلام", "hi", "hello", "salam"]:
        return "سلام 👋"

    if "چطوری" in t:
        return "خوبم، تو چطوری؟"

    if "خوبی" in t:
        return "مرسی، خوبم 😊"

    return "من یک ربات تست ساده‌ام. بگو «سلام» یا «چطوری» 🙂"


# -----------------------------
#        BOT LOOP
# -----------------------------
def bot_loop():
    print("Bot polling loop started...")
    last_update_id = None

    while True:
        updates = get_updates(offset=last_update_id)

        for upd in updates:
            last_update_id = upd.get("update_id", last_update_id)
            if last_update_id:
                last_update_id += 1

            msg = upd.get("message")
            if not msg:
                continue

            text = msg.get("text")
            chat_id = msg.get("chat", {}).get("id")

            if not text or not chat_id:
                continue

            print(f"[Bale] {chat_id}: {text}")
            reply = handle_text(text)
            send_message(chat_id, reply)

        time.sleep(1)


# -----------------------------
#        FLASK SERVER
# -----------------------------
@app.route("/")
def home():
    return "Bale bot is running on Render ✓"


# -----------------------------
#         ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    # Start bot loop in a background thread
    threading.Thread(target=bot_loop, daemon=True).start()

    # Run Flask web server so Render sees an open port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
