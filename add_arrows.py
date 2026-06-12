import os

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

old_dots = '''            <!-- Pagination Dots -->
            <div class="ma-slides-dots">
              <span class="ma-dot active" onclick="setMaSlide(0)"></span>
              <span class="ma-dot" onclick="setMaSlide(1)"></span>
              <span class="ma-dot" onclick="setMaSlide(2)"></span>
              <span class="ma-dot" onclick="setMaSlide(3)"></span>
            </div>'''

new_dots = '''            <!-- Pagination Dots -->
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

old_js = '''    function nextMaSlide() {
      const maSlides = document.querySelectorAll('.ma-slide');
      if (maSlides.length === 0) return;
      let next = (currentMaSlide + 1) % maSlides.length;
      window.setMaSlide(next);
    }'''

new_js = '''    window.nextMaSlide = function() {
      const maSlides = document.querySelectorAll('.ma-slide');
      if (maSlides.length === 0) return;
      let next = (currentMaSlide + 1) % maSlides.length;
      window.setMaSlide(next);
    }

    window.prevMaSlide = function() {
      const maSlides = document.querySelectorAll('.ma-slide');
      if (maSlides.length === 0) return;
      let prev = (currentMaSlide - 1 + maSlides.length) % maSlides.length;
      window.setMaSlide(prev);
    }'''

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. replace html
    content = content.replace(old_dots, new_dots)
    
    # 2. replace JS
    content = content.replace(old_js, new_js)
    content = content.replace('setInterval(nextMaSlide, 6000)', 'setInterval(window.nextMaSlide, 6000)')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
