import os

log_dir = r"C:\Users\SystemX\.gemini\antigravity\brain\9aa48c27-5e79-4ce6-9c15-f61b17b52430"
found = []

for root, dirs, files in os.walk(log_dir):
    for f in files:
        path = os.path.join(root, f)
        size = os.path.getsize(path)
        found.append((path, size))

print(f"Total files: {len(found)}")
for p, s in sorted(found, key=lambda x: x[1], reverse=True):
    print(f"Path: {p}, Size: {s} bytes")
