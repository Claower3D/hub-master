import os
import json
import re

brain_dir = r"C:\Users\SystemX\.\.gemini\antigravity\brain"
if not os.path.exists(brain_dir):
    brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"

candidates = []

print(f"Scanning brain directory: {brain_dir}")
for conv in os.listdir(brain_dir):
    conv_path = os.path.join(brain_dir, conv)
    if not os.path.isdir(conv_path):
        continue
    log_path = os.path.join(conv_path, ".system_generated", "logs", "overview.txt")
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if 'hubmaster.html' in line and ('Total Lines: 4' in line or 'Total Lines: 3' in line):
                        # Inspect the content length
                        size = len(line)
                        if size > 100000: # large payload
                            print(f"Match found in Conv: {conv}, Line: {line_num}, Size: {size}")
                            candidates.append((conv, line_num, line))
        except Exception as e:
            pass

print(f"Found {len(candidates)} candidates.")
for idx, (conv, line_num, line) in enumerate(candidates):
    try:
        data = json.loads(line)
        content = data.get("content", "")
        if not content and "output" in data:
            content = data["output"]
            
        # Parse line-numbered lines
        lines_match = re.findall(r'(?:^|\n)\s*(\d+):\s*(.*)', content)
        if lines_match:
            max_line = max(int(num) for num, _ in lines_match)
            min_line = min(int(num) for num, _ in lines_match)
            print(f"Candidate {idx}: Conv={conv}, LogLine={line_num}, Line range={min_line} to {max_line}")
            
            reconstructed = {}
            for num, text in lines_match:
                reconstructed[int(num)] = text
            
            out_filename = f"recovered_hubmaster_conv_{conv}_line_{line_num}.html"
            with open(out_filename, 'w', encoding='utf-8') as out:
                for i in range(1, max_line + 1):
                    if i in reconstructed:
                        out.write(reconstructed[i] + "\n")
                    else:
                        out.write(f"<!-- MISSING LINE {i} -->\n")
            print(f"  Saved to {out_filename}")
    except Exception as e:
        print(f"  Error parsing candidate {idx}: {e}")
