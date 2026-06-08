import re
import json
import os

log_paths = [
    r"C:\Users\SystemX\.gemini\antigravity\brain\9aa48c27-5e79-4ce6-9c15-f61b17b52430\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\afb57b92-f46a-4fb8-b8d0-13a2e13ea3d7\.system_generated\logs\overview.txt"
]

candidates = []

for log_path in log_paths:
    if not os.path.exists(log_path):
        continue
    print(f"Reading log: {log_path}")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Let's find occurrences of HTML structures in logs.
    # Look for patterns that look like full HTML content
    for m in re.finditer(r"<!DOCTYPE html>", text, re.IGNORECASE):
        start = m.start()
        end_m = text.find("</html>", start)
        if end_m != -1:
            end = end_m + len("</html>")
            content = text[start:end]
            # Clean up escape sequences if any
            cleaned = content.replace(r'\n', '\n').replace(r'\"', '"').replace(r'\/', '/').replace(r'\\', '\\')
            
            # Filter by size to find large monolithic ones
            if len(cleaned) > 70000:
                candidates.append((log_path, start, len(cleaned), cleaned))

print(f"Found {len(candidates)} candidates.")
for i, (path, pos, length, content) in enumerate(candidates):
    # check first 200 chars and last 200 chars
    print(f"Candidate {i}: Path={os.path.basename(os.path.dirname(os.path.dirname(path)))}, Pos={pos}, Length={length}")
    # Write to a file
    filename = f"candidate_hubmaster_{i}.html"
    with open(filename, 'w', encoding='utf-8') as out:
        out.write(content)
    print(f"  Saved to {filename}")
