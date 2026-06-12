import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

old_dots_html = r'''            <!-- Pagination Dots -->
            <div class="ma-slides-nav" style="display: flex; align-items: center; margin-bottom: 24px;">
              <button class="carousel-btn-arrow prev-btn" onclick="prevMaSlide()" style="width: 36px; height: 36px; margin-right: 4px;">‹</button>
              <div class="ma-slides-dots" style="margin: 0 16px;">
                <span class="ma-dot active" onclick="setMaSlide(0)"></span>
                <span class="ma-dot" onclick="setMaSlide(1)"></span>
                <span class="ma-dot" onclick="setMaSlide(2)"></span>
                <span class="ma-dot" onclick="setMaSlide(3)"></span>
              </div>
              <button class="carousel-btn-arrow next-btn" onclick="nextMaSlide()" style="width: 36px; height: 36px; margin-left: 4px;">›</button>
            </div>'''

new_dots_html = '''            <!-- Pagination Dots -->
            <div class="ma-slides-dots">
              <span class="ma-dot active" onclick="setMaSlide(0)"></span>
              <span class="ma-dot" onclick="setMaSlide(1)"></span>
              <span class="ma-dot" onclick="setMaSlide(2)"></span>
              <span class="ma-dot" onclick="setMaSlide(3)"></span>
            </div>'''

swipe_js = '''
    // Touch swipe logic for ma-slides
    let maTouchStartX = 0;
    let maTouchEndX = 0;
    
    document.addEventListener('DOMContentLoaded', () => {
      const maCol = document.querySelector('.ma-left-col');
      if (maCol) {
        maCol.addEventListener('touchstart', e => {
          maTouchStartX = e.changedTouches[0].screenX;
        }, {passive: true});
        
        maCol.addEventListener('touchend', e => {
          maTouchEndX = e.changedTouches[0].screenX;
          if (maTouchEndX < maTouchStartX - 40) {
            if(window.nextMaSlide) window.nextMaSlide();
          }
          if (maTouchEndX > maTouchStartX + 40) {
            if(window.prevMaSlide) window.prevMaSlide();
          }
        }, {passive: true});
      }
    });
'''

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Revert HTML for dots
    content = content.replace(old_dots_html, new_dots_html)
    
    # 2. Add swipe JS at the end of the script, before </script>
    # Wait, the script has many functions. I'll just find a good place to insert it.
    # Like right after "function resetMaInterval() {" block.
    
    # Or just right before the closing tag of DOMContentLoaded
    if 'let maTouchStartX' not in content:
        insert_marker = "// Initialize text slider auto-rotation\n    document.addEventListener('DOMContentLoaded', () => {"
        replacement = swipe_js + "\n    " + insert_marker
        content = content.replace(insert_marker, replacement)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
