/* =============================================
   SALÁN PRODUCCIONES — main.js
   ============================================= */

(function () {
  'use strict';

  /* --- Nav scroll shadow --- */
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    });
  }

  /* --- Mobile nav toggle --- */
  const toggle = document.querySelector('.nav-toggle');
  const mobileMenu = document.querySelector('.nav-mobile');
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      const open = toggle.classList.toggle('open');
      mobileMenu.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        toggle.classList.remove('open');
        mobileMenu.classList.remove('open');
      });
    });
  }

  /* --- Active nav link --- */
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-links a, .nav-mobile a').forEach(a => {
    const href = a.getAttribute('href').replace(/\/$/, '') || '/';
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      a.classList.add('active');
    }
  });

  /* --- Scroll reveal --- */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => io.observe(el));
  }


  function responsivePosterAttrs(src, sizes) {
    if (!src || !src.includes('/conciertos/2026/') || !src.endsWith('/poster.webp')) return '';
    const base = src.replace('/poster.webp', '/poster');
    return `srcset="${base}-320.webp 320w, ${base}-480.webp 480w, ${base}-768.webp 768w" sizes="${sizes}" decoding="async"`;
  }

  /* --- Dynamic copyright year --- */
  document.querySelectorAll('.footer-copy').forEach(el => {
    el.innerHTML = el.innerHTML.replace(/\d{4}/, new Date().getFullYear());
  });

  /* --- Newsletter form (Loops) --- */
  function loopsSubmitHandler(event) {
    event.preventDefault();
    var container = event.target.parentNode;
    var form = container.querySelector('.newsletter-form');
    var emailInput = container.querySelector('input[type="email"]');
    var nameInput = container.querySelector('input[name="firstName"]');
    var allInputs = container.querySelectorAll('.newsletter-form-input');
    var success = container.querySelector('.newsletter-success');
    var errorContainer = container.querySelector('.newsletter-error');
    var errorMessage = container.querySelector('.newsletter-error-message');
    var backButton = container.querySelector('.newsletter-back-button');
    var submitButton = container.querySelector('.newsletter-form-button');
    var loadingButton = container.querySelector('.newsletter-loading-button');

    var hideInputs = function() { allInputs.forEach(function(el) { el.style.display = 'none'; }); };

    var rateLimit = function() {
      errorContainer.style.display = 'flex';
      errorMessage.innerText = 'Demasiados intentos, espera un momento.';
      submitButton.style.display = 'none';
      hideInputs();
      backButton.style.display = 'block';
    };

    var time = new Date();
    var timestamp = time.valueOf();
    var previousTimestamp = localStorage.getItem('loops-form-timestamp');
    if (previousTimestamp && Number(previousTimestamp) + 60000 > timestamp) { rateLimit(); return; }
    localStorage.setItem('loops-form-timestamp', timestamp);

    submitButton.style.display = 'none';
    loadingButton.style.display = 'inline-flex';

    var firstName = nameInput && nameInput.value.trim() ? '&firstName=' + encodeURIComponent(nameInput.value.trim()) : '';
    var formBody = 'userGroup=&mailingLists=&email=' + encodeURIComponent(emailInput.value) + firstName;

    fetch(event.target.action, {
      method: 'POST',
      body: formBody,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
      .then(function(res) { return [res.ok, res.json(), res]; })
      .then(function(arr) {
        var ok = arr[0], dataPromise = arr[1], res = arr[2];
        if (ok) {
          success.style.display = 'flex';
          form.reset();
        } else {
          dataPromise.then(function(data) {
            errorContainer.style.display = 'flex';
            errorMessage.innerText = data.message ? data.message : res.statusText;
          });
        }
      })
      .catch(function(error) {
        if (error.message === 'Failed to fetch') { rateLimit(); return; }
        errorContainer.style.display = 'flex';
        if (error.message) errorMessage.innerText = error.message;
        localStorage.setItem('loops-form-timestamp', '');
      })
      .finally(function() {
        hideInputs();
        loadingButton.style.display = 'none';
        backButton.style.display = 'block';
      });
  }

  function loopsResetHandler(event) {
    var container = event.target.parentNode;
    var allInputs = container.querySelectorAll('.newsletter-form-input');
    var success = container.querySelector('.newsletter-success');
    var errorContainer = container.querySelector('.newsletter-error');
    var errorMessage = container.querySelector('.newsletter-error-message');
    var backButton = container.querySelector('.newsletter-back-button');
    var submitButton = container.querySelector('.newsletter-form-button');
    success.style.display = 'none';
    errorContainer.style.display = 'none';
    errorMessage.innerText = 'Algo salió mal, inténtalo de nuevo.';
    backButton.style.display = 'none';
    allInputs.forEach(function(el) { el.style.display = 'flex'; });
    submitButton.style.display = 'flex';
  }

  document.querySelectorAll('.newsletter-form-container').forEach(function(container) {
    if (container.classList.contains('newsletter-handlers-added')) return;
    container.querySelector('.newsletter-form').addEventListener('submit', loopsSubmitHandler);
    container.querySelector('.newsletter-back-button').addEventListener('click', loopsResetHandler);
    container.classList.add('newsletter-handlers-added');
  });

  /* --- Contact form --- */
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = contactForm.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = '✓ Mensaje enviado';
        btn.style.background = '#2ecc71';
        btn.style.borderColor = '#2ecc71';
        btn.style.color = '#fff';
      }
    });
  }

  /* --- Dynamic Concert Loading (Upcoming) --- */
  const upcomingGrid = document.getElementById('upcoming-grid');
  const concertsTimeline = document.getElementById('concerts-timeline');
  
  if (upcomingGrid || concertsTimeline) {
    fetch('/conciertos.json')
      .then(res => res.json())
      .then(data => {
        const today = new Date().toISOString().split('T')[0];
        
        // 1. Render Upcoming — solo si el grid está vacío (sin cards estáticas en el HTML)
        if (upcomingGrid && upcomingGrid.children.length === 0) {
          const upcoming = data.filter(c => c.dateISO >= today).sort((a, b) => a.dateISO.localeCompare(b.dateISO));
          
          if (upcoming.length === 0) {
            upcomingGrid.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: var(--muted);">No hay conciertos próximos programados en este momento. ¡Atento a nuestras redes!</p>';
          } else {
            let html = '';
            upcoming.forEach(c => {
              const buttonHtml = c.disabled 
                ? `<button class="btn btn-outline" style="flex:1" disabled>${c.buttonLabel}</button>`
                : `<a href="${c.linkBuy}" class="btn btn-primary" style="flex:2;text-align:center" target="_blank" rel="noopener" aria-label="${c.buyAria}">${c.buttonLabel}</a>`;
                
              html += `
                <article class="concert-card reveal">
                  <div class="concert-card-img">
                    <img src="${c.image.replace('/poster.webp', '/poster-480.webp')}" ${responsivePosterAttrs(c.image, '(max-width: 700px) 92vw, (max-width: 1100px) 45vw, 320px')} alt="Cartel ${c.title} — ${c.dateDisplay}" loading="lazy" width="400" height="533">
                    <span class="concert-card-badge">${c.badge}</span>
                  </div>
                  <div class="concert-card-body">
                    <div class="concert-card-date">${c.dateDisplay}</div>
                    <h3 class="concert-card-title">${c.title}</h3>
                    <p class="concert-card-venue">${c.venue}</p>
                    <p class="concert-card-price">${c.price || ''}</p>
                    <div style="display:flex;gap:8px;margin-top:8px">
                      <a href="${c.linkInfo}" class="btn btn-outline" style="flex:1;text-align:center">+ Info</a>
                      ${buttonHtml}
                    </div>
                  </div>
                </article>
              `;
            });
            upcomingGrid.innerHTML = html;
            
            setTimeout(() => {
              const io = new IntersectionObserver((entries) => {
                entries.forEach(e => {
                  if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    io.unobserve(e.target);
                  }
                });
              }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
              upcomingGrid.querySelectorAll('.reveal').forEach(el => io.observe(el));
            }, 100);
          }
        }

        // 2. Render Past (Anteriores) dynamically on top of existing ones
        if (concertsTimeline) {
          const past = data.filter(c => c.dateISO < today).sort((a, b) => b.dateISO.localeCompare(a.dateISO)); // newest first
          
          if (past.length > 0) {
            // Group by year
            const grouped = {};
            past.forEach(c => {
              const year = c.dateISO.split('-')[0];
              if (!grouped[year]) grouped[year] = [];
              grouped[year].push(c);
            });

            // For each year, find or create the year block and prepend the new past concerts
            Object.keys(grouped).sort((a, b) => b - a).forEach(year => {
              let yearBlock = concertsTimeline.querySelector(`.timeline-year-group[data-year="${year}"]`);
              let gridContainer;
              
              if (!yearBlock) {
                // Create new year block if it doesn't exist
                yearBlock = document.createElement('div');
                yearBlock.className = 'timeline-year-group';
                yearBlock.setAttribute('data-year', year);
                yearBlock.innerHTML = `
                  <div class="timeline-year"><span>${year}</span></div>
                  <div class="timeline-grid"></div>
                `;
                // Insert at the beginning
                concertsTimeline.insertBefore(yearBlock, concertsTimeline.firstChild);
                gridContainer = yearBlock.querySelector('.timeline-grid');
              } else {
                gridContainer = yearBlock.querySelector('.timeline-grid');
              }

              // Prepend cards
              // We reverse because we prepend each one, so we want the newest to be at the very top
              [...grouped[year]].reverse().forEach(c => {
                const shortDate = new Date(c.dateISO).toLocaleString('es-ES', { month: 'short', year: 'numeric' }).replace('.', '');
                
                // Avoid duplicates from the static timeline. Responsive images may use
                // poster-480.webp/poster-768.webp, so comparing only the filename is not enough.
                const normalize = value => (value || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, ' ').trim();
                const existingText = normalize(gridContainer.innerText);
                const imageDir = c.image.split('/poster.webp')[0];
                const existingImgs = Array.from(gridContainer.querySelectorAll('img')).map(img => img.currentSrc || img.src);
                const isDuplicate = existingImgs.some(src => src.includes(imageDir)) || (existingText.includes(normalize(c.title)) && existingText.includes(normalize(c.venue)));
                
                if (!isDuplicate) {
                  const card = document.createElement('div');
                  card.className = 'timeline-card';
                  card.innerHTML = `
                    <div class="timeline-card-img"><img src="${c.image.replace('/poster.webp', '/poster-480.webp')}" ${responsivePosterAttrs(c.image, '(max-width: 700px) 44vw, (max-width: 1100px) 30vw, 240px')} alt="${c.title}" loading="lazy" width="400" height="560"></div>
                    <div class="timeline-card-date">${shortDate}</div>
                    <div class="timeline-card-name">${c.title}</div>
                    <div class="timeline-card-venue">${c.venue}</div>
                  `;
                  gridContainer.insertBefore(card, gridContainer.firstChild);
                }
              });
            });
          }
        }
      })
      .catch(err => console.error('Error loading concerts:', err));
  }

})();
