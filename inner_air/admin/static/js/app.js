const toggler_btn = document.querySelector('.navbar-toggle');
const html = document.querySelector('html');

toggler_btn.addEventListener('click', () => {
        toggler_btn.classList.toggle('toggled');
        html.classList.toggle('nav-open');
});

/* =============== TAB LIST ============== */
const tabs = document.querySelectorAll('[data-tab-target]');
const tab_contents = document.querySelectorAll('[data-tab-content]');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = document.querySelector(tab.dataset.tabTarget);

        tab_contents.forEach(tab_content => {
            tab_content.classList.remove('active');
        });

        tabs.forEach(tab => {
            tab.classList.remove('active');
        });

        tab.classList.add('active');
        target.classList.add('active');
    });
});
