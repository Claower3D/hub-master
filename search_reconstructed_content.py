import os

path = "extracted_html_0.html"
queries = ["hero", "dashboard", "style", "div", "master"]

if os.path.exists(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    print(f"Total lines in {path}: {len(lines)}")
    for q in queries:
        matches = [idx + 1 for idx, l in enumerate(lines) if q in l.lower()]
        print(f"Query '{q}': found {len(matches)} matches. First 5 line numbers: {matches[:5]}")
        if matches:
            print(f"  Example line {matches[0]}: {repr(lines[matches[0]-1][:120])}")
else:
    print(f"{path} does not exist")
