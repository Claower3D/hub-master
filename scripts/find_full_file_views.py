import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            tool_calls = data.get("tool_calls", [])
            for tc in tool_calls:
                if tc.get("name") == "view_file":
                    args = tc.get("args", {})
                    # If StartLine or EndLine are not present, or if it reads a large range
                    start = args.get("StartLine")
                    end = args.get("EndLine")
                    if start is None or end is None or (isinstance(end, int) and isinstance(start, int) and (end - start > 1000)):
                        print(f"Line {idx}: Step {data.get('step_index')}, view_file args: {args}")
        except Exception as e:
            pass
