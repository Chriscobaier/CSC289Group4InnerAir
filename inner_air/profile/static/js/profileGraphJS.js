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
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 1}},
                x:{grid:{display: false}}
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
    label: "Number of Exercises Completed past 1 month",
    data: yMonthlabel,
    fill: false,
    borderColor: 'rgb(49, 67, 170)',
    pointBackgroundColor: 'rgb(49, 67, 170)',
    lineTension: 0.1
        }]
    },
    options:
    {
        responsive: false,
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 1}},
                x:{grid:{display: false}}
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
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 1}},
                x:{grid:{display: false}},}
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
        scales:
            {
                y:{beginAtZero: true, grid:{display: true}, ticks: {stepSize: 10}},
                x:{grid:{display: false}},}
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
