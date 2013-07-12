d3 = require('d3');
fs = require('fs');

// replace d3.csv to work with local files
// TODO. add check for url so those will still work
d3.csv = (function(old) {
  var wrapped = function(file, callback) {
    file = './' + file;
    var filename = require.resolve(file);
    var content = fs.readFileSync(filename, 'utf8');
    var data = old.parse(content);
    return callback(data)
  }
  wrapped.prototype = old;
  for (var name in old) {
    wrapped[name] = old[name]
  }
  return wrapped
})(d3.csv)
