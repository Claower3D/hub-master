import os
import json

brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"
matches = []

for root, dirnames, filenames in os.walk(brain_dir):
    for filename in filenames:
        if filename == 'overview.txt':
            path = os.path.join(root, filename)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_idx, line in enumerate(f):
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                            tool_calls = data.get("tool_calls", [])
                            for tc in tool_calls:
                                name = tc.get("name")
                                if name == "write_to_file":
                                    args = tc.get("args", {})
                                    target = args.get("TargetFile", "")
                                    if "hubmaster" in target.lower():
                                        matches.append((path, data.get("step_index"), target, len(args.get("CodeContent", ""))))
                        except:
                            pass
            except Exception as e:
                pass

print(f"Found {len(matches)} write_to_file calls targeting hubmaster:")
for m in matches:
    print(f"Log: {m[0]}, Step: {m[1]}, Target: {m[2]}, ContentLen: {m[3]}")
