import urllib.request

url = "https://master-hub-production.up.railway.app"
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
    print("HTML Content:")
    print(html)
except Exception as e:
    print("Error:", e)
