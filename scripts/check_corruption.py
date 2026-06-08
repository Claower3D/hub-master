import os
import time

for path in ["hubmaster.html", "index.html"]:
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print(f"{path}: MTime={formatted_time}, Size={os.path.getsize(path)} bytes")
    else:
        print(f"{path} does not exist.")
