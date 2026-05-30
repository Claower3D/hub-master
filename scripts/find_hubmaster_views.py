import re
import json
import os

log_paths = [
    r"C:\Users\SystemX\.gemini\antigravity\brain\9aa48c27-5e79-4ce6-9c15-f61b17b52430\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\afb57b92-f46a-4fb8-b8d0-13a2e13ea3d7\.system_generated\logs\overview.txt"
]

for log_path in log_paths:
    if not os.path.exists(log_path):
        continue
    print(f"Searching in: {log_path}")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Let's search for "Total Lines: 4282" or similar
    for m in re.finditer(r"Total Lines:\s*(\d+)", content):
        line_count = int(m.group(1))
        # let's look at the surrounding text
        start_idx = max(0, m.start() - 200)
        end_idx = min(len(content), m.end() + 200)
        print(f"Found 'Total Lines: {line_count}' in log! Context:")
        print(content[start_idx:end_idx])
        print("="*80)
