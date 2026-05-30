import os

base_dir = r"C:\Users\SystemX\.gemini\antigravity"
found = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(('.jsx', '.js', '.css')) and not 'node_modules' in root:
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            found.append((path, size))

print(f"Found {len(found)} code files in AppData:")
for p, s in found:
    print(f"Path: {p}, Size: {s} bytes")
