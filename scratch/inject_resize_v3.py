import re

with open('public/builder.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for resize overlay
css_to_add = """
          .builder-resize-overlay {
            position: absolute;
            border: 2px dashed #10b981;
            pointer-events: none;
            display: none;
            z-index: 100000;
          }
          .resize-handle {
            position: absolute;
            width: 14px; height: 14px;
            background: #10b981;
            border: 2px solid #fff;
            pointer-events: auto;
            border-radius: 50%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
          }
          .resize-handle.top-left { top: -7px; left: -7px; cursor: nwse-resize; }
          .resize-handle.top-right { top: -7px; right: -7px; cursor: nesw-resize; }
          .resize-handle.bottom-left { bottom: -7px; left: -7px; cursor: nesw-resize; }
          .resize-handle.bottom-right { bottom: -7px; right: -7px; cursor: nwse-resize; }
"""
content = content.replace('.builder-add-divider {', css_to_add + '\n          .builder-add-divider {')


# 2. Add resize variables after clickStart = 0;
js_vars = """
        let clickStart = 0;

        // RESIZE OVERLAY
        const resizeOverlay = doc.createElement('div');
        resizeOverlay.className = 'builder-resize-overlay';
        resizeOverlay.innerHTML = `
           <div class="resize-handle top-left" data-dir="tl"></div>
           <div class="resize-handle top-right" data-dir="tr"></div>
           <div class="resize-handle bottom-left" data-dir="bl"></div>
           <div class="resize-handle bottom-right" data-dir="br"></div>
        `;
        doc.body.appendChild(resizeOverlay);

        let isResizing = false;
        let activeResizeEl = null;
        let resizeDir = '';
        let startWidth = 0;
        let startHeight = 0;
"""
content = content.replace('let clickStart = 0;', js_vars)


# 3. Modify mousedown
old_mousedown = """doc.addEventListener('mousedown', (e) => {
          const editable = e.target.closest('.builder-inline-editable');
          if (editable) {
            dragEl = editable;
            isDragging = false;
            startMouseX = e.clientX;
            startMouseY = e.clientY;
            clickStart = Date.now();
            
            const comp = window.getComputedStyle(dragEl);
            if (comp.position === 'static') {
              dragEl.style.position = 'relative';
            }
            startLeft = parseFloat(dragEl.style.left) || 0;
            startTop = parseFloat(dragEl.style.top) || 0;
          }
        }, true);"""

new_mousedown = """doc.addEventListener('mousedown', (e) => {
          if (e.target.classList.contains('resize-handle')) {
             isResizing = true;
             resizeDir = e.target.getAttribute('data-dir');
             startMouseX = e.clientX;
             startMouseY = e.clientY;
             if (activeResizeEl) {
                 startWidth = activeResizeEl.offsetWidth;
                 startHeight = activeResizeEl.offsetHeight;
                 isDragging = false;
                 dragEl = null;
             }
             e.preventDefault();
             e.stopPropagation();
             return;
          }

          const editable = e.target.closest('.builder-inline-editable');
          if (editable) {
            activeResizeEl = editable;
            const rect = editable.getBoundingClientRect();
            resizeOverlay.style.display = 'block';
            resizeOverlay.style.width = rect.width + 'px';
            resizeOverlay.style.height = rect.height + 'px';
            resizeOverlay.style.top = (rect.top + doc.defaultView.scrollY) + 'px';
            resizeOverlay.style.left = (rect.left + doc.defaultView.scrollX) + 'px';

            dragEl = editable;
            isDragging = false;
            startMouseX = e.clientX;
            startMouseY = e.clientY;
            clickStart = Date.now();
            
            const comp = window.getComputedStyle(dragEl);
            if (comp.position === 'static') {
              dragEl.style.position = 'relative';
            }
            startLeft = parseFloat(dragEl.style.left) || 0;
            startTop = parseFloat(dragEl.style.top) || 0;
          } else if (!e.target.closest('.builder-resize-overlay') && !e.target.closest('.builder-section-toolbar')) {
             resizeOverlay.style.display = 'none';
             activeResizeEl = null;
          }
        }, true);"""

content = content.replace(old_mousedown, new_mousedown)

# 4. Modify mousemove
old_mousemove = """doc.addEventListener('mousemove', (e) => {
          if (!dragEl) return;
          const dx = e.clientX - startMouseX;
          const dy = e.clientY - startMouseY;"""

new_mousemove = """doc.addEventListener('mousemove', (e) => {
          if (isResizing && activeResizeEl) {
             const dx = e.clientX - startMouseX;
             const dy = e.clientY - startMouseY;
             let newWidth = startWidth;
             let newHeight = startHeight;
             
             if (resizeDir === 'br') {
                newWidth = startWidth + dx;
                newHeight = startHeight + dy;
             } else if (resizeDir === 'tr') {
                newWidth = startWidth + dx;
                newHeight = startHeight - dy;
             } else if (resizeDir === 'bl') {
                newWidth = startWidth - dx;
                newHeight = startHeight + dy;
             } else if (resizeDir === 'tl') {
                newWidth = startWidth - dx;
                newHeight = startHeight - dy;
             }
             
             if (activeResizeEl.tagName === 'IMG') {
                 activeResizeEl.style.width = newWidth + 'px';
                 activeResizeEl.style.height = 'auto'; 
             } else {
                 activeResizeEl.style.width = newWidth + 'px';
                 activeResizeEl.style.height = newHeight + 'px';
             }
             
             const rect = activeResizeEl.getBoundingClientRect();
             resizeOverlay.style.width = rect.width + 'px';
             resizeOverlay.style.height = rect.height + 'px';
             resizeOverlay.style.top = (rect.top + doc.defaultView.scrollY) + 'px';
             resizeOverlay.style.left = (rect.left + doc.defaultView.scrollX) + 'px';
             
             e.preventDefault();
             e.stopPropagation();
             return;
          }

          if (!dragEl) return;
          const dx = e.clientX - startMouseX;
          const dy = e.clientY - startMouseY;"""

content = content.replace(old_mousemove, new_mousemove)

# 5. Update overlay pos during drag
old_drag_pos = """dragEl.style.left = newLeft + 'px';
            dragEl.style.top = newTop + 'px';
          }
        }, true);"""

new_drag_pos = """dragEl.style.left = newLeft + 'px';
            dragEl.style.top = newTop + 'px';
            
            if (activeResizeEl === dragEl) {
               const rect = activeResizeEl.getBoundingClientRect();
               resizeOverlay.style.top = (rect.top + doc.defaultView.scrollY) + 'px';
               resizeOverlay.style.left = (rect.left + doc.defaultView.scrollX) + 'px';
            }
          }
        }, true);"""

content = content.replace(old_drag_pos, new_drag_pos)

# 6. Modify mouseup
old_mouseup = """doc.addEventListener('mouseup', (e) => {
          if (dragEl) {"""

new_mouseup = """doc.addEventListener('mouseup', (e) => {
          if (isResizing) {
             isResizing = false;
             if (activeResizeEl) activeResizeEl.setAttribute('data-pos-edited', 'true');
             e.preventDefault(); e.stopPropagation();
          }

          if (dragEl) {"""

content = content.replace(old_mouseup, new_mouseup)


with open('public/builder.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected smoothly!")
