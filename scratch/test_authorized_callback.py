import urllib.request
import json

# 1. Login
login_url = "https://master-hub-production.up.railway.app/api/auth/login"
login_payload = {
    "email": "admin@masterhub.kz",
    "password": "admin123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    req = urllib.request.Request(
        login_url,
        data=json.dumps(login_payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        login_res = json.loads(response.read().decode('utf-8'))
        token = login_res.get("token")
        print(f"Logged in successfully. Token: {token[:15]}...")
        
    # 2. Submit callback with token
    callback_url = "https://master-hub-production.up.railway.app/api/callback"
    callback_payload = {
        "name": "Азамат Авторизованный",
        "phone": "+7 (705) 846-2749",
        "service": "Ремонт стиральных машин",
        "city": "Алматы",
        "comment": "Тестовая заявка от авторизованного пользователя"
    }
    
    headers["Authorization"] = f"Bearer {token}"
    req_cb = urllib.request.Request(
        callback_url,
        data=json.dumps(callback_payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req_cb) as response_cb:
        cb_res = json.loads(response_cb.read().decode('utf-8'))
        print("Callback Submission Status Code: 200")
        print(f"Callback Submission Response: {json.dumps(cb_res)}")
        
except Exception as e:
    print(f"Error occurred: {e}")
