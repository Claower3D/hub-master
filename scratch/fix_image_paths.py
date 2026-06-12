import os
import re

files_to_update = [
    'public/index.html',
    'public/template1.html',
    'public/template2.html',
    'public/hubmaster.html',
    'hub-master/hubmaster.html'
]

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the JS bug causing the src to have /public/
    content = content.replace("'/public/hero_master.webp?v=2'", "'/hero_master.webp?v=2'")
    content = content.replace("'/public/hero_master_day.webp?v=2'", "'/hero_master_day.webp?v=2'")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filepath}")
