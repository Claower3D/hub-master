import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get("step_index") == 901:
                print(f"Step 901 type={data.get('type')}, keys={list(data.keys())}")
                content = data.get("content", "")
                print(f"Content length={len(content)}")
                print("First 300 chars:")
                print(repr(content[:300]))
                print("Last 300 chars:")
                print(repr(content[-300:]))
                break
        except Exception as e:
            pass
