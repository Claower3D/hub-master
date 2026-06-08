import os

found = False
encodings = ['utf-8', 'windows-1251', 'latin-1', 'utf-16']

for root, dirs, files in os.walk(r"c:\Users\SystemX\Downloads"):
    if ".git" in root or ".gemini" in root or "node_modules" in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    content = f.read()
                if 'seo-preloader' in content:
                    print(f"Found in: {filepath} (encoding: {enc})")
                    found = True
                    break
            except Exception:
                pass

if not found:
    print("Still not found.")
