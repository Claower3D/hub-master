import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

css_inject = '''
    /* Mobile Responsive Fixes for Modals */
    @media (max-width: 768px) {
      .mega-catalog-body {
        display: flex !important;
        flex-direction: column !important;
        overflow-y: auto !important;
      }
      .mega-col {
        padding: 16px !important;
        border-right: none !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        overflow-y: visible !important;
      }
      [data-theme="light"] .mega-col {
        border-bottom-color: rgba(0, 0, 0, 0.05);
      }
      .mega-col:empty {
        display: none !important;
      }
      .mega-col:last-child {
        background: transparent !important;
      }
      .mega-catalog-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }
      .mega-controls {
        margin: 0 !important;
        width: 100% !important;
        max-width: none !important;
      }

      #cab-dashboard-container {
        flex-direction: column !important;
        overflow-y: auto;
      }
      .cab-sidebar {
        width: 100% !important;
        border-right: none !important;
        border-bottom: 1px solid #1f212a !important;
        padding: 16px !important;
        height: auto !important;
        flex-shrink: 0;
      }
      [data-theme="light"] .cab-sidebar {
        border-bottom-color: var(--border) !important;
      }
      #cab-dashboard-container > div:last-child {
        padding: 16px !important;
        width: 100% !important;
        box-sizing: border-box;
      }
    }
'''

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Mobile Responsive Fixes for Modals' not in content:
        insert_marker_css = ".mega-cat-btn {"
        content = content.replace(insert_marker_css, css_inject + "\n    " + insert_marker_css)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
