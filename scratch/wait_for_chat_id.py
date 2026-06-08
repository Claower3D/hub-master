import urllib.request
import json
import time
import sys

# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN = "8837427955:AAH9tieG7RrxQKr2YJpNmglr58U1oJe9lOs"

print("Ozhidayu soobshchenie botu (otprav /start botu)...")
print("   Ctrl+C dlya vyhoda\n")

offset = 0
while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=20&offset={offset}"
        with urllib.request.urlopen(url, timeout=25) as r:
            data = json.loads(r.read().decode())
            if data.get("result"):
                for upd in data["result"]:
                    offset = upd["update_id"] + 1
                    msg = upd.get("message", {})
                    chat = msg.get("chat", {})
                    chat_id = chat.get("id")
                    username = chat.get("username", "net")
                    name = chat.get("first_name", "net")
                    text = msg.get("text", "")
                    print(f"POLUCHENO SOOBSHCHENIE!")
                    print(f"   Chat ID  : {chat_id}")
                    print(f"   Username : @{username}")
                    print(f"   Name     : {name}")
                    print(f"   Text     : {text}")
                    print(f"\nSkopiruyte Chat ID: {chat_id}")
    except KeyboardInterrupt:
        print("\nVyhod.")
        break
    except Exception as e:
        print(f"Oshibka: {e}")
        time.sleep(2)
