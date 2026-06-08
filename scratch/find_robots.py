import os

for root, dirs, files in os.walk(r"c:\Users\SystemX\Downloads\1"):
    if ".git" in root or "node_modules" in root:
        continue
    for file in files:
        if file.lower() == "robots.txt":
            print(f"Found robots.txt at: {os.path.join(root, file)}")
