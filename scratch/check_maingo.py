import urllib.request

url = "https://master-hub-production.up.railway.app/main.go"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        print("Successfully fetched main.go!")
        print(f"Content (first 100 chars):\n{content[:100]}\n---")
except Exception as e:
    print(f"Error fetching main.go: {e}")
