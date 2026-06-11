import urllib.request
import urllib.error

sizes = [600000]

for size in sizes:
    # 600KB with spaces
    data = b'{"page":"test.html","html":"' + b'x '*(size//2) + b'"}'
    req = urllib.request.Request('https://hub-master-production.up.railway.app/api/admin/save-page-html', data=data, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test'})

    try:
        resp = urllib.request.urlopen(req)
        print(f"Size {size}: SUCCESS")
    except urllib.error.HTTPError as e:
        print(f"Size {size}: HTTP Error {e.code}")
    except Exception as e:
        print(f"Size {size}: Other Error {e}")
