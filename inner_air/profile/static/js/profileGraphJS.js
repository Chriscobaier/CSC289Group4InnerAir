var ctx = document.getElementById("histogram1").getContext("2d");
var histogram1 = new Chart(ctx,
{
    type: 'line',
    data:
    {
        labels: xWeeklabels,
        datasets:
        [{
            label: "Number of Exercises Completed past 1 week",
            data: yWeeklabel,
            fill: false,
            borderColor: 'rgb(49, 67, 170)',
            pointBackgroundColor: 'rgb(49, 67, 170)',
            lineTension: 0.1

        }]
    },
    options:
    {
        responsive: false,
        plugins: {legend:{display:false}, title:{display: true,
            text:'Number of Exercises Completed past 1 week',
            font: {size:20,
                lineHeight:2}}},
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 1},
                    title:{display: true,
                    text:'Number of Exercises',
                    font: {size:16,
                            weight:'bold',
                            lineHeight:2}}},
                x:{grid:{display: false},
                    title:{display: true,
                        text:'Date',
                        font: {size:20,
                            weight:'bold',
                            lineHeight:2}}}
            }

    }});

var ctx = document.getElementById("histogram2").getContext("2d");
var histogram2 = new Chart(ctx,
    {
        type: 'line',
        data:
        {
            labels: xMonthLabels,
datasets:
[{
    data: yMonthlabel,
    label: "Number of Exercises Completed past 1 month",
    fill: false,
    borderColor: 'rgb(49, 67, 170)',
    pointBackgroundColor: 'rgb(49, 67, 170)',
    lineTension: 0.1
        }]
    },
    options:
    {
        responsive: false,
        plugins: {legend:{display:false}, title:{display: true,
            text:'Number of Exercises Completed past 1 month',
            font: {size:20,
                lineHeight:2}}},
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 1},
                    title:{display: true,
                    text:'Number of Exercises',
                    font: {size:16,
                            weight:'bold',
                            lineHeight:2}}},
                x:{grid:{display: false}, ticks:{display: false},
                    title:{display: true,
                        text:'Date',
                        font: {size:20,
                            weight:'bold',
                            lineHeight:2}}}
            }
    }});

var ctx = document.getElementById("histogram3").getContext("2d");
var histogram3 = new Chart(ctx,
    {
        type: 'line',
        data:
        {
            labels: xQLabels,
datasets:
[{
    label: "Number of Exercises Completed past 3 months",
    data: yQlabel,
    fill: false,
    borderColor: 'rgb(49, 67, 170)',
    pointBackgroundColor: 'rgb(49, 67, 170)',
    lineTension: 0.1
        }]
    },
    options:
    {
        responsive: false,
        plugins: {legend:{display:false}, title:{display: true,
            text:'Number of Exercises Completed past 3 months',
            font: {size:20,
                lineHeight:2}}},
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 1},
                    title:{display: true,
                    text:'Number of Exercises',
                    font: {size:16,
                            weight:'bold',
                            lineHeight:2}}},
                x:{grid:{display: false}, ticks:{display:false},
                    title:{display: true,
                        text:'Date',
                        font: {size:20,
                            weight:'bold',
                            lineHeight:2}}}
                }
            }
     });

var ctx = document.getElementById("histogram4").getContext("2d");
var histogram4 = new Chart(ctx,
    {
        type: 'bar',
        data:
        {
            labels: xBreathLabel,
datasets:
[{
    label: "Maximum Breath Hold Time (seconds) past 1 month",
    data: yDataMaxBreathHoldslabel,
    fill: false,
    backgroundColor: 'rgb(170, 0, 91, 0.5)',
    borderColor: 'rgb(170, 0, 91)',
    borderWidth: 1,
    lineTension: 0.1
        }]
    },
    options:
    {
        responsive: false,
        plugins: {legend:{display:false}, title:{display: true,
            text:'Maximum Breath Hold Time (seconds) past 1 month',
            font: {size:20,
                lineHeight:2}}},
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 10},
                    title:{display: true,
                    text:'Seconds',
                    font: {size:16,
                            weight:'bold',
                            lineHeight:2}}},
                x:{grid:{display: false}, ticks:{display:false},
                    title:{display: true,
                        text:'Date',
                        font: {size:20,
                            weight:'bold',
                            lineHeight:2}}}
                }
            }
     });


/*
var ctx = document.getElementById("histogram5").getContext("2d");
var histogram5 = new Chart(ctx,
    {
        type: 'line',
        data:
        {
            labels: xQLabels,
datasets:
[{
    label: "Number of Exercises completed",
    data: yQlabel,
    fill: false,
    lineTension: 0.1
        }]
    },
options:
{
    responsive: false,
        scales:
    {
        yAxes: [{ ticks: { beginAtZero: true } }],
            x: [{ type: 'time',tooltipFormat: 'ddd. DD MMM YYYY', time: { unit: 'day', tooltipFormat: 'ddd. DD MMM YYYY' } }],
            }
}
});

*/


// Hide all canvas elements except the first one
var charts = document.getElementsByClassName("chart");
for (var i = 1; i < charts.length; i++) {
  charts[i].style.display = "none";
}

// Function to show the selected graph and hide the others
function showGraph(num) {
  for (var i = 0; i < charts.length; i++) {
    if (i == num-1) {
      charts[i].style.display = "block";
    } else {
      charts[i].style.display = "none";
    }
  }
}
