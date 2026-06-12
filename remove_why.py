import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove block 1: <!-- Why Choose Us -->
    # It starts with:           <!-- Why Choose Us -->
    # It ends with:           </div> (of why-choose-block)
    # The container closes with:
    #         </div>
    #       </div>
    #     </section>
    
    # We can match from "<!-- Why Choose Us -->" up to "</div>\n        </div>\n      </div>\n    </section>"
    # Wait, the closing tags are:
    # 6338:           </div>
    # 6339: 
    # 6340:         </div>
    # 6341:       </div>
    # 6342:     </section>
    
    # So we want to remove everything from <!-- Why Choose Us --> up to the closing tags
    
    pattern1 = re.compile(r'\s*<!-- Why Choose Us -->\s*<div class="ma-block why-choose-block".*?</div>\s*</div>\s*(?=</div>\s*</div>\s*</section>)', re.DOTALL)
    
    # Wait, the structure is:
    #           <!-- Why Choose Us -->
    #           <div class="ma-block why-choose-block" style="width:100%;">
    #             ...
    #             <div class="why-grid-3x3">
    #               ...
    #             </div>
    #           </div>
    
    pattern1 = re.compile(r'\s*<!-- Why Choose Us -->\s*<div class="ma-block why-choose-block".*?(?=</div>\s*</div>\s*</section>\s*<!-- SHOWCASE COMBO -->)', re.DOTALL)
    
    # For the second block:
    pattern2 = re.compile(r'\s*<!-- WHY CHOOSE US -->\s*<section class="why-section" id="why-choose">.*?</section>', re.DOTALL)
    
    c1, count1 = pattern1.subn('', content)
    c2, count2 = pattern2.subn('', c1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'Patched {filepath} (p1: {count1}, p2: {count2})')
