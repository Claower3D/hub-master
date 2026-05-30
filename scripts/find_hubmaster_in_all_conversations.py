import os

brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"
matches = []

for root, dirnames, filenames in os.walk(brain_dir):
    for filename in filenames:
        path = os.path.join(root, filename)
        try:
            size = os.path.getsize(path)
            if size > 10000 and size < 10000000:
                if filename.endswith(('.txt', '.json', '.html', '.log')):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'hubmaster' in content.lower() or 'hub master' in content.lower():
                            matches.append((path, size))
        except Exception as e:
            pass

print(f"Found {len(matches)} potential candidate files:")
for m in matches:
    print(f"Path: {m[0]}, Size: {m[1]} bytes")
