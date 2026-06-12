import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

old_container_css = '''    .masters-carousel-container {
      overflow: hidden;
      width: 100%;
      padding: 2px;
    }'''

new_container_css = '''    .masters-carousel-container {
      overflow-x: auto;
      overflow-y: hidden;
      width: 100%;
      padding: 2px;
      scroll-snap-type: x mandatory;
      scrollbar-width: none; /* Firefox */
      -ms-overflow-style: none; /* IE/Edge */
      scroll-behavior: smooth;
      /* Improve touch handling */
      -webkit-overflow-scrolling: touch;
    }
    .masters-carousel-container::-webkit-scrollbar {
      display: none; /* Chrome/Safari */
    }'''

old_card_css = '''    .master-card-new {
      flex: 0 0 220px;
      background: rgba(25, 25, 29, 0.55);'''

new_card_css = '''    .master-card-new {
      flex: 0 0 220px;
      background: rgba(25, 25, 29, 0.55);
      scroll-snap-align: start;'''

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(old_container_css, new_container_css)
    content = content.replace(old_card_css, new_card_css)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
