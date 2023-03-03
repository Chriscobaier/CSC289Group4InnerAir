//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// button animation
let start_button = document.getElementById("start-button");
start_button.addEventListener("click", switch_button);

// changes to stop/start state of the button
function switch_button() {
    if (start_button.classList.contains("button--green")) {
        start_button.className = "button--red";
        start_button.textContent = "Stop";
        animate_feather();
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
let exhale;
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
        exhale = xhr.response.exhale_hold;
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

function animate_feather() {
    let cycle_length = (inhale_time + exhale_time) * 1000 + 2;

    // should be repeating the cycle's, but it doesn't
    let cycle_id = setInterval(feather_cycle(), cycle_length);

    // clear interval after a certain all cycles have past
    clearInterval(cycle_id, cycle_length * cycle_count);
}

function feather_cycle() {
    // top and bottom of the feather box
    let bottom = animate_scope.offsetHeight / 2;
    let top = bottom * -1;
    feather.style.top = top + "px";

    // give transition a certain amount of time to finish
    feather.style.transition = "all " + inhale_time + "s ease-in-out";

    // wait a millisecond, in order for functions to not override each other
    setTimeout(function () {
        feather.style.top = bottom + "px";
    }, 1);

    // waits for down motion to finnish
    setTimeout(function () {
        feather.style.transition = "all " + exhale_time + "s ease-in-out";
        setTimeout(function () {
            feather.style.top = top + "px";
        }, 1);
    }, exhale_time * 1000);
}
