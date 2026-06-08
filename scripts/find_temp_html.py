import os

recycle_bin = r"C:\$Recycle.Bin"
found = []

if os.path.exists(recycle_bin):
    try:
        for root, dirs, files in os.walk(recycle_bin):
            for f in files:
                if f.lower().endswith('.html'):
                    path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(path)
                        if 100000 <= size <= 160000:
                            found.append((path, size))
                    except:
                        pass
    except Exception as e:
        print(f"Error accessing Recycle Bin: {e}")
else:
    print("Recycle Bin does not exist.")

print(f"Found {len(found)} HTML files in Recycle Bin between 100KB and 160KB:")
for p, s in found:
    print(f"Path: {p}, Size: {s} bytes")
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as file:
            first_lines = [file.readline().strip() for _ in range(10)]
            print(f"  First lines: {first_lines}")
    except Exception as e:
        print(f"  Error reading: {e}")
    print("-" * 50)
