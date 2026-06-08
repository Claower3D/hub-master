import re

log_path = r"C:\Users\SystemX\.gemini\antigravity\brain\95fdbd5f-3238-477c-85ab-b847ede4f00b\.system_generated\logs\overview.txt"
with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the first HTML match starting with <!DOCTYPE html> and ending with </html>
# We know it has diff markers. Let's extract it.
m = re.search(r"<!DOCTYPE html>.*?</html>", text, re.DOTALL)
if m:
    diff_content = m.group(0)
    # Clean up JSON string escapes (\\n to \n, \\" to ", etc.)
    cleaned = diff_content.replace(r'\n', '\n').replace(r'\"', '"').replace(r'\/', '/').replace(r'\\', '\\')
    
    # Let's reconstruct the file by processing line by line.
    # In a typical diff representation in the log:
    # - Lines that were changed/added start with '+' or '-' (e.g. '+<head>' or '-<head>')
    # - Unchanged lines might start with a space or no prefix, or they might have been captured by the editor.
    # Let's write a parser that handles:
    # If the line starts with '+', we strip the '+' and keep the line.
    # If the line starts with '-', we discard it.
    # If the line starts with ' ' (space), we strip the leading space and keep it.
    # Otherwise, we keep the line.
    
    reconstructed_lines = []
    lines = cleaned.split('\n')
    for line in lines:
        if line.startswith('+'):
            reconstructed_lines.append(line[1:])
        elif line.startswith('-'):
            # Discard removed lines
            continue
        elif line.startswith(' '):
            reconstructed_lines.append(line[1:])
        else:
            reconstructed_lines.append(line)
            
    reconstructed_html = '\n'.join(reconstructed_lines)
    with open("hubmaster_reconstructed.html", "w", encoding="utf-8") as out:
        out.write(reconstructed_html)
    print(f"Reconstructed HTML written to hubmaster_reconstructed.html. Total lines: {len(reconstructed_lines)}")
else:
    print("Could not find HTML diff in overview.txt")
