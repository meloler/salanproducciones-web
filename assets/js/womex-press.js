(() => {
  'use strict';
  const section = document.querySelector('[data-womex-press]');
  if (!section) return;
  const track = section.querySelector('[data-press-track]');
  const cards = Array.from(track.children);
  const controls = section.querySelector('[data-press-controls]');
  const prev = section.querySelector('[data-press-prev]');
  const next = section.querySelector('[data-press-next]');
  const counter = section.querySelector('[data-press-counter]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  let announceTimer;
  const maxScroll = () => Math.max(0, track.scrollWidth - track.clientWidth);
  const step = () => cards.length > 1 ? cards[1].offsetLeft - cards[0].offsetLeft : track.clientWidth;
  const update = () => {
    frame = 0;
    const atStart = track.scrollLeft <= 2;
    const atEnd = track.scrollLeft >= maxScroll() - 2;
    prev.disabled = atStart;
    next.disabled = atEnd;
    const bounds = track.getBoundingClientRect();
    const visible = cards.map((card, i) => ({ rect: card.getBoundingClientRect(), i }))
      .filter(({ rect }) => Math.min(rect.right, bounds.right) - Math.max(rect.left, bounds.left) >= rect.width / 2);
    if (visible.length) {
      const first = visible[0].i + 1;
      const last = visible[visible.length - 1].i + 1;
      const label = first === last ? `${first} de ${cards.length}` : `${first}–${last} de ${cards.length}`;
      if (counter.textContent !== label) {
        clearTimeout(announceTimer);
        announceTimer = setTimeout(() => { counter.textContent = label; }, 160);
      }
    }
  };
  const move = (left) => track.scrollTo({ left: Math.min(maxScroll(), Math.max(0, left)), behavior: reduceMotion.matches ? 'auto' : 'smooth' });
  prev.addEventListener('click', () => move(track.scrollLeft - step()));
  next.addEventListener('click', () => move(track.scrollLeft + step()));
  track.addEventListener('keydown', (event) => {
    if (event.target !== track) return;
    const targets = { ArrowLeft: track.scrollLeft - step(), ArrowRight: track.scrollLeft + step(), Home: 0, End: maxScroll() };
    if (!(event.key in targets)) return;
    event.preventDefault();
    move(targets[event.key]);
  });
  track.addEventListener('scroll', () => { if (!frame) frame = requestAnimationFrame(update); }, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  controls.hidden = false;
  update();
})();
