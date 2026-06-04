import urllib.request

for path in ['/robots.txt', '/sitemap.xml']:
    url = f"https://master-hub-production.up.railway.app{path}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            print(f"URL: {url}")
            print(f"Content:\n{content[:200]}\n---")
    except Exception as e:
        print(f"URL: {url} Error: {e}")
