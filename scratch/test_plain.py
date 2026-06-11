import urllib.request
import urllib.error

# 600KB
data = b'<html><body>' + b'hello ' * 100000 + b'</body></html>'
req = urllib.request.Request('https://hub-master-production.up.railway.app/api/admin/save-page-html?page=test.html', data=data, headers={'Content-Type': 'text/plain', 'Authorization': 'Bearer test'})

try:
    resp = urllib.request.urlopen(req)
    print(f"Plain Text: SUCCESS")
except urllib.error.HTTPError as e:
    print(f"Plain Text: HTTP Error {e.code}")
except Exception as e:
    print(f"Plain Text: Other Error {e}")
