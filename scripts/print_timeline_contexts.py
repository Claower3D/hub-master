import os
import re

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for idx, m in enumerate(re.finditer(r'initHeroTimeline', content, re.IGNORECASE)):
        start = max(0, m.start() - 1000)
        end = min(len(content), m.end() + 1000)
        print(f"Occurrence {idx} at position {m.start()}:")
        print(content[start:end])
        print("=" * 85)
else:
    print("Log not found.")
