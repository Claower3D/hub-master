import re

files_to_patch = ['public/index.html', 'public/hubmaster.html', 'public/template1.html', 'public/template2.html']

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the text
    content = content.replace('Алматы, ул. Байзакова, 280', 'Алматы, Сейфулина 404, БЦ Каскад')
    content = content.replace('"ул. Байзакова, 280"', '"Сейфулина 404, БЦ Каскад"')
    content = content.replace('Алматы, пр. Аль-Фараби 77/7', 'Алматы, Сейфулина 404, БЦ Каскад')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched {filepath}')
