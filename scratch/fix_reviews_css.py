import re
import glob

css_to_add = """
      .showcase-stats-row {
        flex-direction: column;
        align-items: stretch; /* Fix: allow children to be full width */
      }

      .reviews-scroll {
        width: 100%;
        padding-top: 10px;
      }
"""

for file in glob.glob('public/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the showcase-stats-row inside the media query and replace it
    old_css = """      .showcase-stats-row {
        flex-direction: column;
        align-items: center;
      }"""
      
    if old_css in content:
        content = content.replace(old_css, css_to_add)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file}")

print("Done")
