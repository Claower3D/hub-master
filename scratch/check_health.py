import urllib.request
import json

try:
    with urllib.request.urlopen("https://master-hub-production.up.railway.app/api/health") as response:
        data = response.read().decode('utf-8')
        print(f"Health Response: {data}")
except Exception as e:
    print(f"Error: {e}")
