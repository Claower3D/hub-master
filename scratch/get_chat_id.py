import urllib.request
import json

TOKEN = "8837427955:AAH9tieG7RrxQKr2YJpNmglr58U1oJe9lOs"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read().decode())
        if data.get("result"):
            for upd in data["result"]:
                msg = upd.get("message", {})
                chat = msg.get("chat", {})
                print(f"Chat ID: {chat.get('id')} | Username: {chat.get('username')} | Name: {chat.get('first_name')}")
        else:
            print("No updates. Send /start to your bot first, then re-run.")
except Exception as e:
    print(f"Error: {e}")
