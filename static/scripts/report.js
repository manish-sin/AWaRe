document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect('http://localhost:5000');

	socket.on('connect', () => {
		socket.send("I am connected");
	})


	socket.on('message', data=> {
		<!-- var variable1 = localStorage.getItem("vOneLocalStorage "); */ -->
		console.log(`Excel Apps: ${data[8]};`)
		console.log(`Excel Duration: ${data[9]};`)
		console.log(`Chrome Apps: ${data[4]};`)
		console.log(`Chrome Duration: ${data[5]};`)
		/* for (i = 1; i < data[0]+1; i++) {
         console.log(`Message No.  : ${data[i]};`)
        } */



	/* #const data = data */
	var color = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#1ABC9C", "#A93226", "#F5B7B1", "#633974", "#2471A3", "#AED6F1", "#148F77" ]

	var pie_chart = new Chart(document.getElementById("pie-chart"), {
		type: 'pie',
		data: {
		  labels: data[0],
		  datasets: [{

			backgroundColor: color,
			data: data[1]
		  }]
		},
		options: {
		  title: {
			display: true,
			text: 'Summay of all applications used'
		  }
		}
	});
	
	var excel_chart = new Chart(document.getElementById("excel-chart"), {
		type: 'horizontalBar',
		data: {
		  labels: data[8],
		  datasets: [{

			backgroundColor: 'rgba(68, 115, 130, 0.5)',
			data: data[9]
		  }]
		},
		options: {
		  title: {
			display: true,
			text: 'Excel'
		  },
		  scales: {
        yAxes: [{ticks: {mirror: true}}]
		  },
		legend: { display: false }
		}
	});
	
	var chrome_chart = new Chart(document.getElementById("chrome-chart"), {
		type: 'horizontalBar',
		data: {
		  labels: data[4],
		  datasets: [{

			backgroundColor: 'rgba(68, 115, 130, 0.5)',
			data: data[5]
		  }]
		},
		options: {
		  title: {
			display: true,
			text: 'Google Chrome'
		  },
		  scales: {
        yAxes: [{ticks: {mirror: true}}]
		  },
		legend: { display: false }
		}
		
	});
	

	});

	});