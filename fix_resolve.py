import glob

for filepath in glob.glob('public/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # FIX: resolveCatalogRoute - when tabId is null from resolvedCat fallback,
    # also try resolvedCat.tabId (the new field we added)
    # Current line 11373:
    # tabId: resolvedTab ? resolvedTab.id : (resolvedCat ? resolvedCat.tabId : null),
    # This is already correct IF resolvedCat.tabId is populated... let's also check the item
    # item.tabId is also a new field.
    
    old_return = """      if (resolvedTab || resolvedCat || resolvedItem) {
        return {
          tabId: resolvedTab ? resolvedTab.id : (resolvedCat ? resolvedCat.tabId : null),
          catId: resolvedCat ? resolvedCat.id : null,
          itemId: resolvedItem ? resolvedItem.id : null
        };
      }"""
    
    new_return = """      if (resolvedTab || resolvedCat || resolvedItem) {
        const tabId = resolvedTab
          ? resolvedTab.id
          : resolvedCat
            ? (resolvedCat.tabId || null)
            : resolvedItem
              ? (resolvedItem.tabId || null)
              : null;
        return {
          tabId: tabId,
          catId: resolvedCat ? resolvedCat.id : (resolvedItem ? resolvedItem.catId : null),
          itemId: resolvedItem ? resolvedItem.id : null
        };
      }"""
    
    new_content = content.replace(old_return, new_return)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    if new_content != content:
        print(f'Fixed: {filepath}')
    else:
        print(f'No changes: {filepath}')

print('Done!')
