import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"
search_terms = ["вызвать мебельщика", "сборка кухонь", "оставить заявку на сервис", "перетяжка"]
matches = []

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f.endswith(('.txt', '.html', '.log', '.json')):
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

print(f"Found {len(matches)} files containing search terms:")
for m in matches:
    print(f"Path: {m[0]}, Term: '{m[1]}', Size: {m[2]} bytes")
