import json
import os

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    print("Parsing logs...")
    with open(log_path, 'r', encoding='utf-8') as f:
        for line_idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                step = data.get("step_index")
                action_type = data.get("type")
                tool_calls = data.get("tool_calls", [])
                
                # Check for write_to_file or replace_file_content in tool_calls
                for tc in tool_calls:
                    name = tc.get("name")
                    if name in ("write_to_file", "replace_file_content"):
                        args = tc.get("args", {})
                        target = args.get("TargetFile")
                        content_key = "CodeContent" if name == "write_to_file" else "ReplacementContent"
                        content_val = args.get(content_key, "")
                        print(f"Line {line_idx}: Step {step}, Tool {name}, Target: {target}, ContentLen: {len(content_val)}")
            except Exception as e:
                pass
else:
    print("Log path does not exist")
