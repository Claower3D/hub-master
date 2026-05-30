import os

recycle_bin = r"C:\$Recycle.Bin"
found = []

if os.path.exists(recycle_bin):
    try:
        for root, dirs, files in os.walk(recycle_bin):
            for f in files:
                if 'hubmaster' in f.lower() or 'index' in f.lower():
                    path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(path)
                        found.append((path, size))
                    except:
                        pass
    except Exception as e:
        print(f"Error accessing Recycle Bin: {e}")
else:
    print("Recycle Bin does not exist or cannot be accessed.")

print(f"Found {len(found)} candidate files in Recycle Bin:")
for p, s in found:
    print(f"Path: {p}, Size: {s} bytes")
