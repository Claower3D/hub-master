import os

paths_to_search = [
    r"C:\Users\SystemX\Downloads",
    r"C:\Users\SystemX\Desktop"
]

found = []

for base in paths_to_search:
    if os.path.exists(base):
        print(f"Scanning: {base}")
        for root, dirs, files in os.walk(base):
            # Exclude node_modules to avoid scanning too many files
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            if 'dist' in dirs:
                dirs.remove('dist')
            for f in files:
                if 'hubmaster' in f.lower() and f.endswith('.html'):
                    path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(path)
                        found.append((path, size))
                    except:
                        pass

print(f"Found {len(found)} hubmaster html files:")
for p, s in found:
    print(f"Path: {p}, Size: {s} bytes")
