import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for filename in ["candidate_hubmaster_0.html", "candidate_hubmaster_1.html"]:
    path = os.path.join(r"c:\Users\SystemX\Downloads\1", filename)
    if os.path.exists(path):
        print(f"=== File: {filename} ===")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Search for "вызвать мебельщика"
        idx = content.lower().find("вызвать мебельщика")
        if idx != -1:
            print(f"Found 'вызвать мебельщика' at index {idx}. Extracting context:")
            start = max(0, idx - 1000)
            end = min(len(content), idx + 2500)
            print(content[start:end])
        else:
            print("Not found.")
        print("=" * 60)
