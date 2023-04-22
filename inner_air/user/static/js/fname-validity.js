const first_name = document.getElementById('firstname');
const invalid_fname_summary = document.querySelector('.fname-validity-summary');

first_name.addEventListener('keyup', () => {
    let fname = first_name.value.length;

    if (fname < 64 || fname == 0) {
        invalid_fname_summary.style.display = 'none';
    } else {
        invalid_fname_summary.style.display = 'flex';
        invalid_fname_summary.textContent = 'Name must be less than 64 characters.';
    }

});



document.querySelector('input[name="anonymous_mode"]').addEventListener('mouseover', function() {
  document.querySelector('.extra-info').style.display = 'flex';
});
document.querySelector('input[name="anonymous_mode"]').addEventListener('mouseout', function() {
  document.querySelector('.extra-info').style.display = 'none';
});
