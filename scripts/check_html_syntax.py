import html.parser
import sys

sys.stdout.reconfigure(encoding='utf-8')

class SimpleHTMLValidator(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags_stack = []
        self.errors = []
        
    def handle_starttag(self, tag, attrs):
        # We don't track self-closing tags
        self_closing = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        if tag not in self_closing:
            self.tags_stack.append((tag, self.getpos()))
            
    def handle_endtag(self, tag):
        self_closing = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        if tag in self_closing:
            return
        if not self.tags_stack:
            self.errors.append(f"Unexpected end tag </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.tags_stack.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tag </{tag}> at line {self.getpos()[0]} (expected </{last_tag}> from line {pos[0]})")
            # Push back to try to recover
            self.tags_stack.append((last_tag, pos))

def validate_file(path):
    print(f"Validating {path}...")
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        parser = SimpleHTMLValidator()
        parser.feed(content)
        
        if parser.tags_stack:
            print(f"Unclosed tags at the end of the file:")
            for tag, pos in reversed(parser.tags_stack):
                print(f"  <{tag}> from line {pos[0]}")
        else:
            print("No unclosed tags!")
            
        if parser.errors:
            print("Tag mismatches found:")
            for err in parser.errors[:15]:
                print("  ", err)
        else:
            print("No tag mismatches!")
            
        # Check script content syntax
        # We can extract the <script> blocks and parse them or run syntax check if possible
        
    except Exception as e:
        print(f"Error during validation: {e}")

validate_file("hubmaster.html")
print("="*40)
validate_file("index.html")
