import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\SystemX\Downloads\1\hubmaster.html"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    print(f"Total lines: {len(lines)}")
    found = []
    for idx, line in enumerate(lines):
        if 'hero-container' in line or 'category-grid' in line:
            found.append((idx+1, line.strip()))
            
    print("Found occurrences:")
    for f in found:
        print(f"Line {f[0]}: {f[1]}")
else:
    print("hubmaster.html not found.")
