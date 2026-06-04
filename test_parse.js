const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('hubmaster.html', 'utf8');

// Find all script blocks
const regex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let index = 1;
while ((match = regex.exec(html)) !== null) {
  const js = match[1];
  console.log(`Analyzing script block ${index}...`);
  try {
    new vm.Script(js);
    console.log(`Script block ${index} is valid!`);
  } catch (err) {
    console.error(`Error in script block ${index}:`, err);
  }
  index++;
}
