const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});



function compress(points, precision) {
   var oldLat = 0, oldLng = 0, len = points.length, index = 0;
   var encoded = '';
   precision = Math.pow(10, precision);
   while (index < len) {
      //  Round to N decimal places
      var lat = Math.round(points[index++] * precision);
      var lng = Math.round(points[index++] * precision);

      //  Encode the differences between the points
      encoded += encodeNumber(lat - oldLat);
      encoded += encodeNumber(lng - oldLng);

      oldLat = lat;
      oldLng = lng;
   }
   return encoded;
}

function encodeNumber(num) {
   var num = num << 1;
   if (num < 0) {
      num = ~(num);
   }
   var encoded = '';
   while (num >= 0x20) {
      encoded += String.fromCharCode((0x20 | (num & 0x1f)) + 63);
      num >>= 5;
   }
   encoded += String.fromCharCode(num + 63);
   return encoded;
}