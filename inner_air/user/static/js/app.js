const modal = document.querySelector('.modal');

window.addEventListener('load', function() {
    setTimeout(
        function open(event) {
            modal.style.display = 'flex';
        },
        1000
    )
});

