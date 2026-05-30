import os

brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"
found = []

for entry in os.listdir(brain_dir):
    c_path = os.path.join(brain_dir, entry)
    if os.path.isdir(c_path):
        scratch_path = os.path.join(c_path, "scratch")
        if os.path.exists(scratch_path) and os.path.isdir(scratch_path):
            for root, dirs, files in os.walk(scratch_path):
                for f in files:
                    if f.endswith(('.html', '.js', '.jsx', '.css', '.json', '.txt')):
                        path = os.path.join(root, f)
                        try:
                            size = os.path.getsize(path)
                            found.append((path, size))
                        except:
                            pass

print(f"Total scratch files: {len(found)}")
for p, s in sorted(found, key=lambda x: x[1], reverse=True):
    # Only print files larger than 1KB to keep output clean
    if s > 1000:
        print(f"Path: {p}, Size: {s} bytes")
