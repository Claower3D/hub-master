import os

brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"
matches = []

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f.endswith(('.txt', '.html', '.log', '.json')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if 'initherotimeline' in content.lower():
                        matches.append((path, len(content)))
            except:
                pass

print(f"Found {len(matches)} files containing 'initHeroTimeline':")
for m in matches:
    print(f"Path: {m[0]}, Size: {m[1]} bytes")
