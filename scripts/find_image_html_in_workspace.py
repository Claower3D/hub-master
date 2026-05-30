import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\SystemX\Downloads\1"
search_terms = ["вызвать мебельщика", "оставить заявку на сервис", "перетяжка", "hvac", "сборка мебели"]
matches = []

for root, dirs, files in os.walk(workspace_dir):
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    if 'dist' in dirs:
        dirs.remove('dist')
    for f in files:
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                for term in search_terms:
                    if term in content.lower():
                        matches.append((path, term, len(content)))
                        break
        except:
            pass

print(f"Found {len(matches)} files in workspace containing search terms:")
for m in matches:
    print(f"  Path: {m[0]}, Term: '{m[1]}', Size: {m[2]} bytes")
