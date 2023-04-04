const modal = document.querySelector(".modal");
const btn = document.querySelector(".button");

window.addEventListener("load", function () {
  setTimeout(function open(event) {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  }, 200);
});

btn.addEventListener(
    "click", () => {
        btn.classList.add("spinner");

        setTimeout(() => {
            btn.classList.remove("spinner");
        }, 6000);
    }, false
);
