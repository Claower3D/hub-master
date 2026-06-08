import json
import os

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if 'step_index' in line:
                try:
                    data = json.loads(line)
                    if data.get("step_index") == 84:
                        content = data.get("content")
                        with open("step_84_untruncated.txt", "w", encoding="utf-8") as out:
                            out.write(content)
                        print("Saved Step 84 untruncated content to step_84_untruncated.txt")
                        break
                except Exception as e:
                    print("Error:", e)
else:
    print("Log not found.")
