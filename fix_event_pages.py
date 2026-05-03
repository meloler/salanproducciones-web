import os
import re

css_to_append = """
/* =============================================
   EVENT PAGES (CONCIERTOS)
   ============================================= */
.event-hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    align-items: center;
    padding: 120px 24px 80px; /* Incremented top padding to account for fixed header */
    max-width: var(--max);
    margin: 0 auto;
}

.event-poster {
    width: 100%;
    max-width: 400px;
    border-radius: 8px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.event-hero-content h1 {
    font-family: 'Oswald', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    color: var(--gold);
    margin-bottom: 20px;
    font-weight: 700;
    text-transform: uppercase;
    line-height: 1.1;
    letter-spacing: -.01em;
}

.event-date-badge {
    font-size: 1.2rem;
    color: var(--red);
    font-weight: bold;
    margin-bottom: 40px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.event-info {
    max-width: var(--max);
    margin: 0 auto;
    padding: 0 24px 80px;
}

.event-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    margin-bottom: 60px;
}

.event-card {
    background: var(--bg3);
    padding: 30px;
    border-radius: var(--radius);
    border-left: 3px solid var(--red);
}

.event-card h3 {
    color: var(--gold);
    margin-bottom: 15px;
    font-size: 1.1rem;
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.event-card p {
    color: var(--text);
    line-height: 1.6;
}

.price {
    font-size: 1.5rem;
    color: var(--red);
    font-weight: bold;
}

.event-description {
    background: var(--bg3);
    padding: 40px;
    border-radius: var(--radius);
    margin-bottom: 40px;
}

.event-description h2 {
    color: var(--gold);
    margin-bottom: 20px;
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    font-size: 2rem;
}

.event-description p {
    color: var(--muted);
    line-height: 1.8;
    font-size: 1.05rem;
    margin-bottom: 15px;
}

.event-past-banner {
    background: var(--red);
    color: white;
    padding: 20px;
    text-align: center;
    font-weight: bold;
    margin-bottom: 40px;
    border-radius: 4px;
    max-width: var(--max);
    margin-left: auto;
    margin-right: auto;
}

@media (max-width: 768px) {
    .event-hero {
        grid-template-columns: 1fr;
        padding: 100px 24px 40px;
    }
    .event-poster {
        max-width: 100%;
    }
}
"""

with open("assets/css/main.css", "a", encoding="utf-8") as f:
    f.write(css_to_append)

header_html = """<!-- ===================== HEADER / NAV ===================== -->
<header class="site-header" role="banner">
  <div class="nav-inner">
    <a href="/" class="nav-logo" aria-label="Salán Producciones — inicio">
      <img src="/assets/images/logo-salan.png" alt="Salán Producciones" height="36" style="height:36px;width:auto;display:block;filter:brightness(0) invert(1);">
    </a>
    <nav class="nav-links" aria-label="Navegación principal">
      <a href="/">Inicio</a>
      <a href="/#proximos">Próximos conciertos</a>
      <a href="/conciertos-anteriores/">Anteriores</a>
      <a href="/pub-la-calle/">Pub La Calle</a>
      <a href="/contacto/">Contacto</a>
    </nav>
    <button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
  <nav class="nav-mobile" aria-label="Menú móvil">
    <a href="/">Inicio</a>
    <a href="/#proximos">Próximos conciertos</a>
    <a href="/conciertos-anteriores/">Anteriores</a>
    <a href="/pub-la-calle/">Pub La Calle</a>
    <a href="/contacto/">Contacto</a>
  </nav>
</header>"""

footer_html = """<!-- ===================== FOOTER ===================== -->
<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer-inner">

      <div>
        <div class="footer-brand-name">Salán <span>Producciones</span></div>
        <p class="footer-brand-desc">
          Más de 35 años produciendo y promoviendo música en directo en las Islas Canarias y España. Un proyecto de Juan Salán.
        </p>
        <div class="footer-social" aria-label="Redes sociales">
          <a href="https://www.facebook.com/salanproducciones" target="_blank" rel="noopener" aria-label="Facebook">f</a>
          <a href="https://www.instagram.com/salanproducciones" target="_blank" rel="noopener" aria-label="Instagram">ig</a>
          <a href="https://www.youtube.com/@salanproducciones" target="_blank" rel="noopener" aria-label="YouTube">yt</a>
        </div>
      </div>

      <div>
        <div class="footer-col-title">Secciones</div>
        <ul class="footer-links">
          <li><a href="/#proximos">Próximos conciertos</a></li>
          <li><a href="/conciertos-anteriores/">Conciertos anteriores</a></li>
          <li><a href="/pub-la-calle/">Pub La Calle</a></li>
          <li><a href="/contacto/">Contacto</a></li>
        </ul>
      </div>

      <div>
        <div class="footer-col-title">Contacto</div>
        <div class="footer-contact-item">
          <span>📞</span>
          <a href="tel:+34637138073">637 138 073</a>
        </div>
        <div class="footer-contact-item">
          <span>📧</span>
          <a href="/contacto/">Formulario de contacto</a>
        </div>
        <div class="footer-contact-item">
          <span>📍</span>
          <span>Islas Canarias, España</span>
        </div>
      </div>

    </div>

    <div class="footer-bottom">
      <p class="footer-copy">© 2026 Salán Producciones SL. Todos los derechos reservados.</p>
      <div class="footer-legal">
        <a href="#">Política de privacidad</a>
        <a href="#">Aviso legal</a>
        <a href="#">Cookies</a>
      </div>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>"""

import glob

files_to_process = glob.glob("conciertos/**/*.html", recursive=True)
files_to_process.append("conciertos/PLANTILLA-evento.html")

for filepath in files_to_process:
    if not os.path.exists(filepath): continue
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add fonts to head if missing
    if '<link rel="preconnect" href="https://fonts.googleapis.com">' not in content:
        content = content.replace("</head>", '  <link rel="preconnect" href="https://fonts.googleapis.com">\n</head>')

    # Remove inline style
    content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)

    # Replace header
    content = re.sub(r'<header>.*?</header>', header_html, content, flags=re.DOTALL)

    # Replace footer
    content = re.sub(r'<footer>.*?</footer>', footer_html, content, flags=re.DOTALL)

    # Add <script src="/assets/js/main.js" defer></script> if not present (handled in footer now)
    # Actually wait, the old script might be at the bottom, let's keep it but ensure main.js is loaded
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Processed {len(files_to_process)} files.")
