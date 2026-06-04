import urllib.request
import re

url = "https://master-hub-production.up.railway.app/assets/index-BARJxVLW.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    js_code = response.read().decode('utf-8')

# Find fetch calls to api/callback
matches = re.finditer(r'/api/callback', js_code)
for m in matches:
    start = max(0, m.start() - 150)
    end = min(len(js_code), m.end() + 250)
    print(f"Match around /api/callback:\n{js_code[start:end]}\n---")
