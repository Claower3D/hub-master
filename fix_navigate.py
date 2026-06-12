import glob

for filepath in glob.glob('public/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change navigateThematic to always open in a new tab
    old_func = """    window.navigateThematic = function (catId, subcatId = '', itemId = '') {
      let path = '/';
      if (catId) {
        path += catId;
        if (subcatId) {
          path += '/' + subcatId;
          if (itemId) {
            path += '/' + itemId;
          }
        }
      }
      
      

      if (window.location.pathname !== path) {
        history.pushState({ catId, subcatId, itemId }, '', path);
      }
      renderThematicPage(catId, subcatId, itemId);
      closeMegaModal();
    };"""
    
    new_func = """    window.navigateThematic = function (catId, subcatId = '', itemId = '') {
      // Empty catId = go home
      if (!catId) {
        closeMegaModal();
        if (window.location.pathname !== '/') {
          window.location.href = '/';
        }
        return;
      }
      let path = '/' + catId;
      if (subcatId) {
        path += '/' + subcatId;
        if (itemId) {
          path += '/' + itemId;
        }
      }
      // Always open service page as a fresh full-page navigation (new URL, NOT SPA overlay)
      closeMegaModal();
      window.location.href = path;
    };"""
    
    new_content = content.replace(old_func, new_func)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    if new_content != content:
        print(f'Fixed: {filepath}')
    else:
        print(f'No changes: {filepath}')

print('Done!')
