import re

with open('hubmaster.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# 1. Style tag balance
open_style = len(re.findall(r'<style[^>]*>', text))
close_style = len(re.findall(r'</style>', text))
print('style tags open=%d close=%d -> %s' % (open_style, close_style, 'OK' if open_style==close_style else 'MISMATCH'))

# 2. Key JS functions
for fn in ['toggleDropdown','closeAllDropdowns','selectCity','switchCategoryFromMenu','switchCategory']:
    found = ('function ' + fn) in text
    print('JS fn %s: %s' % (fn, 'OK' if found else 'MISSING'))

# 3. Category IDs - look for the names in dropdown matching real servicesData
svc_data_ids = re.findall(r'id: "([^"]+)"', text)
menu_ids = re.findall(r"switchCategoryFromMenu\('([^']+)'\)", text)
for cid in menu_ids:
    print('Cat "%s" in servicesData: %s' % (cid, 'OK' if cid in svc_data_ids else 'NOT FOUND'))

# 4. City count
city_opts = re.findall(r"selectCity\('([^']+)'\)", text)
print('City options count: %d' % len(city_opts))
for c in city_opts:
    print('  - ' + c)
