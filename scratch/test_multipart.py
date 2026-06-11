import urllib.request
import urllib.error
import io

boundary = b'----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = io.BytesIO()
body.write(b'--' + boundary + b'\r\n')
body.write(b'Content-Disposition: form-data; name="page"\r\n\r\n')
body.write(b'test.html\r\n')
body.write(b'--' + boundary + b'\r\n')
body.write(b'Content-Disposition: form-data; name="html"; filename="test.html"\r\n')
body.write(b'Content-Type: text/html\r\n\r\n')
body.write(b'<html><head><script>alert("xss")</script></head><body>' + b'x'*500000 + b'</body></html>\r\n')
body.write(b'--' + boundary + b'--\r\n')

data = body.getvalue()

req = urllib.request.Request('https://hub-master-production.up.railway.app/api/admin/save-page-html', data=data, headers={'Content-Type': b'multipart/form-data; boundary=' + boundary, 'Authorization': 'Bearer test'})

try:
    resp = urllib.request.urlopen(req)
    print(f"Multipart: SUCCESS")
except urllib.error.HTTPError as e:
    print(f"Multipart: HTTP Error {e.code}")
except Exception as e:
    print(f"Multipart: Other Error {e}")
