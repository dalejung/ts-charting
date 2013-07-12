var fs = require('fs');
var d3 = require('d3')

function get_json(file) {
  var filename = require.resolve(file);
  var content = fs.readFileSync(filename, 'utf8');
  return JSON.parse(content);
}

data = get_json('./dataframe.json');

index = data['index']
columns = data['columns']
data = data['data']

exports.data = data
exports.index = index
exports.columns = columns

// whee
d3.select('body').append('div').attr('id', 'chart');
