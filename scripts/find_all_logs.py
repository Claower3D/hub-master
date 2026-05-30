import json
import os

log_paths = [
    r"C:\Users\SystemX\.gemini\antigravity\brain\afb57b92-f46a-4fb8-b8d0-13a2e13ea3d7\.system_generated\logs\overview.txt",
    r"C:\Users\SystemX\.gemini\antigravity\brain\7738301a-5c16-4d17-873b-e44f04ccf693\.system_generated\logs\overview.txt"
]

for p in log_paths:
    if os.path.exists(p):
        print(f"=== {p} ===")
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        if tc.get("name") == "view_file":
                            args = tc.get("args", {})
                            if 'hubmaster' in str(args).lower():
                                print(f"  Step {data.get('step_index')}: view_file args={args}")
                except Exception as e:
                    pass
