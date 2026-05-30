import json

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get("step_index")
            if step >= 900 and step <= 906:
                print(f"Step {step}: type={data.get('type')}, source={data.get('source')}, content_len={len(data.get('content', ''))}, keys={list(data.keys())}")
                if 'tool_calls' in data:
                    print(f"  tool_calls: {data['tool_calls']}")
        except Exception as e:
            pass
