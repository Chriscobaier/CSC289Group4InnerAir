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

function inhale() {
    feather.style.transitionDuration = inhale_time + "s";
    feather.className = "float-object bottom";
    console.log("inhale");
}

function exhale() {
    setTimeout(() => {
        feather.style.transitionDuration = inhale_time + "s";
        feather.className = "float-object top";
    }, inhale_hold * 1000);
}

function feather_cycle(cycle) {
    inhale();
    setTimeout(exhale, inhale_time * 1000);

    // repeat cycle once animation is done
    setTimeout(() => {
        if (cycle == 0) {
            return;
        } else {
            console.log(cycle);
            return feather_cycle(cycle - 1);
        }
    }, (inhale_time + inhale_hold + exhale_time + inhale_hold) * 1000);
}
