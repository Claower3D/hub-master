import os
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

cwd = r"c:\Users\SystemX\Downloads\1"
pre_session_files = []

# Our session started around 2026-05-29 09:24:00 local time
session_start_time = time.mktime(time.strptime("2026-05-29 09:24:00", "%Y-%m-%d %H:%M:%S"))

for root, dirs, files in os.walk(cwd):
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    if 'dist' in dirs:
        dirs.remove('dist')
    for f in files:
        path = os.path.join(root, f)
        try:
            mtime = os.path.getmtime(path)
            if mtime < session_start_time:
                size = os.path.getsize(path)
                pre_session_files.append((path, mtime, size))
        except:
            pass

pre_session_files.sort(key=lambda x: x[1], reverse=True)

print("Files modified right before this session:")
for path, mtime, size in pre_session_files[:15]:
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    print(f"Path: {path}")
    print(f"  MTime: {formatted_time}, Size: {size} bytes")
