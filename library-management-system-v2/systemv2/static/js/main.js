/* ============================================
   LibraryOS — Main JS
   Dark/Light mode + Animations
   ============================================ */

// ---- THEME TOGGLE ----
const html  = document.documentElement;
const toggle = document.getElementById('themeToggle');

// Load saved preference
const savedTheme = localStorage.getItem('los-theme') || 'dark';
html.setAttribute('data-theme', savedTheme);

if (toggle) {
    toggle.addEventListener('click', () => {
        const current = html.getAttribute('data-theme');
        const next    = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('los-theme', next);

        // Ripple effect
        toggle.classList.add('clicked');
        setTimeout(() => toggle.classList.remove('clicked'), 300);
    });
}

// ---- NAVBAR SCROLL EFFECT ----
const navbar = document.getElementById('navbar');
if (navbar) {
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
}

// ---- AUTO-DISMISS ALERTS ----
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.transition = 'opacity 0.5s, transform 0.5s';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 500);
    }, 4000);
});

// ---- COUNTER ANIMATION (hero stats) ----
function animateCount(el) {
    const target = parseInt(el.getAttribute('data-count'), 10);
    const duration = 1500;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        el.textContent = Math.floor(current);
    }, 16);
}

const counterEls = document.querySelectorAll('[data-count]');
if (counterEls.length) {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                animateCount(e.target);
                observer.unobserve(e.target);
            }
        });
    }, { threshold: 0.5 });
    counterEls.forEach(el => observer.observe(el));
}

// ---- SCROLL REVEAL ----
const revealEls = document.querySelectorAll('.feat-card, .stat-card, .form-container, .table-container');
const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.style.opacity = '1';
            e.target.style.transform = 'translateY(0)';
            revealObserver.unobserve(e.target);
        }
    });
}, { threshold: 0.1 });

revealEls.forEach((el, i) => {
    if (!el.closest('.hero')) {
        el.style.opacity    = '0';
        el.style.transform  = 'translateY(24px)';
        el.style.transition = `opacity 0.6s ${i * 0.05}s cubic-bezier(0.16,1,0.3,1), transform 0.6s ${i * 0.05}s cubic-bezier(0.16,1,0.3,1)`;
        revealObserver.observe(el);
    }
});

// ---- ACTIVE NAV LINK ----
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === '/' ? currentPath === '/' : currentPath.startsWith(href)) {
        link.style.color      = 'var(--text)';
        link.style.background = 'var(--border)';
    }
});
