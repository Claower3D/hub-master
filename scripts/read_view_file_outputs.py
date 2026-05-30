import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            action_type = data.get("type")
            if action_type == "VIEW_FILE":
                content = data.get("content", "")
                args = data.get("args", {})
                print(f"Line {line_idx}: Step {data.get('step_index')}, Args {args}, Content len: {len(content)}")
                # Print first 200 chars of content
                print(f"  Snippet: {repr(content[:200])}")
        except Exception as e:
            pass
