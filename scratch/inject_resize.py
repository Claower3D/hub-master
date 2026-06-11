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

# Insert CSS into the injected styles
content = re.sub(r'(\.builder-section-toolbar \{)', lambda m: css_to_add + m.group(1), content)

# 2. Add JavaScript logic
js_to_add = """
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

# Insert variables after SMART GUIDES
content = re.sub(r'(let clickStart = 0;)', lambda m: m.group(1) + js_to_add, content)


# Modify mousedown
mousedown_logic = """
          if (e.target.classList.contains('resize-handle')) {
             isResizing = true;
             resizeDir = e.target.getAttribute('data-dir');
             startMouseX = e.clientX;
             startMouseY = e.clientY;
             if (activeResizeEl) {
                 startWidth = activeResizeEl.offsetWidth;
                 startHeight = activeResizeEl.offsetHeight;
                 // Prevent dragging if resizing
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
"""

content = re.sub(r'const editable = e\.target\.closest\(\'\.builder-inline-editable\'\);\s*if \(editable\) \{', mousedown_logic, content)

# Hide overlay if clicked outside
hide_logic = """
          } else if (!e.target.closest('.builder-resize-overlay') && !e.target.closest('.builder-section-toolbar')) {
             resizeOverlay.style.display = 'none';
             activeResizeEl = null;
          }
"""
content = re.sub(r'startTop = parseFloat\(dragEl\.style\.top\) \|\| 0;\s*\}', lambda m: m.group(0) + hide_logic, content)

# Modify mousemove
mousemove_logic = """
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
             
             // Keep aspect ratio for images if shift is not pressed
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
"""
content = re.sub(r'const dx = e\.clientX - startMouseX;\s*const dy = e\.clientY - startMouseY;', lambda m: m.group(0) + mousemove_logic, content)

# Update overlay pos on drag
update_overlay_drag = """
            if (activeResizeEl === dragEl) {
               const rect = activeResizeEl.getBoundingClientRect();
               resizeOverlay.style.top = (rect.top + doc.defaultView.scrollY) + 'px';
               resizeOverlay.style.left = (rect.left + doc.defaultView.scrollX) + 'px';
            }
"""
content = re.sub(r'dragEl\.style\.top = newTop \+ \'px\';', lambda m: m.group(0) + update_overlay_drag, content)

# Modify mouseup
mouseup_logic = """
          if (isResizing) {
             isResizing = false;
             if (activeResizeEl) activeResizeEl.setAttribute('data-pos-edited', 'true');
             e.preventDefault(); e.stopPropagation();
          }
"""
content = re.sub(r'if \(dragEl\) \{', lambda m: mouseup_logic + m.group(0), content)

with open('public/builder.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected Photoshop-like resize handles into builder.html!")
