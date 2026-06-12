import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

pattern_chestnye = re.compile(
    r'\s*<div class="why-card">\s*<div class="why-icon">\s*<svg viewBox="0 0 24 24" stroke="none" fill="currentColor">\s*<polygon\s*points="12 2 15\.09 8\.26 22 9\.27 17 14\.14 18\.18 21\.02 12 17\.77 5\.82 21\.02 7 14\.14 2 9\.27 8\.91 8\.26 12 2" />\s*</svg>\s*</div>\s*<h4 class="why-title" data-i18n="why4">Честные цены</h4>\s*<p class="why-desc" data-i18n="why4Desc">Рассчитываем стоимость до начала работ\. Никаких скрытых платежей\.\s*</p>\s*</div>',
    re.DOTALL
)

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, count = pattern_chestnye.subn('', content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Removed Честные цены from {filepath}')
