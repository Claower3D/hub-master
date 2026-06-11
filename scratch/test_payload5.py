import urllib.request
import urllib.error

data = b'{"page":"test.html","html":"' + b'x'*600000 + b'"}'
req = urllib.request.Request(
    'https://hub-master-production.up.railway.app/api/admin/save-page-html', 
    data=data, 
    headers={
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer test',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
)

try:
    resp = urllib.request.urlopen(req)
    print("SUCCESS")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}")
except Exception as e:
    print(f"Other Error {e}")
