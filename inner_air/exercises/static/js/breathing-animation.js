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
// animation logic
let feather = document.getElementById("feather");
let animate_scope = document.getElementById("scope");
let timer = document.getElementById("timer");
let position = 0;

/* Changes contents of the timer */
function timer_count(state, time, timeout) {
    setTimeout(() => {
        timer.textContent = state + " for " + time + " seconds";
        time--;
        let id = setInterval(() => {
            timer.textContent = state + " for " + time + " seconds";
            if (time == 1) {
                clearInterval(id);
            }
            time--;
        }, 1000);
    }, timeout);
}

/* Sets timer cycle */
function set_timer(ih_time, ih_hold, ex_time, ex_hold) {
    timer_count("Inhale", ih_time);
    timer_count("Inhale Hold", ih_time, ih_time * 1000);
    timer_count("Exhale", ih_time, (ih_time + ih_hold) * 1000);
    timer_count("Exhale Hold", ih_time, (ih_time + ih_hold + ex_time) * 1000);
}

/* Plays Inhale animation */
function inhale() {
    feather.style.transitionDuration = inhale_time + "s";
    feather.className = "float-object bottom";
}

/* Plays exhale animation with timing for inhale hold */
function exhale() {
    setTimeout(() => {
        feather.style.transitionDuration = inhale_time + "s";
        feather.className = "float-object top";
    }, inhale_hold * 1000);
}

/* Loops the animation */
function feather_cycle(cycle) {
    set_timer(inhale_time, inhale_hold, exhale_time, exhale_hold);
    inhale();
    setTimeout(exhale, inhale_time * 1000);

    // repeat cycle once animation is done
    setTimeout(() => {
        if (cycle == 0) {
            return;
        } else {
            return feather_cycle(cycle - 1);
        }
    }, (inhale_time + inhale_hold + exhale_time + inhale_hold) * 1000);
}
