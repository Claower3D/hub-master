import os
import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

pattern = re.compile(
    r'\s*<div class="partners-category">\s*<span class="partners-label">ЗАСТРОЙЩИК</span>\s*<div class="partners-dev-card">\s*<div class="partners-dev-title">Everest Development</div>\s*<div class="partners-dev-text">[^<]+</div>\s*</div>\s*</div>'
)

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, count = pattern.subn('', content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Removed from {filepath}')
    else:
        print(f'Pattern not found in {filepath}')
