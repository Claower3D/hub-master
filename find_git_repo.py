import os

path = r"c:\Users\SystemX\Downloads\1"
found = False

while True:
    git_dir = os.path.join(path, ".git")
    if os.path.exists(git_dir) and os.path.isdir(git_dir):
        print(f"Found .git repository at: {path}")
        found = True
        break
    parent = os.path.dirname(path)
    if parent == path:
        break
    path = parent

if not found:
    print("No git repository found in workspace or parent directories.")
