// Tailwind config (must run BEFORE Tailwind CDN finishes loading)
window.tailwind = window.tailwind || {};
window.tailwind.config = {
    darkMode: 'class',
};

// Apply saved theme immediately (before render)
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