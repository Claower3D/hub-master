import glob

for filepath in glob.glob('public/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # FIX 1: In fetchDynamicCatalog - store tabId on each category and item
    old_cat_return = """                return {
                  id: cat.id,
                  title: cat.title,
                  titleKz: getCatalogText(cat.title, 'KZ'),
                  titleEn: getCatalogText(cat.title, 'EN'),
                  icon: cat.icon,
                  items: items
                };"""
    
    new_cat_return = """                return {
                  id: cat.id,
                  tabId: tab.id,
                  title: cat.title,
                  titleKz: getCatalogText(cat.title, 'KZ'),
                  titleEn: getCatalogText(cat.title, 'EN'),
                  icon: cat.icon,
                  items: items
                };"""
    
    # FIX 2: Also add tabId in items
    old_item_return = """                  return {
                    id: sub.id,
                    catId: cat.id,
                    catTitle: cat.title,"""
    
    new_item_return = """                  return {
                    id: sub.id,
                    tabId: tab.id,
                    catId: cat.id,
                    catTitle: cat.title,"""
    
    new_content = content.replace(old_cat_return, new_cat_return).replace(old_item_return, new_item_return)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    if new_content != content:
        print(f'Fixed: {filepath}')
    else:
        print(f'No changes: {filepath}')

print('Done!')
