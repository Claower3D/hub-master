import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

css_hide_arrows = '''
    @media (max-width: 768px) {
      .carousel-btn-arrow {
        display: none !important;
      }
      .masters-carousel-container {
        padding: 0;
        margin: 0 -20px; /* bleed edges */
        width: calc(100% + 40px);
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        scrollbar-width: none;
      }
      .masters-carousel-container::-webkit-scrollbar {
        display: none;
      }
      .masters-carousel-track {
        padding: 0 20px;
        transform: none !important; /* disable JS transform on mobile */
      }
      .master-card-new {
        scroll-snap-align: start;
      }
    }
'''

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'bleed edges' not in content:
        insert_marker_css = ".masters-carousel-wrap {"
        content = content.replace(insert_marker_css, css_hide_arrows + "\n    " + insert_marker_css)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
