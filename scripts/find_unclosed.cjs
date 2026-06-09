const fs = require('fs');
const html = fs.readFileSync('hubmaster.html', 'utf8');

const regex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let index = 1;

while ((match = regex.exec(html)) !== null) {
  if (index === 2) {
    const js = match[1];
    console.log("Analyzing Script Block 2...");
    
    // Simple bracket balancer that tracks characters, braces, parens, templates, quotes
    let inString = null; // null or ' | " | `
    let stack = [];
    let line = 7224; // starting line of Script Block 2
    let col = 1;

    for (let i = 0; i < js.length; i++) {
      const char = js[i];
      if (char === '\n') {
        line++;
        col = 1;
      } else {
        col++;
      }

      // Handle escape chars
      if (char === '\\' && inString) {
        i++; // skip next char
        continue;
      }

      if (inString) {
        if (char === inString) {
          inString = null;
        } else if (inString === '`' && char === '$' && js[i+1] === '{') {
          stack.push({ type: 'template_expr', line, col });
          i++; // skip '{'
        }
        continue;
      }

      if (char === '"' || char === "'" || char === '`') {
        inString = char;
        continue;
      }

      if (char === '{') {
        stack.push({ type: 'brace', line, col });
      } else if (char === '}') {
        const top = stack.pop();
        if (!top) {
          console.error(`Unexpected closing brace } at line ${line}, col ${col}`);
        } else if (top.type === 'template_expr') {
          // Re-enter template string
          inString = '`';
        } else if (top.type !== 'brace') {
          console.error(`Mismatched closing brace } for ${top.type} opened at line ${top.line}, col ${top.col}`);
        }
      } else if (char === '(') {
        stack.push({ type: 'paren', line, col });
      } else if (char === ')') {
        const top = stack.pop();
        if (!top || top.type !== 'paren') {
          console.error(`Unexpected or mismatched closing paren ) at line ${line}, col ${col}`);
        }
      } else if (char === '[') {
        stack.push({ type: 'bracket', line, col });
      } else if (char === ']') {
        const top = stack.pop();
        if (!top || top.type !== 'bracket') {
          console.error(`Unexpected or mismatched closing bracket ] at line ${line}, col ${col}`);
        }
      }
    }

    if (inString) {
      console.error(`Unclosed string literal (${inString}) starting somewhere!`);
    }
    if (stack.length > 0) {
      console.error(`Unclosed structures remaining at end of script:`, stack);
    } else {
      console.log("No unclosed structures found!");
    }
  }
  index++;
}
