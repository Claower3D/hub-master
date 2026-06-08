import os

files = ["hubmaster_reconstructed.html", "hubmaster_restored.html", "extracted_html_0.html"]

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        count = content.lower().count('truncated')
        print(f"File {f}: found {count} occurrences of 'truncated'")
    else:
        print(f"File {f} does not exist")
