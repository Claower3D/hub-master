import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line_idx, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
        step_idx = data.get("step_index")
        if step_idx is not None and step_idx >= 1210:
            tool_calls = data.get("tool_calls", [])
            content = data.get("content", "")
            action_type = data.get("type")
            
            # Print info about the step
            print(f"Line {line_idx}: Step {step_idx}, Type {action_type}, Content length: {len(content)}")
            if tool_calls:
                for tc in tool_calls:
                    print(f"  Tool Call: {tc.get('name')} with args {tc.get('args')}")
            
            # If there's content, look for text like "Showing lines" or the actual file content
            if "Showing lines" in content:
                print(f"  --> Contains 'Showing lines' info!")
    except Exception as e:
        pass
