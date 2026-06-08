import os
import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\9aa48c27-5e79-4ce6-9c15-f61b17b52430\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    print("Reading log...")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            if 'hubmaster.html' in line:
                print(f"Log Line {idx}: size={len(line)} chars")
                # Print first 200 chars
                print(f"  Snippet: {line[:200]}")
else:
    print("Log not found.")
