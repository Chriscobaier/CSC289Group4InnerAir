const email = document.getElementById('email');
const invalid_email_summary = document.querySelector('.email-validity-summary');

email.addEventListener('keyup', () => {
    let regExp = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (email.value.match(regExp) || email.value == "") {
        invalid_email_summary.style.display = 'none';
    } else {
        invalid_email_summary.style.display = 'flex';
        invalid_email_summary.textContent = 'You have entered an invalid email address.';
    }

});