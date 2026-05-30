import os

scratch_dir = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\scratch"
for name in ["decoded_logs.txt", "user_requests.txt", "block_markup.txt"]:
    path = os.path.join(scratch_dir, name)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"File {name}: size {size} bytes")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"Contains <!DOCTYPE html>: {'<!DOCTYPE html>' in content}")
        print(f"Contains <html: {'<html' in content}")
