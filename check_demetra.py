import os

path = r"C:\Users\SystemX\Downloads\Деметра\index.html"
with open("demetra_index_head.txt", "w", encoding="utf-8") as out:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for _ in range(50):
                out.write(f.readline())
