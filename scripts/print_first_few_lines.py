import os

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx in range(10):
            line = f.readline()
            if not line:
                break
            print(f"Line {idx+1}: size={len(line)} chars")
            print(f"  {line[:150]}")
            print("-" * 50)
else:
    print("Log not found.")
