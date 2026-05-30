import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\SystemX\Downloads\1\hubmaster.html"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    
    # search for translations const, toggleCity function, translateUI function
    trans_line = -1
    toggle_line = -1
    translate_line = -1
    
    for idx, line in enumerate(lines):
        if 'const translations =' in line and trans_line == -1:
            trans_line = idx
        if 'function toggleCity()' in line and toggle_line == -1:
            toggle_line = idx
        if 'function translateUI()' in line and translate_line == -1:
            translate_line = idx
            
    print(f"translations: line {trans_line+1}")
    print(f"toggleCity: line {toggle_line+1}")
    print(f"translateUI: line {translate_line+1}")
    
    # print lines around translations start
    print("\n--- Translations block start (lines 1735-1770) ---")
    for idx in range(trans_line, min(len(lines), trans_line + 40)):
        print(f"{idx+1}: {lines[idx]}", end='')
        
    # print lines around toggleCity
    print("\n--- toggleCity block start ---")
    for idx in range(toggle_line, min(len(lines), toggle_line + 20)):
        print(f"{idx+1}: {lines[idx]}", end='')
        
    # print lines around translateUI
    print("\n--- translateUI block start ---")
    for idx in range(translate_line, min(len(lines), translate_line + 30)):
        print(f"{idx+1}: {lines[idx]}", end='')
else:
    print("hubmaster.html not found.")
