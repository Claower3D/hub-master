import urllib.request
import json

url = "https://master-hub-production.up.railway.app/api/callback"
payload = {
    "name": "Азамат Тест",
    "phone": "+7 (705) 846-2749",
    "service": "Общая заявка",
    "city": "Алматы",
    "comment": "Заказ через модальное окно на услугу: Общая заявка"
}

headers = {
    "Content-Type": "application/json"
}

try:
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        status_code = response.status
        body = response.read().decode('utf-8')
        print(f"Status Code: {status_code}")
        print(f"Response: {body}")
except Exception as e:
    print(f"Error: {e}")
