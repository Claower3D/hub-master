import os

paths = [
    r"c:\Users\SystemX\Downloads\1\src",
    r"c:\Users\SystemX\Downloads\1\public"
]

found = []
for p in paths:
    if os.path.exists(p):
        for root, dirs, files in os.walk(p):
            for f in files:
                found.append(os.path.join(root, f))

print(f"Found {len(found)} files in src and public:")
for f in found:
    print(f, os.path.getsize(f))
