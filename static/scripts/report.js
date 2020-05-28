
document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect('http://localhost:5000');

	socket.on('connect', () => {
		socket.send("I am connected"); 
	})
	
	document.querySelector('#go').onclick= () => {
	  console.log(`Hi`);
	  
	  var y = document.getElementById("start").value;  
	  
	  socket.emit('msg',{y});
	  console.log(`Go Home: ${y};`);
	  window.location.reload(true)
	  
	  
	  
	  
	  };
	
	
	socket.on('message', data=> {
		<!-- var variable1 = localStorage.getItem("vOneLocalStorage "); */ -->
		/* console.log(`Apps Names: ${data[0][0]};`)
		console.log(`Apps Duration: ${data[0][1]};`) */
		/* console.log(`App Count: ${data[0][2]};`)*/
		console.log(`Choosen Apps Name: ${data[1][2]};`)
		/* console.log(`Sub-app Duration: ${data[1][1]};`)
		console.log(`Sub-app Name: ${data[1][0]};`)*/ 
		console.log(`Sub_app Count: ${data[1][3]};`)
		console.log(`Today's Date: ${data[4]};`)
		console.log(`Max Date: ${data[2]};`)
		console.log(`Min Date: ${data[3]};`)
		console.log(`Min Date: ${data};`)
		console.log(`Min Date: ${data[5]};`)
		var recived_date = data[4];
		document.getElementById("start").value = recived_date;
		document.getElementById("start").min = data[2]
		document.getElementById("start").max = data[3]
		
		
		
	
	
	
	
	
	
	document.getElementById("heading").innerHTML = data[1][2];
	
	
	
	/* 
The base code is borrowed from 
https://bl.ocks.org/charlesdguthrie/11356441
*/
var color = data[5]
//https://codepen.io/va1da5/pen/ORkYQO?editors=0010
function getData(){

	var arr = [];

	var names = data[1][0];

	var items = data[1][1];

	for (var i = 0; i < data[1][3]; i++ ){
		arr.push({name: names[i], count: items[i]});
	}

	arr.sort(function (a, b) {
	  if (a.count > b.count) {
	    return -1;
	  }
	  if (a.count < b.count) {
	    return 1;
	  }
	  return 0;
	});
	return arr;	// produces array of objects {name: "", count: 0}
}



// Create new chart
var hite = data[1][3]*25;

var chart = new HorizontalChart('#chart', hite);


// Draw the chart
chart.draw(getData());
	// every 3 seconds




function HorizontalChart(id, hite){
	this.id = id;
	var self = this;

	this.margin = {top: 0, right: 0, bottom: 0, left: 0};
	this.width = 1200 - this.margin.left - this.margin.right;
	this.height = hite - this.margin.top - this.margin.bottom;
	this.categoryIndent = 4*15 + 5;
	this.defaultBarWidth = 2000;

	this.color = d3.scale.ordinal()
		.range(["#92f79f"]);

	//Set up scales
	this.x = d3.scale.linear()
		.domain([0, this.defaultBarWidth])
		.range([0, this.width]);

	this.y = d3.scale.ordinal()
		.rangeRoundBands([0, this.height], 0.1, 0);

	//Create SVG element
	d3.select(this.id).selectAll("svg").remove();

	this.svg = d3.select(this.id).append("svg")
		.attr("width", this.width + this.margin.left + this.margin.right)
		.attr("height", this.height + this.margin.top + this.margin.bottom)
	  .append("g")
		.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

	
	this.draw = function(data){
		// var margin=settings.margin, width=settings.width, height=settings.height, categoryIndent=settings.categoryIndent, 
		// svg=settings.svg, x=settings.x, y=settings.y;

		//Reset domains
		this.y.domain(data.sort(function(a,b){
			return b.count - a.count;
		})
			.map(function(d) { return d.name; }));

		var barmax = d3.max(data, function(e) {
			return e.count;
		});

		this.x.domain([0,barmax]);

		/////////
		//ENTER//
		/////////

		//Bind new data to chart rows 
		//Create chart row and move to below the bottom of the chart
		var chartRow = this.svg.selectAll("g.chartRow")
			.data(data, function(d){ return d.name});

		chartRow.transition()
			.duration(300)
			.remove();

		var newRow = chartRow
			.enter()
			.append("g")
			.attr("class", "chartRow")
			.attr("transform", "translate(0," + this.height + this.margin.top + this.margin.bottom + ")");

		//Add rectangles
		newRow.insert("rect")
			.attr("class","bar")
			.attr("x", 0)
			.attr("opacity",0)
			.style("fill", function (d, i) { return self.color(d.name)})
			.attr("height", this.y.rangeBand())
			.attr("width", function(d) { return self.x(d.count);}) 

		//Add value labels
		newRow.append("text")
			.attr("class","label")
			.attr("y", this.y.rangeBand()/2)
			.attr("x",0)
			.attr("opacity",0)
			.attr("dy",".35em")
			.attr("dx","0.5em")
			.text(function(d){return d.count;}); 

		//Add Headlines
		newRow.append("text")
			.attr("class","category")
			.attr("text-overflow","ellipsis")
			.attr("y", this.y.rangeBand()/2)
			.attr("x", this.categoryIndent)
			.attr("opacity",0)
			.attr("dy",".35em")
			.attr("dx","0.5em")
			.text(function(d){return d.name});


		//////////
		//UPDATE//
		//////////

		//Update bar widths
		chartRow.select(".bar").transition()
			.duration(300)
			.attr("width", function(d) { return self.x(d.count);})
			.attr("height", this.y.rangeBand())
			.attr("opacity",1);

		//Update data labels
		chartRow.select(".label").transition()
			.duration(300)
			.attr("opacity",1)
			.attr("y", this.y.rangeBand()/2)
			.tween("text", function(d) {
				var i = d3.interpolate(+this.textContent.replace(/\,/g,''), +d.count);
				return function(t) {
					this.textContent = Math.round(i(t));
				};
			});

		//Fade in categories
		chartRow.select(".category").transition()
			.duration(300)
			.attr("y", this.y.rangeBand()/2)
			.attr("opacity",1);

		////////
		//EXIT//
		////////

		//Fade out and remove exit elements
		chartRow.exit().transition()
			.style("opacity","0")
			.attr("transform", "translate(0," + (this.height + this.margin.top + this.margin.bottom) + ")")
			.remove();


		////////////////
		//REORDER ROWS//
		////////////////

		var delay = function(d, i) { return 200 + i * 30; };

		chartRow.transition()
			.delay(delay)
			.duration(900)
			.attr("transform", function(d){ return "translate(0," + self.y(d.name) + ")"; });

	}
}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
















	
	
	
	
	
	
	
	
	
	
	
	
		
	
		
		

	var h= data[1][3]*40;
	
	
	
	var a = {
		type: 'pie',
		data: {
		  labels: data[0][0],
		  datasets: [{

			backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#1ABC9C", "#A93226", "#F5B7B1", "#633974", "#2471A3", "#AED6F1", "#148F77" ],
			data: data[0][1]
		  }]
		},
		options: {
		  title: {
			display: true,
			text: 'Summay of all applications used'
		  }
		  
		}
	};
	
	
	
	var pie_chart = new Chart(document.getElementById("pie-chart"), a );
	
	

	

	
	document.getElementById("pie-chart").onclick = function(evt)
	 {var activePoints = pie_chart.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var chartData = activePoints[0]['_chart'].config.data;
        var idx = activePoints[0]['_index'];

        var label = chartData.labels[idx];
        var value = chartData.datasets[0].data[idx];  
        socket.emit('msg',{label} );
		console.log(`Sub-app: ${label} ;`)
		document.getElementById("detail").click();
		
	  }			
       
      };
	
	
	
	
     

	
	

	});

	});

