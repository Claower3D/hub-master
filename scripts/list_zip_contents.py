import zipfile

zip_path = r"C:\Users\SystemX\Downloads\stitch_hub_master_service_portal.zip"
try:
    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
    print(f"Zip contains {len(names)} files. First 30 files:")
    for n in names[:30]:
        print(n)
    
    # Let's search if any name contains hubmaster or index or html
    matches = [n for n in names if 'hubmaster' in n.lower() or 'index' in n.lower() or n.endswith('.html')]
    print(f"\nMatches for 'hubmaster', 'index' or '.html' ({len(matches)} files):")
    for m in matches:
        print(m)
except Exception as e:
    print("Error reading zip:", e)
