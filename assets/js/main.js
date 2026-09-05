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

  function localISODate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function concertEndDate(concert) {
    return concert.endDateISO || concert.dateISO;
  }

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, char => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[char]));
  }

  function stripHtml(value) {
    return String(value || '').replace(/<[^>]*>/g, '');
  }

  function currentLanguage() {
    const path = window.location.pathname;
    if (path === '/en' || path.startsWith('/en/')) return 'en';
    if (path === '/de' || path.startsWith('/de/')) return 'de';
    return 'es';
  }

  const lang = currentLanguage();
  const uiCopy = {
    es: {
      noUpcoming: 'No hay conciertos próximos programados en este momento. ¡Atento a nuestras redes!',
      info: '+ Info',
      poster: 'Cartel',
      contactSent: '✓ Mensaje enviado'
    },
    en: {
      noUpcoming: 'There are no upcoming concerts scheduled right now. Follow our channels for new dates.',
      info: '+ Info',
      poster: 'Poster',
      contactSent: 'Message sent'
    },
    de: {
      noUpcoming: 'Zurzeit sind keine kommenden Konzerte geplant. Folge unseren Kanälen für neue Termine.',
      info: '+ Info',
      poster: 'Plakat',
      contactSent: 'Nachricht gesendet'
    }
  };
  const t = uiCopy[lang] || uiCopy.es;

  function insertLanguageSwitcher() {
    const alternates = {};
    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(link => {
      const code = link.getAttribute('hreflang');
      if (code === 'es' || code === 'en' || code === 'de') {
        alternates[code] = link.getAttribute('href');
      }
    });
    if (!alternates.es && !alternates.en && !alternates.de) return;

    function buildSwitcher() {
      const wrap = document.createElement('div');
      wrap.className = 'language-switcher';
      wrap.setAttribute('aria-label', 'Selector de idioma');
      ['es', 'en', 'de'].forEach((code, index) => {
        if (index > 0) {
          const sep = document.createElement('span');
          sep.textContent = '|';
          wrap.appendChild(sep);
        }
        const a = document.createElement('a');
        a.href = alternates[code] || (code === 'es' ? '/' : '/' + code + '/');
        a.lang = code;
        a.hreflang = code;
        a.textContent = code.toUpperCase();
        if (code === lang) {
          a.className = 'active';
          a.setAttribute('aria-current', 'true');
        }
        wrap.appendChild(a);
      });
      return wrap;
    }

    const desktopNav = document.querySelector('.nav-links');
    if (desktopNav && !desktopNav.parentNode.querySelector('.language-switcher')) {
      desktopNav.insertAdjacentElement('afterend', buildSwitcher());
    }
    const mobileNav = document.querySelector('.nav-mobile');
    if (mobileNav && !mobileNav.querySelector('.language-switcher')) {
      mobileNav.appendChild(buildSwitcher());
    }
  }

  insertLanguageSwitcher();

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

  /* --- Newsletter popup --- */
  (function () {
    if (/^\/(?:conciertos|en\/concerts|de\/konzerte)\//.test(location.pathname)) return;
    var DISMISSED_KEY = 'nl-dismissed';
    var SUBSCRIBED_KEY = 'nl-subscribed';
    var LOOPS_ACTION = 'https://app.loops.so/api/newsletter-form/cmb7ofbqv5jgi0y0ipx3q1au0';
    var GRACE_MS = 30 * 24 * 60 * 60 * 1000; // 30 days

    function shouldShow() {
      if (localStorage.getItem(SUBSCRIBED_KEY)) return false;
      var dismissed = localStorage.getItem(DISMISSED_KEY);
      if (dismissed && (Date.now() - Number(dismissed)) < GRACE_MS) return false;
      return true;
    }

    function dismiss() {
      localStorage.setItem(DISMISSED_KEY, Date.now());
      var popup = document.getElementById('nl-popup');
      if (popup) popup.remove();
    }

    function injectPopup() {
      if (!shouldShow()) return;
      if (document.getElementById('nl-popup')) return;

      var popup = document.createElement('div');
      popup.id = 'nl-popup';
      popup.setAttribute('role', 'dialog');
      popup.setAttribute('aria-label', 'Suscríbete a la newsletter');
      popup.innerHTML =
        '<button class="nl-close" aria-label="Cerrar">&times;</button>' +
        '<p class="nl-eyebrow">Newsletter</p>' +
        '<h3 class="nl-title">Conciertos antes que nadie</h3>' +
        '<p class="nl-desc">Entérate primero de los próximos shows, preventa exclusiva y noticias de Salán Producciones.</p>' +
        '<div class="newsletter-form-container">' +
          '<form action="' + LOOPS_ACTION + '" method="post" class="newsletter-form">' +
            '<div class="newsletter-form-input" style="display:flex">' +
              '<input type="email" name="email" placeholder="tu@email.com" required class="form-input" style="flex:1;min-width:0">' +
            '</div>' +
            '<div class="newsletter-form-input" style="display:flex">' +
              '<input type="text" name="firstName" placeholder="Tu nombre (opcional)" class="form-input" style="flex:1;min-width:0">' +
            '</div>' +
            '<button type="submit" class="btn btn-primary newsletter-form-button" style="width:100%;margin-top:8px">Suscribirme</button>' +
            '<button type="button" class="btn btn-outline newsletter-loading-button" style="width:100%;margin-top:8px;display:none" disabled>Enviando…</button>' +
          '</form>' +
          '<div class="newsletter-success" style="display:none;flex-direction:column;align-items:center;gap:8px;padding:16px 0">' +
            '<span style="font-size:2rem">🎸</span>' +
            '<p style="margin:0;font-weight:600;color:var(--text)">¡Ya estás dentro!</p>' +
            '<p style="margin:0;font-size:.85rem;color:var(--muted)">Te avisaremos antes que nadie.</p>' +
          '</div>' +
          '<div class="newsletter-error" style="display:none;flex-direction:column;gap:6px">' +
            '<p class="newsletter-error-message" style="margin:0;font-size:.85rem;color:#e05c5c">Algo salió mal, inténtalo de nuevo.</p>' +
          '</div>' +
          '<button type="button" class="newsletter-back-button" style="display:none;background:none;border:none;color:var(--muted);font-size:.8rem;cursor:pointer;padding:4px 0;text-decoration:underline">Volver</button>' +
        '</div>';

      document.body.appendChild(popup);

      // Close button
      popup.querySelector('.nl-close').addEventListener('click', dismiss);

      // Wire up Loops handlers
      var container = popup.querySelector('.newsletter-form-container');
      container.querySelector('.newsletter-form').addEventListener('submit', loopsSubmitHandler);
      container.querySelector('.newsletter-back-button').addEventListener('click', loopsResetHandler);
      container.classList.add('newsletter-handlers-added');

      // Watch for success → mark subscribed and auto-close
      var successEl = container.querySelector('.newsletter-success');
      var observer = new MutationObserver(function () {
        if (successEl.style.display !== 'none') {
          localStorage.setItem(SUBSCRIBED_KEY, '1');
          setTimeout(function () {
            var p = document.getElementById('nl-popup');
            if (p) p.remove();
          }, 3000);
        }
      });
      observer.observe(successEl, { attributes: true, attributeFilter: ['style'] });
    }

    setTimeout(injectPopup, 10000);
  })();

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
        btn.textContent = t.contactSent;
        btn.style.background = '#2ecc71';
        btn.style.borderColor = '#2ecc71';
        btn.style.color = '#fff';
      }
    });
  }

  /* --- Dynamic Concert Loading (Upcoming) --- */
  const upcomingGrid = document.getElementById('upcoming-grid');
  const agendaGrid = document.getElementById('agenda-grid');
  const carouselTrack = document.getElementById('carousel-track');
  const concertsTimeline = document.getElementById('concerts-timeline');
  
  if (upcomingGrid || agendaGrid || carouselTrack || concertsTimeline) {
    const concertsFeed = lang === 'en' ? '/concerts.en.json' : (lang === 'de' ? '/concerts.de.json' : '/conciertos.json');
    fetch(concertsFeed)
      .then(res => res.json())
      .then(data => {
        const today = localISODate(new Date());
        const upcoming = data.filter(c => concertEndDate(c) >= today).sort((a, b) => a.dateISO.localeCompare(b.dateISO));
        
        // 1. Render Upcoming dynamically from conciertos.json
        if (upcomingGrid || agendaGrid) {
          const upcomingContainers = [upcomingGrid, agendaGrid].filter(Boolean);
          if (upcoming.length === 0) {
            upcomingContainers.forEach(container => {
              container.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: var(--muted);">' + t.noUpcoming + '</p>';
            });
          } else {
            let html = '';
            upcoming.forEach(c => {
              const buttonHtml = c.disabled 
                ? `<button class="btn btn-outline" style="flex:1" disabled>${c.buttonLabel}</button>`
                : `<a href="${c.linkBuy}" class="btn btn-primary" style="flex:2;text-align:center" ${c.linkBuy.startsWith("/") ? "" : 'target="_blank" rel="noopener"'} aria-label="${c.buyAria}">${c.buttonLabel}</a>`;
              const titleHtml = c.subtitle
                ? `${c.title}<br><small style="font-size:.75em;color:var(--muted)">${c.subtitle}</small>`
                : c.title;
                
              html += `
                <article class="concert-card reveal">
                  <div class="concert-card-img">
                    <img src="${c.image.replace('/poster.webp', '/poster-480.webp')}" ${responsivePosterAttrs(c.image, '(max-width: 700px) 92vw, (max-width: 1100px) 45vw, 320px')} alt="${t.poster} ${c.title} - ${c.dateDisplay}" loading="lazy" width="400" height="533">
                    <span class="concert-card-badge">${c.badge}</span>
                  </div>
                  <div class="concert-card-body">
                    <div class="concert-card-date">${c.dateDisplay}</div>
                    <h3 class="concert-card-title">${titleHtml}</h3>
                    <p class="concert-card-venue">${c.venue}</p>
                    <p class="concert-card-price">${c.price || ''}</p>
                    <div style="display:flex;gap:8px;margin-top:8px">
                      <a href="${c.linkInfo}" class="btn btn-outline" style="flex:1;text-align:center">${t.info}</a>
                      ${buttonHtml}
                    </div>
                  </div>
                </article>
              `;
            });
            upcomingContainers.forEach(container => {
              container.innerHTML = html;
            
              setTimeout(() => {
                const io = new IntersectionObserver((entries) => {
                  entries.forEach(e => {
                    if (e.isIntersecting) {
                      e.target.classList.add('visible');
                      io.unobserve(e.target);
                    }
                  });
                }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
                container.querySelectorAll('.reveal').forEach(el => io.observe(el));
              }, 100);
            });
          }
        }

        if (carouselTrack) {
          const dots = document.getElementById('carousel-dots');
          if (dots) dots.innerHTML = '';

          if (upcoming.length === 0) {
            carouselTrack.innerHTML = '';
            const section = carouselTrack.closest('.mobile-carousel-section');
            if (section) section.style.display = 'none';
          } else {
            carouselTrack.dataset.carouselReady = 'false';
            carouselTrack.innerHTML = upcoming.map(c => `
              <a href="${escapeHtml(c.linkInfo)}" class="carousel-item" aria-label="${escapeHtml(stripHtml(c.title))} - ${escapeHtml(stripHtml(c.dateDisplay))}">
                <img src="${escapeHtml(c.image.replace('/poster.webp', '/poster-320.webp'))}" alt="${escapeHtml(stripHtml(c.title))}" loading="lazy" width="320" height="427">
                <div class="carousel-item-info">
                  <div class="carousel-item-date">${escapeHtml(c.dateDisplay)}</div>
                  <div class="carousel-item-title">${escapeHtml(c.title)}</div>
                  <div class="carousel-item-venue">${escapeHtml(c.venue)}</div>
                </div>
              </a>
            `).join('');

            if (typeof window.initSalanCarousel === 'function') {
              window.initSalanCarousel();
            } else {
              window.salanCarouselNeedsInit = true;
            }
          }
        }

        // 2. Render Past (Anteriores) dynamically on top of existing ones
        if (concertsTimeline) {
          const past = data.filter(c => concertEndDate(c) < today).sort((a, b) => b.dateISO.localeCompare(a.dateISO)); // newest first
          
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
