import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    idx = content.rfind("КАЧЕСТВЕННАЯ СБОРКА")
    if idx != -1:
        print(f"Found 'КАЧЕСТВЕННАЯ СБОРКА' at {idx}. Printing context:")
        # Let's print from idx-1000 to idx+3000
        print(content[idx-1000:idx+3500])
    else:
        print("Not found.")
else:
    print("overview.txt not found.")
