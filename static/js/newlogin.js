document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerButtons = document.querySelectorAll('.register-btn');
    const loginButtons = document.querySelectorAll('.login-btn');

    if (!container) return;

    registerButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            container.classList.add('active');
        });
    });

    loginButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            container.classList.remove('active');
        });
    });

    const passwordToggles = document.querySelectorAll('.toggle-password');
    passwordToggles.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            let input = targetId ? document.getElementById(targetId) : null;

            if (!input) {
                const shell = btn.closest('.input-shell');
                input = shell ? shell.querySelector('input, textarea') : null;
            }

            if (!input) return;

            const reveal = input.getAttribute('type') === 'password';
            input.setAttribute('type', reveal ? 'text' : 'password');
            btn.setAttribute('aria-pressed', reveal ? 'true' : 'false');
            btn.setAttribute('aria-label', reveal ? 'Hide password' : 'Show password');

            const icon = btn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-eye', !reveal);
                icon.classList.toggle('fa-eye-slash', reveal);
            }
        });
    });
});
