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
    position = animate_scope.getBoundingClientRect().top * 2 - 150;
    let bottom = position + 400;
    let top = position;
    feather.style.top = position + "px";
    console.log(top);

    let inhale_time_id = setInterval(function () {
        console.log(feather);
        position += 10;
        feather.style.top = position + "px";

        if (position == bottom) {
            clearInterval(inhale_time_id);

            let exhale_time_id = setInterval(function () {
                position -= 10;
                feather.style.top = position + "px";

                if (position == top) {
                    clearInterval(exhale_time_id);
                }
            }, 100);
        }
    }, 100);
}
