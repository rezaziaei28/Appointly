// ============================================================
// TAILWIND CONFIG (must run before body renders)
// ============================================================
tailwind.config = {
    darkMode: 'class',
};


// ============================================================
// APPLY SAVED THEME (before page renders - no flash)
// ============================================================
(function applyTheme() {
    const saved = localStorage.getItem('theme');

    if (saved === 'dark') {
        document.documentElement.classList.add('dark');
    } else if (saved === 'light') {
        document.documentElement.classList.remove('dark');
    } else {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
    }
})();


// ============================================================
// DOM READY
// ============================================================
document.addEventListener('DOMContentLoaded', () => {

    // --------------------------------------------------------
    // THEME TOGGLE
    // --------------------------------------------------------
    const themeToggle = document.getElementById('themeToggle');

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const html = document.documentElement;
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }


    // --------------------------------------------------------
    // MOBILE MENU
    // --------------------------------------------------------
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
        });

        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
            });
        });
    }


    // --------------------------------------------------------
    // PASSWORD SHOW / HIDE (eye icon)
    // --------------------------------------------------------
    const passwordToggles = document.querySelectorAll('.password-toggle');

    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const wrapper = toggle.closest('.password-wrapper');
            if (!wrapper) return;

            const input = wrapper.querySelector('input');
            if (!input) return;

            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';

            toggle.textContent = isPassword ? '🙈' : '👁';
        });
    });


    // --------------------------------------------------------
    // OTP INPUTS (auto-focus next, paste, backspace)
    // --------------------------------------------------------
    const otpInputs = document.querySelectorAll('.otp-input');

    if (otpInputs.length > 0) {

        otpInputs.forEach((input, index) => {

            // When user types a digit → go to next input
            input.addEventListener('input', (e) => {
                const value = e.target.value;

                if (value.length > 1) {
                    e.target.value = value.slice(-1);
                }

                if (e.target.value && index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            });

            // Backspace on empty input → go to previous
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && !e.target.value && index > 0) {
                    otpInputs[index - 1].focus();
                }
            });

            // Arrow keys navigation
            input.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft' && index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
                if (e.key === 'ArrowRight' && index > 0) {
                    otpInputs[index - 1].focus();
                }
            });
        });

        // Paste whole code into first input → spread across all
        otpInputs[0].addEventListener('paste', (e) => {
            e.preventDefault();
            const pasted = (e.clipboardData || window.clipboardData).getData('text');
            const digits = pasted.replace(/\D/g, '').slice(0, otpInputs.length);

            digits.split('').forEach((digit, i) => {
                otpInputs[i].value = digit;
            });

            const lastIndex = Math.min(digits.length, otpInputs.length - 1);
            otpInputs[lastIndex].focus();
        });

        // Focus first input on load
        otpInputs[0].focus();
    }

    // --------------------------------------------------------
    // OTP RESEND TIMER (2 minutes)
    // --------------------------------------------------------
    const timerElement = document.getElementById('timer');
    const resendBtn = document.getElementById('resend-btn');
    if (timerElement && resendBtn) {
        let timeLeft = 120; // 2 minutes in seconds
        resendBtn.disabled = true;
        resendBtn.classList.add('cursor-not-allowed');
        
        const countdown = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            
            // Format time to 02:00
            timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                clearInterval(countdown);
                resendBtn.innerHTML = `<a href="/accounts/login/" class="text-teal-600 hover:underline">ارسال مجدد کد</a>`;
                resendBtn.disabled = false;
                resendBtn.classList.remove('cursor-not-allowed', 'text-slate-500');
                resendBtn.classList.add('text-teal-600', 'hover:underline');
            }
            timeLeft--;
        }, 1000);
    }


});