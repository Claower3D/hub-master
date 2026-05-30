import re

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"
with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find all occurrences of "<!DOCTYPE html>" and "</html>" in the text
# and check if the content between them is clean (i.e. does not have "+ " or "- " at the start of lines).
# Also let's print their lengths and positions.

matches = []
for m in re.finditer(r"<!DOCTYPE html>", text):
    start = m.start()
    end_m = text.find("</html>", start)
    if end_m != -1:
        end = end_m + len("</html>")
        content = text[start:end]
        # Clean up escapes
        cleaned = content.replace(r'\n', '\n').replace(r'\"', '"').replace(r'\/', '/').replace(r'\\', '\\')
        
        # Check if this contains diff markers at the start of lines
        lines = cleaned.split('\n')
        diff_lines = [l for l in lines if l.startswith('+') or l.startswith('-')]
        
        print(f"Match at position {start}: length={len(cleaned)} chars, lines={len(lines)}, diff_lines={len(diff_lines)}")
        
        if len(diff_lines) < 10:  # if very few diff-like lines, it might be clean
            matches.append((start, cleaned))

if matches:
    # Save the cleanest and longest one
    best_start, best_content = max(matches, key=lambda x: len(x[1]))
    with open("hubmaster_clean.html", "w", encoding="utf-8") as out:
        out.write(best_content)
    print(f"Saved cleanest HTML (length {len(best_content)}) from position {best_start} to hubmaster_clean.html")
else:
    print("No clean HTML matches found.")
