import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to add mouse events to the swipe logic.
    old_js = '''    // Touch swipe logic for masters carousel
    let mastersTouchStartX = 0;
    let mastersTouchEndX = 0;
    
    document.addEventListener('DOMContentLoaded', () => {
      const mastersTrack = document.getElementById('masters-track');
      if (mastersTrack) {
        mastersTrack.addEventListener('touchstart', e => {
          mastersTouchStartX = e.changedTouches[0].screenX;
        }, {passive: true});
        
        mastersTrack.addEventListener('touchend', e => {
          mastersTouchEndX = e.changedTouches[0].screenX;
          if (mastersTouchEndX < mastersTouchStartX - 40) {
            moveCarousel(1); // swipe left -> next
          }
          if (mastersTouchEndX > mastersTouchStartX + 40) {
            moveCarousel(-1); // swipe right -> prev
          }
        }, {passive: true});
      }
    });'''
    
    new_js = '''    // Touch & Mouse swipe logic for masters carousel
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
    
    # And for the main slider:
    old_main_js = '''    // Touch swipe logic for ma-slides
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
    });'''

    new_main_js = '''    // Touch & Mouse swipe logic for ma-slides
    let maTouchStartX = 0;
    let maTouchEndX = 0;
    let isMaDragging = false;
    
    document.addEventListener('DOMContentLoaded', () => {
      const maCol = document.querySelector('.ma-left-col');
      if (maCol) {
        // Touch events
        maCol.addEventListener('touchstart', e => {
          maTouchStartX = e.changedTouches[0].screenX;
        }, {passive: true});
        
        maCol.addEventListener('touchend', e => {
          maTouchEndX = e.changedTouches[0].screenX;
          handleMaSwipe();
        }, {passive: true});

        // Mouse events
        maCol.addEventListener('mousedown', e => {
          isMaDragging = true;
          maTouchStartX = e.screenX;
        });
        
        document.addEventListener('mouseup', e => {
          if (!isMaDragging) return;
          isMaDragging = false;
          maTouchEndX = e.screenX;
          handleMaSwipe();
        });
      }
    });

    function handleMaSwipe() {
      if (maTouchEndX < maTouchStartX - 40) {
        if(window.nextMaSlide) window.nextMaSlide();
      }
      if (maTouchEndX > maTouchStartX + 40) {
        if(window.prevMaSlide) window.prevMaSlide();
      }
    }'''
    
    content = content.replace(old_js, new_js)
    content = content.replace(old_main_js, new_main_js)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
