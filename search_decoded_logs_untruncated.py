import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\scratch\decoded_logs.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    print(f"Loaded decoded_logs.txt, size: {len(content)}")
    import re
    matches = [m.start() for m in re.finditer(r'ПЕРЕТЯЖКА|HVAC|PLUMBING', content, re.IGNORECASE)]
    print(f"Matches found: {len(matches)}")
    for idx in matches:
        print(f"--- Occurrence at {idx} ---")
        print(content[idx-200:idx+800])
        print("="*60)
else:
    print("decoded_logs.txt not found.")
