import os

found = False
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(('.html', '.js', '.jsx', '.tsx', '.ts', '.go', '.json')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'seo-preloader' in content:
                    print(f"Found in: {filepath}")
                    found = True
            except Exception:
                pass

if not found:
    print("Not found in any file.")
