import os

base_dir = r"C:\Users\SystemX\Downloads"
for entry in os.listdir(base_dir):
    full_path = os.path.join(base_dir, entry)
    if os.path.isdir(full_path):
        print(f"Dir: {entry} -> unicode: {entry.encode('unicode_escape').decode('utf-8')}")
        # check if it has html files
        html_files = [f for f in os.listdir(full_path) if f.endswith('.html')]
        if html_files:
            print(f"  HTML files: {html_files}")
