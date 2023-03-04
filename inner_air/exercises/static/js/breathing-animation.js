//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// button animation
let start_button = document.getElementById("start-button");
start_button.addEventListener("click", switch_button);

// changes to stop/start state of the button
function switch_button() {
    if (start_button.classList.contains("button--green")) {
        start_button.className = "button--red";
        start_button.textContent = "Stop";
        feather_cycle(cycle_count);
    } else {
        start_button.className = "button--green";
        start_button.textContent = "Start";
    }
}

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// animation variables
let inhale_time;
let inhale_hold;
let exhale_time;
let exhale_hold;
let cycle_count;

// request animation data
var xhr = new XMLHttpRequest();
xhr.open("GET", window.location.href + "/animation.data");
xhr.responseType = "json";
xhr.onload = function () {
    if (xhr.status === 200) {
        // assign variables
        inhale_time = xhr.response.inhale_time;
        inhale_hold = xhr.response.inhale_hold;
        exhale_time = xhr.response.exhale_time;
        exhale_hold = xhr.response.exhale_hold;
        cycle_count = xhr.response.cycle_count;

        console.log(xhr.response);
    } else {
        console.log(xhr.statusText);
    }
};
xhr.onerror = function () {
    console.log("Error");
};
xhr.send();

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// animation logic
let feather = document.getElementById("feather");
let animate_scope = document.getElementById("scope");
let position = 0;

function feather_cycle(cycle) {
    // top and bottom of the feather box
    feather.style.transitionDuration = inhale_time + "s";
    feather.className = "float-object bottom";

    setTimeout(function () {
        feather.style.transitionDuration = inhale_time + "s";
        feather.className = "float-object top";

        setTimeout(() => {
            if (cycle == 0) {
                return;
            } else {
                console.log(cycle);
                return feather_cycle(cycle - 1);
            }
        }, exhale_time * 1000);
    }, exhale_time * 1000);
}
