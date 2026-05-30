import os

scratch_dir = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\scratch"
files = ["decoded_logs.txt", "search_results.txt", "block_markup.txt"]

for f in files:
    path = os.path.join(scratch_dir, f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"=== {f} ({size} bytes) ===")
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        print("First 200 chars:")
        print(repr(content[:200]))
        print("Count of 'hubmaster':", content.lower().count('hubmaster'))
        # Check if there is any HTML structure
        if '<div' in content or '<style' in content:
            print("Contains HTML tags.")
    else:
        print(f"{f} does not exist")
