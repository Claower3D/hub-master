import urllib.request
import urllib.error

data = b'{"page":"test.html","html":"' + b'x'*600000 + b'"}'
req = urllib.request.Request('https://hub-master-production.up.railway.app/api/admin/save-page-html', data=data, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test'})

try:
    resp = urllib.request.urlopen(req)
    print(resp.read())
except urllib.error.URLError as e:
    print("URL Error:", e)
except Exception as e:
    print("Other Error:", e)
