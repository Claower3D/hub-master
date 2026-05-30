import json
import os

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            content = data.get("content", "")
            # check if there is any mention of view_file and some HTML tags in the same line
            if "view_file" in line.lower() and ("<!doctype" in line.lower() or "</html>" in line.lower() or "body {" in line.lower()):
                print(f"Line {line_idx}: step_index={data.get('step_index')}, type={data.get('type')}, keys={list(data.keys())}")
                print(f"  Content snippet: {repr(content[:200])}")
        except:
            pass
