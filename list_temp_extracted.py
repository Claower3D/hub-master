import os

temp_dir = r"c:\Users\SystemX\Downloads\temp_extracted"
found = []

if os.path.exists(temp_dir):
    for root, dirs, files in os.walk(temp_dir):
        for f in files:
            found.append(os.path.join(root, f))

print(f"Total files in temp_extracted: {len(found)}")
for f in found[:30]:
    print(f, os.path.getsize(f))
