import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\scratch"

if os.path.exists(scratch_dir):
    files = os.listdir(scratch_dir)
    print(f"Scratch files: {files}")
    for file in files:
        path = os.path.join(scratch_dir, file)
        if os.path.isfile(path) and path.endswith('.txt'):
            print(f"\nSearching in {file}...")
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Look for lines containing CSS selector for master-card
            matches = [m.start() for m in re.finditer(r'\.master-card', content)] if 're' in sys.modules else []
            # Or manually search
            import re
            matches = [m.start() for m in re.finditer(r'\.master-card', content)]
            print(f"Found .master-card at {len(matches)} places.")
            for idx in matches:
                print(content[idx-100:idx+800])
                print("="*40)
else:
    print("Scratch dir not found.")
