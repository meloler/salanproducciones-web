/* Progressive enhancement: every image remains a normal full-size link without JS. */
(() => {
  'use strict';
  const links = Array.from(document.querySelectorAll('[data-poseidon-photo]'));
  const dialog = document.querySelector('#poseidon-lightbox');
  if (!links.length || !dialog || typeof dialog.showModal !== 'function') return;
  const image = dialog.querySelector('.poseidon-dialog-image');
  const caption = dialog.querySelector('.poseidon-dialog-caption');
  const count = dialog.querySelector('[data-photo-count]');
  const close = dialog.querySelector('[data-photo-close]');
  let index = 0, returnFocus = null, previousOverflow = '';
  function show(next) {
    index = (next + links.length) % links.length;
    const thumbnail = links[index].querySelector('img');
    image.src = links[index].href;
    image.alt = thumbnail.alt;
    caption.textContent = thumbnail.alt;
    count.textContent = `Fotografía ${index + 1} de ${links.length}`;
  }
  links.forEach((link, position) => link.addEventListener('click', (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); returnFocus = link; previousOverflow = document.body.style.overflow;
    show(position); dialog.showModal(); document.body.style.overflow = 'hidden'; close.focus();
  }));
  close.addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-photo-prev]').addEventListener('click', () => show(index - 1));
  dialog.querySelector('[data-photo-next]').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {event.preventDefault(); show(index + 1);}
    if (event.key === 'ArrowLeft') {event.preventDefault(); show(index - 1);}
    if (event.key === 'Home') {event.preventDefault(); show(0);}
    if (event.key === 'End') {event.preventDefault(); show(links.length - 1);}
  });
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = previousOverflow;
    if (returnFocus) returnFocus.focus({preventScroll: true});
  });
})();
