import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            content = data.get("content", "")
            step_idx = data.get("step_index")
            action_type = data.get("type")
            
            # Check if there is any HTML/CSS content
            if "<!doctype html>" in content.lower() or "button class" in content.lower() or "Качественная" in content:
                print(f"Line {line_idx}: Step {step_idx}, Type {action_type}, Content length {len(content)}")
                print(f"  Preview: {repr(content[:200])}")
        except Exception as e:
            pass
