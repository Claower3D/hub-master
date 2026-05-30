import os

log_dir = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs"
if os.path.exists(log_dir):
    print("Files in logs dir:", os.listdir(log_dir))
else:
    print("Log dir does not exist.")
