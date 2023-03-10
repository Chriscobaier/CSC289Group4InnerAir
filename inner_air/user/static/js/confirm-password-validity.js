const confirm_password = document.getElementById('confirm_password');
const invalid_cpassword_summary = document.querySelector('.cpassword-validity-summary');


confirm_password.addEventListener('keyup', () => {
    let passwrd = password.value;
    let confirm_passwrd = confirm_password.value;


    if (password.length != 0) {
        if (passwrd == confirm_passwrd || confirm_passwrd == "") {
            invalid_cpassword_summary.style.display = 'none';
        } else {
            invalid_cpassword_summary.style.display = 'flex';
            invalid_cpassword_summary.textContent = 'Field must be equal to password.'
        }
    }
});
