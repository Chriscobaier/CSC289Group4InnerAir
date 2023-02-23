const modal = document.querySelector('.modal');

window.addEventListener('load', function() {
    setTimeout(
        function open(event) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        },
        100
    )
});

