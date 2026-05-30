import json
import os
import re

log_paths = [
    r"C:\Users\SystemX\.gemini\antigravity\brain\9aa48c27-5e79-4ce6-9c15-f61b17b52430\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\afb57b92-f46a-4fb8-b8d0-13a2e13ea3d7\.system_generated\logs\overview.txt"
]

for log_path in log_paths:
    if not os.path.exists(log_path):
        continue
    print(f"Scanning log: {log_path}")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Read line by line since overview.txt is a json-lines file
        for line_num, line in enumerate(f, 1):
            if 'hubmaster.html' in line and ('Total Lines: 4' in line or 'lines_viewed' in line or 'lines 1 to' in line):
                print(f"  Found reference on line {line_num}: length={len(line)} chars")
                # Let's inspect the JSON structure
                try:
                    data = json.loads(line)
                    # Let's see what keys are there
                    print(f"    Keys: {list(data.keys())}")
                    # If there's content or tool output
                    content = data.get("content", "")
                    if not content and "output" in data:
                        content = data["output"]
                    
                    # Search for line-numbered block
                    # Line numbers are like "1: <!DOCTYPE html>"
                    lines_match = re.findall(r'(?:^|\n)\s*(\d+):\s*(.*)', content)
                    if lines_match:
                        print(f"    Found {len(lines_match)} line-numbered lines in this entry!")
                        # Let's reconstruct the file from this entry
                        max_line = max(int(num) for num, _ in lines_match)
                        min_line = min(int(num) for num, _ in lines_match)
                        print(f"    Line range: {min_line} to {max_line}")
                        
                        # Reconstruct
                        reconstructed = {}
                        for num, text in lines_match:
                            reconstructed[int(num)] = text
                        
                        out_filename = f"reconstructed_from_log_{line_num}.html"
                        with open(out_filename, 'w', encoding='utf-8') as out:
                            for i in range(1, max_line + 1):
                                if i in reconstructed:
                                    out.write(reconstructed[i] + "\n")
                                else:
                                    out.write(f"<!-- MISSING LINE {i} -->\n")
                        print(f"    Saved reconstructed version to {out_filename}")
                except Exception as e:
                    print(f"    Error parsing JSON: {e}")
