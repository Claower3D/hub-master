import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace the complex CSS with just the display none
    old_css = '''    @media (max-width: 768px) {
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
    }'''
    
    new_css = '''    @media (max-width: 768px) {
      .carousel-btn-arrow {
        display: none !important;
      }
    }'''
    
    # Also we want to add mouse drag support just in case!
    # Because if they test on desktop with a mouse it won't work with just touch events.
    # But wait, it's easier to just use standard touch events if it's on a real phone.
    
    content = content.replace(old_css, new_css)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
