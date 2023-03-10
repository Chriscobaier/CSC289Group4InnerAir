const first_name = document.getElementById('firstname');
const invalid_fname_summary = document.querySelector('.fname-validity-summary');

first_name.addEventListener('keyup', () => {
    let fname = first_name.value.length;

    if (fname >= 3 || fname == 0) {
        invalid_fname_summary.style.display = 'none';
    } else {
        invalid_fname_summary.style.display = 'flex';
        invalid_fname_summary.textContent = 'Name must be at least 3 characters.';
    }

});