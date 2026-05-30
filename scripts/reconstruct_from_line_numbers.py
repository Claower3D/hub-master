import json
import os
import re

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

# Map: line_number (int) -> (step_index (int), line_content (str))
file_lines = {}

# Regular expression to match lines like "123: <div>" or " 123: <div>"
# We want to be careful not to match random text that has a colon.
# The line number should start the line or follow a newline, with optional spaces.
line_pattern = re.compile(r'(?:^|\n)\s*(\d+):\s*(.*)')

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        for json_line in f:
            if not json_line.strip():
                continue
            try:
                data = json.loads(json_line)
                step = data.get("step_index", 0)
                content = data.get("content", "")
                
                # Check for line-numbered patterns in content
                for match in line_pattern.finditer(content):
                    line_num = int(match.group(1))
                    line_text = match.group(2)
                    
                    # If line_num is unreasonably large or 0, ignore
                    if line_num <= 0 or line_num > 6000:
                        continue
                        
                    # Update if we find a newer version of the line
                    if line_num not in file_lines or step >= file_lines[line_num][0]:
                        file_lines[line_num] = (step, line_text)
            except Exception as e:
                pass
                
    # Sort lines by line number
    sorted_line_numbers = sorted(file_lines.keys())
    
    if sorted_line_numbers:
        min_line = sorted_line_numbers[0]
        max_line = sorted_line_numbers[-1]
        print(f"Recovered lines from line {min_line} to {max_line}")
        print(f"Total unique lines recovered: {len(file_lines)}")
        
        # Check for gaps
        gaps = []
        for i in range(min_line, max_line + 1):
            if i not in file_lines:
                gaps.append(i)
        
        print(f"Number of missing lines (gaps): {len(gaps)}")
        if gaps:
            # group gaps into ranges
            gap_ranges = []
            start_gap = gaps[0]
            prev_gap = gaps[0]
            for g in gaps[1:]:
                if g == prev_gap + 1:
                    prev_gap = g
                else:
                    gap_ranges.append((start_gap, prev_gap))
                    start_gap = g
                    prev_gap = g
            gap_ranges.append((start_gap, prev_gap))
            print("Gap ranges:", gap_ranges)
            
        # Write reconstructed file
        out_path = "hubmaster_line_reconstructed.html"
        with open(out_path, "w", encoding="utf-8") as out:
            for i in range(1, max_line + 1):
                if i in file_lines:
                    out.write(file_lines[i][1] + "\n")
                else:
                    out.write(f"<!-- MISSING LINE {i} -->\n")
        print(f"Reconstructed file written to {out_path}")
    else:
        print("No line numbered patterns found in logs.")
else:
    print("Log file not found.")
