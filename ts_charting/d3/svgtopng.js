var child_proc = require('child_process');
var fs = require('fs');

function svgtopng(svgsrc, dest) {
  var res = fs.createWriteStream(dest);
  var convert = child_proc.spawn("convert", ["svg:", "png:-"]);

  convert.stdout.on('data', function (data) {
    res.write(data);
  });
  convert.on('exit', function(code) {
    res.end();
  });

  convert.stdin.write(svgsrc);
  convert.stdin.end();
}
exports.svgtopng = svgtopng

//var content = fs.readFileSync('forukuman.svg', 'utf8');
//svgtopng(content, 'bob.png')
