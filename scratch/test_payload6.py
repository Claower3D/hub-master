import urllib.request
import urllib.error
import urllib.parse

data = urllib.parse.urlencode({'page': 'test.html', 'html': 'x'*600000}).encode('utf-8')
req = urllib.request.Request(
    'https://hub-master-production.up.railway.app/api/admin/save-page-html', 
    data=data, 
    headers={
        'Content-Type': 'application/x-www-form-urlencoded', 
        'Authorization': 'Bearer test',
        'User-Agent': 'Mozilla/5.0'
    }
)

try:
    resp = urllib.request.urlopen(req)
    print("SUCCESS")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}")
except Exception as e:
    print(f"Other Error {e}")
