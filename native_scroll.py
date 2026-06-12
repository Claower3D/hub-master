import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update moveCarousel to use scrollBy
    old_moveCarousel = '''    function moveCarousel(direction) {
      const track = document.getElementById('masters-track');
      if (!track) return;

      const filtered = selectedMastersCategory === 'all' 
        ? mastersData 
        : mastersData.filter(m => m.category === selectedMastersCategory);

      const cardWidth = 232; // card flex width (220) + gap (12)
      const maxOffset = Math.max(0, filtered.length - 2);

      currentCarouselOffset += direction;
      if (currentCarouselOffset < 0) currentCarouselOffset = 0;
      if (currentCarouselOffset > maxOffset) currentCarouselOffset = maxOffset;

      track.style.transform = `translateX(-${currentCarouselOffset * cardWidth}px)`;
    }'''

    new_moveCarousel = '''    function moveCarousel(direction) {
      const container = document.querySelector('.masters-carousel-container');
      if (!container) return;
      
      const cardWidth = 232; // card flex width (220) + gap (12)
      container.scrollBy({ left: direction * cardWidth, behavior: 'smooth' });
    }'''

    content = content.replace(old_moveCarousel, new_moveCarousel)
    
    # 2. Add global CSS for native scrollbar
    css_native_scroll = '''
    .masters-carousel-container {
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      scrollbar-width: none; /* Firefox */
      -ms-overflow-style: none; /* IE/Edge */
      scroll-behavior: smooth;
    }
    .masters-carousel-container::-webkit-scrollbar {
      display: none; /* Chrome/Safari */
    }
    .master-card-new {
      scroll-snap-align: start;
    }
'''
    if 'scrollbar-width: none;' not in content:
        insert_marker_css = ".masters-carousel-wrap {"
        content = content.replace(insert_marker_css, css_native_scroll + "\n    " + insert_marker_css)
    else:
        # if it's already there (maybe from a previous commit), let's ensure it's not restricted to @media
        # Actually in the previous commit I replaced it with just display:none for arrows.
        # Let's just insert it.
        if '.masters-carousel-container {' not in content:
            insert_marker_css = ".masters-carousel-wrap {"
            content = content.replace(insert_marker_css, css_native_scroll + "\n    " + insert_marker_css)

    # 3. Remove custom mouse/touch JS for mastersTrack
    old_masters_js = '''    // Touch & Mouse swipe logic for masters carousel
    let mastersTouchStartX = 0;
    let mastersTouchEndX = 0;
    let isMastersDragging = false;
    
    document.addEventListener('DOMContentLoaded', () => {
      const mastersTrack = document.getElementById('masters-track');
      if (mastersTrack) {
        // Touch events
        mastersTrack.addEventListener('touchstart', e => {
          mastersTouchStartX = e.changedTouches[0].screenX;
        }, {passive: true});
        
        mastersTrack.addEventListener('touchend', e => {
          mastersTouchEndX = e.changedTouches[0].screenX;
          handleMastersSwipe();
        }, {passive: true});

        // Mouse events
        mastersTrack.addEventListener('mousedown', e => {
          isMastersDragging = true;
          mastersTouchStartX = e.screenX;
        });
        
        document.addEventListener('mouseup', e => {
          if (!isMastersDragging) return;
          isMastersDragging = false;
          mastersTouchEndX = e.screenX;
          handleMastersSwipe();
        });
      }
    });

    function handleMastersSwipe() {
      if (mastersTouchEndX < mastersTouchStartX - 40) {
        moveCarousel(1); // swipe left -> next
      }
      if (mastersTouchEndX > mastersTouchStartX + 40) {
        moveCarousel(-1); // swipe right -> prev
      }
    }'''
    
    content = content.replace(old_masters_js, '')
    
    # 4. Remove `track.style.transform = '';` and `currentCarouselOffset = 0;` from `renderMastersCarousel` 
    # Because now it's managed by native scroll.
    # We should scroll container to left=0 on render.
    content = content.replace(
        "track.style.transform = `translateX(0px)`;\n      currentCarouselOffset = 0;",
        "const container = document.querySelector('.masters-carousel-container');\n      if(container) container.scrollTo({left: 0});"
    )
    content = content.replace(
        "track.style.transform = '';",
        "const container = document.querySelector('.masters-carousel-container');\n      if(container) container.scrollTo({left: 0});"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
