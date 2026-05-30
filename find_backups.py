import os

base_dir = r"C:\Users\SystemX\.gemini\antigravity"
found_dirs = []

for root, dirs, files in os.walk(base_dir):
    for d in dirs:
        if 'backup' in d.lower() or 'original' in d.lower():
            found_dirs.append(os.path.join(root, d))

print(f"Found {len(found_dirs)} folders matching 'backup' or 'original' in .gemini/antigravity:")
for p in found_dirs:
    print(p)
