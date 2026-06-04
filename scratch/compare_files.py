import filecmp
import os

files_to_compare = ['App.jsx', 'main.jsx', 'index.css']
for f in files_to_compare:
    root_path = os.path.join(r"c:\Users\SystemX\Downloads\1\src", f)
    front_path = os.path.join(r"c:\Users\SystemX\Downloads\1\frontend\src", f)
    
    if os.path.exists(root_path) and os.path.exists(front_path):
        are_same = filecmp.cmp(root_path, front_path, shallow=False)
        print(f"{f}: {'SAME' if are_same else 'DIFFERENT'}")
        if not are_same:
            print(f"  Root size: {os.path.getsize(root_path)}, Frontend size: {os.path.getsize(front_path)}")
    else:
        print(f"{f}: Missing one or both files")
