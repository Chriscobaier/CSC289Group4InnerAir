let start_button = document.getElementById("start-button");
start_button.addEventListener("click", switch_button);

//changes to stop/start state of the button
function switch_button() {
    if (start_button.classList.contains("button--green")){
        start_button.className = "button";
        start_button.textContent = "Stop"
    } else {
        start_button.className = "button--green";
        start_button.textContent = "Start"
    }
}