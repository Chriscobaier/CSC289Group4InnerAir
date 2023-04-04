let list_sections = document.getElementsByClassName("name");
let list_plate = document.getElementsByClassName("plate");

function expander(event) {
    let exercise_card = event.target.closest(".plate").querySelector(".description");
    
    if (exercise_card.style.display == "none" || !exercise_card.style.display) {
        exercise_card.style.display = "block";
    } else {
        exercise_card.style.display = "none";
    }
}

for (let i = 0; i < list_sections.length; i++) {
    console.log(list_sections[i])
    list_sections[i].addEventListener('click', expander);
    list_plate[i].addEventListener('click', expander);
  }