import urllib.request
import re

url = "https://master-hub-production.up.railway.app/assets/index-BARJxVLW.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    js_code = response.read().decode('utf-8')

matches = re.finditer(r'De\.startsWith', js_code)
for m in matches:
    start = max(0, m.start() - 300)
    end = min(len(js_code), m.end() + 300)
    print(f"Match around De.startsWith:\n{js_code[start:end]}\n---")
