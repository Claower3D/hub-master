import os

brain_dir = r"C:\Users\SystemX\.gemini\antigravity\brain"
if os.path.exists(brain_dir):
    dirs = [d for d in os.listdir(brain_dir) if os.path.isdir(os.path.join(brain_dir, d))]
    print("Brain directories:", dirs)
else:
    print("Brain directory does not exist.")
