import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    print("Searching for code blocks in previous session logs...")
    # Find all code blocks that start with ```css or ```html or ```js or ```javascript
    # Or simply let's find the last occurrences of edits.
    # We can search for the term "apply_consolidated_hero.py" or see what files were edited.
    # Wait, in 95fdbd5f, the user was editing hubmaster.html.
    # Let's search for "replace_file_content" or "write_to_file" calls in the logs.
    pattern = r'replace_file_content.*?ReplacementContent\\":\\"(.*?)\\"'
    matches = re.findall(pattern, content, re.DOTALL)
    print(f"Found {len(matches)} replacement matches.")
    
    # Let's also print code blocks that look like style blocks.
    style_matches = [m.start() for m in re.finditer(r'\.hero-container-consolidated', content)]
    print(f"Found .hero-container-consolidated at indices: {style_matches}")
    for idx in style_matches[-2:]:
        print(f"--- Context at {idx} ---")
        print(content[idx-100:idx+1500])
        print("="*60)
        
    # Let's also search for the HTML structure by searching for "class=\"hero-container-consolidated\""
    html_matches = [m.start() for m in re.finditer(r'class="hero-container-consolidated"', content)]
    print(f"Found class=\"hero-container-consolidated\" at indices: {html_matches}")
    for idx in html_matches[-2:]:
        print(f"--- Context at {idx} ---")
        print(content[idx-50:idx+1500])
        print("="*60)
else:
    print("overview.txt not found.")
