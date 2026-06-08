import os

downloads_dir = r"c:\Users\SystemX\Downloads"
if os.path.exists(downloads_dir):
    subdirs = [d for d in os.listdir(downloads_dir) if os.path.isdir(os.path.join(downloads_dir, d))]
    print("Downloads subdirectories:", subdirs)
else:
    print("Downloads directory not found.")
