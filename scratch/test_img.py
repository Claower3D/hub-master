import urllib.request
import urllib.error
import io

boundary = b'----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = io.BytesIO()
body.write(b'--' + boundary + b'\r\n')
body.write(b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n')
body.write(b'Content-Type: image/jpeg\r\n\r\n')
body.write(b'x'*600000 + b'\r\n')
body.write(b'--' + boundary + b'--\r\n')

data = body.getvalue()

req = urllib.request.Request('https://hub-master-production.up.railway.app/api/admin/upload-image', data=data, headers={'Content-Type': b'multipart/form-data; boundary=' + boundary, 'Authorization': 'Bearer test'})

try:
    resp = urllib.request.urlopen(req)
    print(f"Image Upload: SUCCESS")
except urllib.error.HTTPError as e:
    print(f"Image Upload: HTTP Error {e.code}")
except Exception as e:
    print(f"Image Upload: Other Error {e}")
