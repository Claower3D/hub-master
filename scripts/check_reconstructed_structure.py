import os

path = "hubmaster_reconstructed.html"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx in range(300):
            line = f.readline()
            if not line:
                break
            print(f"{idx+1}: {line.strip()}")
else:
    print("File not found")
