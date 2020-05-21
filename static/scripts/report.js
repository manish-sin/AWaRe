
document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect('http://localhost:5000');

	socket.on('connect', () => {
		socket.send("I am connected");
	})


	socket.on('message', data=> {
		<!-- var variable1 = localStorage.getItem("vOneLocalStorage "); */ -->
		console.log(`Apps Names: ${data[0][0]};`)
		console.log(`Apps Duration: ${data[0][1]};`)
		console.log(`App COunt: ${data[0][2]};`)
		console.log(`Choosen Apps Name: ${data[1][2]};`)
		console.log(`Sub-app Duration: ${data[1][1]};`)
		console.log(`Sub-app Name: ${data[1][0]};`) 
		console.log(`Sub_app Count: ${data[1][3]};`) 
		
		/* for (i = 1; i < data[0]+1; i++) {
         console.log(`Message No.  : ${data[i]};`)
        } */



	/* #const data = data */
	
	
	function addData(chart, label, data) {
		console.log("add function read");
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
	}

	function removeData(chart) {
		console.log("remove function read");
    chart.data.labels.shift();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
		console.log(chart);
	
    });
    chart.update();
	}
	
    
	
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
	console.log(chrome_chart)
	
	

	
	var chrome_chart = new Chart(document.getElementById("chrome-chart"), b);
	
	/* chrome_chart.destroy();
	removeData(chrome_chart) */
	
/* 	ctx = document.getElementById("chrome-chart");
	ctx.height = 500;
	chrome_chart = new Chart(ctx, b);
	console.log(chrome_chart) */
	
	

	
    
	/* var c = data[1][0]
	var d = data[1][1]
	removeData(chrome_chart)
	addData(chrome_chart, c, d) */ 
	
	
	
	
	
	
	
	/* if(chrome_chart!=null){console.log("did read if")
		chrome_chart.data[0] = data[1][0];
	  chrome_chart.data.datasets.data = data[1][1]; // Would update the first dataset's value of 'March' to be 50
	  chrome_chart.options.title.text=data[1][2];
	chrome_chart.update();}
	else{chrome_chart.data[0] = data[1][0];
	  chrome_chart.data.datasets.data = data[1][1]; // Would update the first dataset's value of 'March' to be 50
	  chrome_chart.options.title.text=data[1][2];
	chrome_chart.update();	
      
	  
	console.log("did not read if")
	}	 */
	
	

	
	document.getElementById('chrome-chart').height = "100"
	document.getElementById("pie-chart").onclick = function(evt)
	 {var activePoints = pie_chart.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var chartData = activePoints[0]['_chart'].config.data;
        var idx = activePoints[0]['_index'];

        var label = chartData.labels[idx];
        var value = chartData.datasets[0].data[idx];

        var url = "http://localhost:5000/detail";
        console.log(url);
		
		
		socket.emit('msg',{label} );
		document.getElementById("detail").click();
		
		
		
	
		
		
       
      }
    };
	
	
	
	
     

	
	

	});

	});

