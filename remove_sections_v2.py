import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

# Regex to match <!-- Steps --> up to its closing </div> which is followed by </div> (of showcase-bottom)
# But only capturing the showcase-steps part.
pattern_steps = re.compile(
    r'\s*<!-- Steps -->\s*<div class="showcase-steps">.*?<div class="step-circle">4</div>\s*<div class="step-text">Готово!</div>\s*</div>\s*</div>',
    re.DOTALL
)

pattern_why = re.compile(
    r'\s*<!-- WHY CHOOSE US -->\s*<section class="why-section" id="why-choose">.*?</section>',
    re.DOTALL
)

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    c1, count_steps = pattern_steps.subn('', content)
    c2, count_why = pattern_why.subn('', c1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'Patched {filepath} (steps: {count_steps}, why: {count_why})')
