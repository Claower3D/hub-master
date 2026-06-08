import urllib.request

url = "https://masterhub.kz"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read()
        print(f"URL: {url} | Response Length: {len(content)} bytes")
except Exception as e:
    print(f"URL: {url} | Error: {e}")
