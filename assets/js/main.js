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

  /* --- Newsletter form --- */
  document.querySelectorAll('.newsletter-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      const nameInput = form.querySelector('input[type="text"]');
      const btn = form.querySelector('button[type="submit"]');

      if (!emailInput || !emailInput.value.trim()) return;

      // Disable during "submit"
      if (btn) {
        btn.disabled = true;
        btn.textContent = '✓ ¡Apuntado!';
        btn.style.background = '#2ecc71';
        btn.style.borderColor = '#2ecc71';
        btn.style.color = '#fff';
      }
      // In a real integration you'd POST to your email service here
      // e.g. Mailchimp, Brevo, etc.
    });
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
        
        // 1. Render Upcoming
        if (upcomingGrid) {
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
                    <img src="${c.image}" alt="Cartel ${c.title} — ${c.dateDisplay}" loading="lazy" width="400" height="533">
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
                
                // Avoid duplicates (checking if link or title already exists in the grid)
                // Simple heuristic: if the grid already has an image with the same src, skip it
                const existingImgs = Array.from(gridContainer.querySelectorAll('img')).map(img => img.src);
                const isDuplicate = existingImgs.some(src => src.includes(c.image.split('/').pop()));
                
                if (!isDuplicate) {
                  const card = document.createElement('div');
                  card.className = 'timeline-card';
                  card.innerHTML = `
                    <div class="timeline-card-img"><img src="${c.image}" alt="${c.title}" loading="lazy"></div>
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
