import re

with open("scratch/check_js_bundle.py", "r") as f:
    # We already have check_js_bundle.py, we can just edit/rewrite it to find API_BASE logic.
    pass

# Let's read the JS bundle we downloaded (we didn't save it to a file, let's download it again and search)
import urllib.request
url = "https://master-hub-production.up.railway.app/assets/index-BARJxVLW.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    js_code = response.read().decode('utf-8')

# Search for the pattern similar to window.location.hostname === 'localhost'
matches = re.finditer(r'localhost', js_code)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(js_code), m.end() + 100)
    print(f"Match around localhost:\n{js_code[start:end]}\n---")
