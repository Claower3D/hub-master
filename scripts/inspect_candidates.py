import os

for f in ["candidate_hubmaster_0.html", "candidate_hubmaster_1.html"]:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        lines = content.splitlines()
        print(f"File: {f}")
        print(f"  Total lines: {len(lines)}")
        print(f"  File size: {len(content)} bytes")
        print(f"  First 10 lines:")
        for l in lines[:10]:
            print(f"    {l[:100]}")
        print(f"  Last 10 lines:")
        for l in lines[-10:]:
            print(f"    {l[:100]}")
        print("-" * 50)
