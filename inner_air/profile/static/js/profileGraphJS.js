
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
