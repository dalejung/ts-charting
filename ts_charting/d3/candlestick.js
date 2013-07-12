var d = require('./pre.js')
data = d.data
index = d.index

var d3 = require('d3')

function min(a, b){ return a < b ? a : b ; }
function max(a, b){ return a > b ? a : b; }    

var width = 1200;
var height = 800;
var margin = 50;

d3.selectAll('#chart svg').remove()

var chart = d3.select("#chart")
  .append("svg:svg")
  .attr("class", "chart")
  .attr("width", width)
  .attr("height", height);


function build_chart(data) {
  var bar_width = 0.5 * (width - 2*margin)/data.length

  var x = d3.scale.linear()
    .domain([0, data.length-1])
    .range([margin,width-margin]);

  var y = d3.scale.linear()
    .domain([d3.min(data, function(x) {return x[2];}) * .95, 
             d3.max(data, function(x){return x[1];}) * 1.01])
    .range([height-margin, margin]);

  var now = new Date();
  var utc_offset = now.getTimezoneOffset() * 60000;
  var date = new Date(index[0] / 1000000 + utc_offset);

  var format = d3.time.format("%Y-%m-%d");

  chart.selectAll("text.xrule")
   .data(x.ticks(10))
   .enter().append("svg:text")
   .attr("class", "xrule")
   .attr("x", x)
   .attr("y", height - margin)
   .attr("dy", 20)
   .attr("text-anchor", "middle")
  .text(function(d){
    var date = new Date(index[d] / 1000000 + utc_offset);
    return format(date);
  });

 chart.selectAll("text.yrule")
  .data(y.ticks(10))
  .enter().append("svg:text")
  .attr("class", "yrule")
  .attr("x", width - margin)
  .attr("y", y)
  .attr("dy", 0)
  .attr("dx", 20)		 
  .attr("text-anchor", "middle")
  .text(String);

  chart.selectAll("line.x")
   .data(x.ticks(10))
   .enter().append("svg:line")
   .attr("class", "x")
   .attr("x1", x)
   .attr("x2", x)
   .attr("y1", margin)
   .attr("y2", height - margin)
   .attr("stroke", "#ccc")
   .attr("width", 1)

  var line_y = chart.selectAll("line.y")
   .data(y.ticks(10))

   line_y.enter().append("svg:line")
   .attr("class", "y")
   .attr("x1", margin)
   .attr("x2", width - margin)
   .attr("y1", y)
   .attr("y2", y)
   .attr("stroke", "#ccc");

  candles = chart.selectAll("g.candlestick");

  candles = chart.selectAll("g.candlestick")
    .data(data).enter().append("svg:g")
    .attr("class", "candlestick")
    .attr("transform", function(d, i) {return "translate("+(x(i)-bar_width/2)+','+min(d[0], d[3])+')'})

  candles.append("svg:line")
    .attr("class", "stem")
    .attr("x1", bar_width / 2)
    .attr("x2", bar_width / 2)		    
    .attr("y1", function(d) { return y(d[1]);})
    .attr("y2", function(d) { return y(d[2]); })
    .attr("stroke", 'black')

  candles.append("svg:rect")
    .attr("x", 0)
          .attr("y", function(d) {return y(max(d[0], d[3]));})		  
    .attr("height", function(d) { return y(min(d[0], d[3]))-y(max(d[0], d[3]));})
    .attr("width", bar_width)
          .attr("fill",function(d) { return d[0] > d[3] ? "red" : "green" ;});
}
var lines = chart.selectAll('rect');
build_chart(data);
