import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

downloads_dir = r"c:\Users\SystemX\Downloads"
if os.path.exists(downloads_dir):
    for item in os.listdir(downloads_dir):
        path = os.path.join(downloads_dir, item)
        if os.path.isdir(path):
            print(f"Directory: {item}")
            # List files inside this directory (only html)
            try:
                for f in os.listdir(path):
                    if f.endswith('.html') or 'hubmaster' in f.lower():
                        fpath = os.path.join(path, f)
                        size = os.path.getsize(fpath)
                        print(f"  File: {f}, Size: {size} bytes")
            except Exception as e:
                print(f"  Error reading: {e}")
else:
    print("Downloads not found.")
