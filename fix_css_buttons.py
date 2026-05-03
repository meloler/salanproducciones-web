import os

missing_css = """
/* =============================================
   BUTTONS & SECTION STYLES FOR INDIVIDUAL CONCERT PAGES
   ============================================= */
.section {
    padding: 80px 24px;
    max-width: var(--max);
    margin: 0 auto;
}

.section-title {
    font-family: 'Oswald', sans-serif;
    font-size: 2.5rem;
    color: #fff;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.section-sub {
    color: var(--muted);
    font-size: 1.1rem;
    margin-bottom: 40px;
}

.btn-primary, .btn-secondary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 14px 28px;
    font-size: 1.1rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.3s ease;
    text-transform: uppercase;
}

.btn-primary {
    background: var(--gold);
    color: #111;
}
.btn-primary:hover {
    background: #fff;
    color: #000;
}

.btn-secondary {
    background: transparent;
    color: #fff;
    border: 1px solid #fff;
}
.btn-secondary:hover {
    background: #fff;
    color: #000;
}

.event-guest {
    font-size: 1.2rem;
    color: var(--muted);
    margin-bottom: 20px;
}
.event-guest span {
    color: var(--gold);
    font-size: 0.9rem;
    text-transform: uppercase;
    display: block;
    margin-bottom: 5px;
}
"""

with open("assets/css/main.css", "a", encoding="utf-8") as f:
    f.write(missing_css)

print("Buttons and section classes appended to main.css!")
