// static/js/main.js
// Pure vanilla JS — no frameworks. Works with Django's server-rendered HTML.

document.addEventListener('DOMContentLoaded', () => {

  // ── CART SIDEBAR ──
  const cartOverlay  = document.getElementById('cartOverlay');
  const cartSidebar  = document.getElementById('cartSidebar');
  const cartToggle   = document.getElementById('cartToggle');
  const cartClose    = document.getElementById('cartClose');
  const cartContinue = document.getElementById('cartContinue');

  function openCart()  { cartSidebar?.classList.add('open'); cartOverlay?.classList.add('open'); }
  function closeCart() { cartSidebar?.classList.remove('open'); cartOverlay?.classList.remove('open'); }

  cartToggle?.addEventListener('click', () =>
    cartSidebar?.classList.contains('open') ? closeCart() : openCart()
  );
  cartClose?.addEventListener('click', closeCart);
  cartContinue?.addEventListener('click', closeCart);
  cartOverlay?.addEventListener('click', closeCart);

  // Cart qty forms — submit via fetch so page doesn't reload
  // Django view at cart:update returns a redirect; we reload the sidebar portion
  document.querySelectorAll('.qty-form').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const data = new FormData(form);
      fetch('/cart/update/', {
        method: 'POST',
        body: data,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      }).then(() => location.reload());
      // NOTE: Replace location.reload() with a partial re-render
      // once you build the cart update view. For now this works fine.
    });
  });

  // Remove forms — let them submit normally (POST → redirect)
  // They are standard <form method="POST"> so no JS needed.

  // ── HAMBURGER MENU ──
  const menuToggle = document.getElementById('menuToggle');
  const navLinks   = document.getElementById('navLinks');
  menuToggle?.addEventListener('click', () => navLinks?.classList.toggle('open'));

  // ── SEARCH TOGGLE ──
  const searchToggle = document.getElementById('searchToggle');
  const searchBar    = document.getElementById('searchBar');
  const searchInput  = document.querySelector('#searchBar input');
  searchToggle?.addEventListener('click', () => {
    searchBar?.classList.toggle('open');
    if (searchBar?.classList.contains('open')) searchInput?.focus();
  });

  // ── HERO SLIDER ──
  const slides = document.querySelectorAll('.hero-slide');
  const dotsContainer = document.getElementById('heroDots');
  const prevBtn = document.getElementById('heroPrev');
  const nextBtn = document.getElementById('heroNext');
  let currentSlide = 0;
  let slideTimer;

  if (slides.length > 0 && dotsContainer) {
    // Build dots
    slides.forEach((_, i) => {
      const dot = document.createElement('span');
      dot.className = 'dot' + (i === 0 ? ' active' : '');
      dot.addEventListener('click', () => goSlide(i));
      dotsContainer.appendChild(dot);
    });

    function goSlide(n) {
      slides[currentSlide].classList.remove('active');
      dotsContainer.children[currentSlide].classList.remove('active');
      currentSlide = (n + slides.length) % slides.length;
      slides[currentSlide].classList.add('active');
      dotsContainer.children[currentSlide].classList.add('active');
      resetTimer();
    }
    function resetTimer() {
      clearInterval(slideTimer);
      slideTimer = setInterval(() => goSlide(currentSlide + 1), 5000);
    }

    prevBtn?.addEventListener('click', () => goSlide(currentSlide - 1));
    nextBtn?.addEventListener('click', () => goSlide(currentSlide + 1));
    resetTimer();
  }

  // ── COUNTDOWN TIMER ──
  // Used on home page deal banner and deals page.
  // HTML element must have data-end="ISO date string"
  function startCountdown(el) {
    const endDate = new Date(el.dataset.end);
    function tick() {
      const diff = endDate - new Date();
      if (diff <= 0) {
        el.innerHTML = '<span style="color:var(--accent)">Deal Ended</span>';
        return;
      }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      el.innerHTML = `
        <div class="timer-unit"><span>${d}</span><label>Days</label></div>
        <div class="timer-sep">:</div>
        <div class="timer-unit"><span>${String(h).padStart(2,'0')}</span><label>Hrs</label></div>
        <div class="timer-sep">:</div>
        <div class="timer-unit"><span>${String(m).padStart(2,'0')}</span><label>Min</label></div>
        <div class="timer-sep">:</div>
        <div class="timer-unit"><span>${String(s).padStart(2,'0')}</span><label>Sec</label></div>`;
    }
    tick();
    setInterval(tick, 1000);
  }
  document.querySelectorAll('.deal-timer[data-end]').forEach(startCountdown);

  // ── AUTO-DISMISS MESSAGES ──
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => alert.remove(), 4000);
  });

  // ── WISHLIST FORM — show flash without reload (optional enhancement) ──
  // Standard <form method="POST"> wishlist forms work fine without JS.
  // Django redirects back to same page via ?next= param.

});
