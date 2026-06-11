import re
import glob

for file in glob.glob('public/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace /public/ with /
    content = re.sub(r'src="/public/', 'src="/', content)
    content = re.sub(r'url\(\'/public/', 'url(\'/', content)
    content = re.sub(r'avatar:\s*"/public/', 'avatar: "/', content)
    content = re.sub(r'content="https://hubmaster.kz/public/', 'content="https://hubmaster.kz/', content)
    content = re.sub(r'"image":\s*"https://hubmaster.kz/public/', '"image": "https://hubmaster.kz/', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Paths fixed in ALL templates")
