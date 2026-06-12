import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

pattern112 = re.compile(
    r'\s*<div class="why-item-new">\s*<div class="why-icon-new-box"><svg viewBox="0 0 24 24">\s*<line x1="8" y1="6" x2="21" y2="6" />\s*<line x1="8" y1="12" x2="21" y2="12" />\s*<line x1="8" y1="18" x2="21" y2="18" />\s*<line x1="3" y1="6" x2="3\.01" y2="6" />\s*<line x1="3" y1="12" x2="3\.01" y2="12" />\s*<line x1="3" y1="18" x2="3\.01" y2="18" />\s*</svg></div>\s*<div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle1">112 Услуг</span><span\s*class="why-desc-new" data-i18n="whyDesc1">Широкий спектр работ</span></div>\s*</div>',
    re.DOTALL
)

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, count = pattern112.subn('', content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Removed 112 Услуг from {filepath}')
