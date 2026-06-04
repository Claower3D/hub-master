import urllib.request
import re

url = "https://master-hub-production.up.railway.app/assets/index-BARJxVLW.js"

try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        js_code = response.read().decode('utf-8')
    print("Downloaded JS bundle successfully.")
    
    # Search for api endpoints
    matches = re.findall(r'[\'"`][^\'"`]*api/[^\'"`]*[\'"`]', js_code)
    print("\nAPI-related strings found:")
    for match in set(matches[:20]):
        print(match)
        
    # Search for localhost or external domains
    domains = re.findall(r'https?://[a-zA-Z0-9.-]+(?::\d+)?', js_code)
    print("\nDomains found:")
    for d in set(domains):
        print(d)

except Exception as e:
    print(f"Error: {e}")
