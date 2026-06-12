import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

swipe_masters_js = '''
    // Touch swipe logic for masters carousel
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
    });
'''

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
    
    # 1. Add css
    if 'scroll-snap-type: x mandatory;' not in content:
        content = content.replace('</style>', css_hide_arrows + '\n  </style>')
    
    # 2. Add JS
    if 'let mastersTouchStartX = 0;' not in content:
        insert_marker = "// Initialize text slider auto-rotation"
        content = content.replace(insert_marker, swipe_masters_js + "\n    " + insert_marker)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
