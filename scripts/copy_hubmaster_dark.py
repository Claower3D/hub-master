import os

src_path = r"C:\Users\SystemX\Downloads\hubmaster_dark.html"
dst_path = "downloads_hubmaster_dark_copy.html"

if os.path.exists(src_path):
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    with open(dst_path, 'w', encoding='utf-8') as out:
        out.write(content)
    print(f"Copied to {dst_path}")
else:
    print("Source hubmaster_dark.html does not exist")
