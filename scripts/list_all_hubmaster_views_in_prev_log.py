import json
import os

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

views = []

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                step = data.get("step_index")
                action_type = data.get("type")
                tool_calls = data.get("tool_calls", [])
                
                # Check for view_file tool calls
                for tc in tool_calls:
                    name = tc.get("name")
                    if name == "view_file":
                        args = tc.get("args", {})
                        target = args.get("AbsolutePath", "")
                        if "hubmaster.html" in target:
                            start = args.get("StartLine")
                            end = args.get("EndLine")
                            views.append((step, start, end, idx))
            except:
                pass

print(f"Found {len(views)} view_file calls for hubmaster.html:")
for step, start, end, line_num in views:
    print(f"Step {step} (Line {line_num}): range {start} to {end}")
