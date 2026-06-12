import os

files_to_update = [
    'public/index.html',
    'public/template1.html',
    'public/template2.html',
    'public/hubmaster.html',
    'hub-master/hubmaster.html'
]

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Change background to background-color in light theme showcase-master-placeholder
    content = content.replace(
        '[data-theme="light"] .showcase-master-placeholder {\n      background: rgba(0, 0, 0, 0.03);',
        '[data-theme="light"] .showcase-master-placeholder {\n      background-color: rgba(0, 0, 0, 0.03);'
    )
    
    # 2. Add explicit background properties to the base class just in case
    replacement = """    .showcase-master-placeholder {
      width: 500px;
      height: 680px;
      background-color: rgba(255, 255, 255, 0.02);
      background-repeat: no-repeat !important;
      background-position: center bottom !important;
      background-size: contain !important;
      border: none;"""
      
    content = content.replace(
        """    .showcase-master-placeholder {
      width: 500px;
      height: 680px;
      background: rgba(255, 255, 255, 0.02);
      border: none;""",
        replacement
    )
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filepath}")
