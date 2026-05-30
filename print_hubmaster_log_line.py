import os
import re

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    print("Reading log...")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            if 'Total Lines: 4' in line or 'Total Lines: 3' in line:
                print(f"Log Line {idx}: size={len(line)} chars")
                print(f"  Snippet: {line[:300]}")
                print("-" * 50)
else:
    print("Log not found.")
