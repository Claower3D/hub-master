import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

pattern_steps = re.compile(
    r'\s*<!-- Steps -->\s*<div class="showcase-steps">.*?</div>\s*</div>',
    re.DOTALL
)

pattern_why = re.compile(
    r'\s*<!-- WHY CHOOSE US -->\s*<section class="why-section" id="why-choose">.*?</section>',
    re.DOTALL
)

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove showcase-steps
    # It starts with <!-- Steps --> and ends after </div> </div>
    # Let's find exactly:
    start_steps = content.find('<!-- Steps -->')
    if start_steps != -1:
        # find the end of showcase-steps which is just before </div>\n      </div>\n    </section>
        end_steps = content.find('</section>', start_steps)
        if end_steps != -1:
            # We want to remove the showcase-steps block.
            # showcase-steps is a direct child of showcase-bottom. Wait, let's look at the structure.
            # <div class="showcase-bottom">
            #   <div class="showcase-stats-row"> ... </div>
            #   <div class="showcase-steps"> ... </div>
            # </div>
            # So if we remove showcase-steps, we must leave showcase-stats-row and showcase-bottom intact.
            pass

    # Better to use regex for showcase-steps:
    c1, count_steps = pattern_steps.subn('', content)
    c2, count_why = pattern_why.subn('', c1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'Patched {filepath} (steps: {count_steps}, why: {count_why})')
