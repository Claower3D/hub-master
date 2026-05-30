import os
import re
import sys

# Configure stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    matches = list(re.finditer(r'initDashboard', content, re.IGNORECASE))
    print(f"Found {len(matches)} occurrences of 'initDashboard':")
    for idx, m in enumerate(matches):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 200)
        snippet = content[start:end].replace('\n', ' ')
        print(f"Occurrence {idx} at position {m.start()}: size={len(snippet)}")
        print(f"  {snippet[:150]}")
        print("-" * 50)
else:
    print("Log not found.")
