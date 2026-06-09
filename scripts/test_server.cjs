const http = require('http');
const fs = require('fs');
const vm = require('vm');

http.get('http://localhost:3030/hubmaster.html', (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    console.log(`Downloaded ${data.length} characters from server.`);
    fs.writeFileSync('downloaded.html', data, 'utf8');

    // Parse script blocks of the downloaded content
    const regex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    let index = 1;
    while ((match = regex.exec(data)) !== null) {
      const js = match[1];
      console.log(`Analyzing downloaded script block ${index} (length: ${js.length})...`);
      try {
        new vm.Script(js);
        console.log(`Downloaded script block ${index} is valid!`);
      } catch (err) {
        console.error(`Error in downloaded script block ${index}:`, err);
      }
      index++;
    }
  });
}).on('error', (err) => {
  console.error('Request failed:', err);
});
