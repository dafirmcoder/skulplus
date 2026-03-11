document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerButtons = document.querySelectorAll('.register-btn');
    const loginButtons = document.querySelectorAll('.login-btn');
    const authModal = document.getElementById('authModal');
    const openAuthButtons = document.querySelectorAll('[data-open-auth]');
    const closeAuthButtons = document.querySelectorAll('[data-close-auth]');

    const openModal = (mode) => {
        if (container && mode === 'signup') {
            container.classList.add('active');
        } else if (container) {
            container.classList.remove('active');
        }
        if (authModal) {
            authModal.classList.add('open');
            authModal.setAttribute('aria-hidden', 'false');
            document.body.classList.add('auth-modal-open');
        }
    };

    const closeModal = () => {
        if (!authModal) return;
        authModal.classList.remove('open');
        authModal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('auth-modal-open');
    };

    openAuthButtons.forEach(btn => {
        btn.addEventListener('click', (event) => {
            if (!authModal) return;
            event.preventDefault();
            const target = (btn.dataset.openAuth || 'login').toLowerCase();
            openModal(target === 'signup' ? 'signup' : 'login');
        });
    });

    closeAuthButtons.forEach(btn => {
        btn.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeModal();
        }
    });

    if (!container) return;

    registerButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            container.classList.add('active');
            if (authModal) {
                authModal.classList.add('open');
                authModal.setAttribute('aria-hidden', 'false');
                document.body.classList.add('auth-modal-open');
            }
        });
    });

    loginButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            container.classList.remove('active');
            if (authModal) {
                authModal.classList.add('open');
                authModal.setAttribute('aria-hidden', 'false');
                document.body.classList.add('auth-modal-open');
            }
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

    if (authModal && authModal.classList.contains('open')) {
        document.body.classList.add('auth-modal-open');
    }
});
