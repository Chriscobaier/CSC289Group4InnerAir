const password = document.getElementById('password');

const indicator = document.querySelector('.indicator');
const password_weak = document.querySelector('.password-validity-weak');
const password_medium = document.querySelector('.password-validity-medium');
const password_strong = document.querySelector('.password-validity-strong');
const password_summary = document.querySelector('.password-validity-summary');

function CheckStrength(password) {
    let strength = 0;

    /* if password is greater than 7. */
    if (password.length > 7) {
        strength++;
    }
    if (/[A-Z]/.test(password)) {
        strength++;
    }
    if (/[0-9]/.test(password)) {
        strength++;
    }
    if (/[A-Za-z-0-8]/.test(password)) {
        strength++;
    }
    return strength;
}

password.addEventListener('keyup', () => {
    let passwrd = password.value;
    let strength = CheckStrength(passwrd);

    let space_regExp = /^\s+$/;
    let space = passwrd.match(space_regExp);

    if (passwrd != "" && !space) {
        indicator.style.display = 'flex';

        if (strength <= 2) {
            password_weak.classList.add('active');
            password_summary.style.display = 'flex';
            password_summary.textContent = 'Your password is too short';
            password_summary.classList.add('password-validity-weak');

            password_medium.classList.remove('active');
            password_medium.style.backgroundColor = '#D3D3D3';
            password_summary.classList.remove('password-validity-medium');

            password_strong.classList.remove('active');
            password_summary.classList.remove('password-validity-strong');
        }
        else if (strength >= 2 && strength < 4) {
            password_weak.classList.remove('active');
            password_weak.style.backgroundColor = '#FFD33D';
            password_summary.classList.remove('password-validity-weak');

            password_medium.classList.add('active');
            password_summary.style.display = 'flex';
            password_summary.textContent = 'Password needs a number and uppercase letter';
            password_summary.classList.add('password-validity-medium');

            password_strong.classList.remove('active');
            password_summary.classList.remove('password-validity-strong');
        } else {
            password_weak.classList.remove('active');
            password_weak.style.backgroundColor = '#2DA44E';
            password_summary.classList.remove('password-validity-weak');

            password_medium.classList.remove('active');
            password_medium.style.backgroundColor = '#2DA44E';
            password_summary.classList.remove('password-validity-medium');

            password_strong.classList.add('active');
            password_summary.style.display = 'flex';
            password_summary.textContent = 'Password is strong';
            password_summary.classList.add('password-validity-strong');
        }
    } else {
        indicator.style.display = 'none';
        password_summary.style.display = 'none';
    }

});
