import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            step_idx = data.get("step_index")
            action_type = data.get("type")
            tool_calls = data.get("tool_calls", [])
            content = data.get("content", "")
            
            tool_names = [tc.get("name") for tc in tool_calls] if tool_calls else []
            
            content_len = len(content) if content else 0
            print(f"Line {line_idx}: Step {step_idx}, Type {action_type}, Tools {tool_names}, ContentLen {content_len}")
        except Exception as e:
            print(f"Line {line_idx}: Failed to parse JSON: {e}")
