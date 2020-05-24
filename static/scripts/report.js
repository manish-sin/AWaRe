
document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect('http://localhost:5000');

	socket.on('connect', () => {
		socket.send("I am connected"); 
	})
	
	
	function go(){
	  var socket = io.connect('http://localhost:5000');
	  var y = document.getElementById("start").value;  
	  socket.emit('msg',{y});
	  console.log(`Go Home: ${y};`);
	  
	  }
	
	
	

	
	socket.on('message', data=> {
		<!-- var variable1 = localStorage.getItem("vOneLocalStorage "); */ -->
		/* console.log(`Apps Names: ${data[0][0]};`)
		console.log(`Apps Duration: ${data[0][1]};`) */
		/* console.log(`App Count: ${data[0][2]};`)*/
		console.log(`Choosen Apps Name: ${data[1][2]};`)
		/* console.log(`Sub-app Duration: ${data[1][1]};`)
		console.log(`Sub-app Name: ${data[1][0]};`)
		console.log(`Sub_app Count: ${data[1][3]};`)*/ 
		console.log(`Today's Date: ${data};`)
		console.log(`Max Date: ${data[2]};`)
		console.log(`Min Date: ${data[3]};`)
		var recived_date = data[1][4];
		document.getElementById("start").value = recived_date;
		document.getElementById("start").min = data[2]
		document.getElementById("start").max = data[3]
		
		
		
	
		
	
		
		

	var h= data[1][3]*40;
	
	var color = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#1ABC9C", "#A93226", "#F5B7B1", "#633974", "#2471A3", "#AED6F1", "#148F77" ]
	
	var a = {
		type: 'pie',
		data: {
		  labels: data[0][0],
		  datasets: [{

			backgroundColor: color,
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
	var b = {
		type: 'horizontalBar',
		data: {
		  labels: data[1][0],
		  datasets: [{

			backgroundColor: 'rgba(174, 252, 101, 0.5)',
			data: data[1][1]
		  }]
		},
		options: {
			
		  
		  title: {
			display: true,
			text: data[1][2]
		  },
		  events: [],
		  
		  
		  scales: {
			yAxes: [{ticks: {mirror: true}}],
		  
			xAxes: [{type: 'linear',
			position: 'top'}]
			},
			legend: { display: false },
		   
		}
		
	};
	var pie_chart = new Chart(document.getElementById("pie-chart"), a );	

	
	var chrome_chart = new Chart(document.getElementById("chrome-chart"), b);

	

	
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

