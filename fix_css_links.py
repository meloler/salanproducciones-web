import os
import glob

# Missing styles for individual concert pages like Acantha Lang
missing_css = """
/* =============================================
   SPECIFIC CONCERT STYLES (ACANTHA LANG, ETC.)
   ============================================= */
.hero-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    align-items: center;
    max-width: var(--max);
    margin: 0 auto;
    padding: 120px 24px 80px;
}

.poster-card img {
    width: 100%;
    max-width: 450px;
    border-radius: 8px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    display: block;
    margin: 0 auto;
}

.content-card .eyebrow {
    color: var(--gold);
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    font-weight: bold;
    display: block;
    margin-bottom: 10px;
}

.event-title {
    font-family: 'Oswald', sans-serif;
    font-size: clamp(3rem, 6vw, 5rem);
    color: var(--gold);
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 20px;
}

.event-desc {
    font-size: 1.1rem;
    color: var(--muted);
    line-height: 1.6;
    margin-bottom: 30px;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 40px;
    background: var(--bg3);
    padding: 20px;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.info-label {
    font-size: 0.8rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 5px;
}

.info-value {
    font-size: 1.2rem;
    color: var(--gold);
    font-weight: bold;
}

.cta-group {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.video-card {
    max-width: 800px;
    margin: 0 auto;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}

.video-frame {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
}
.video-frame iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.bio-card {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 40px;
    background: var(--bg3);
    padding: 40px;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.bio-text h2 {
    color: var(--gold);
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.bio-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 30px;
}

.bio-tag {
    background: rgba(232,196,77,0.1);
    color: var(--gold);
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 0.8rem;
    text-transform: uppercase;
}

.bio-stats {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.bio-stat-num {
    font-size: 2.5rem;
    font-family: 'Oswald', sans-serif;
    color: var(--gold);
    line-height: 1;
}

.bio-stat-label {
    font-size: 0.8rem;
    color: var(--muted);
    text-transform: uppercase;
}

.final-cta-wrap {
    text-align: center;
    padding: 80px 20px;
}

.final-box h2 {
    font-family: 'Oswald', sans-serif;
    font-size: 3rem;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.final-box p {
    color: var(--muted);
    margin-bottom: 30px;
}

@media (max-width: 768px) {
    .hero-grid, .bio-card {
        grid-template-columns: 1fr;
    }
}
"""

with open("assets/css/main.css", "a", encoding="utf-8") as f:
    f.write(missing_css)

files_to_process = glob.glob("conciertos/**/*.html", recursive=True)

for filepath in files_to_process:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if '<link rel="stylesheet" href="/assets/css/main.css">' not in content:
        # insert before </head>
        content = content.replace('</head>', '    <link rel="stylesheet" href="/assets/css/main.css">\n</head>')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
print("Fixed missing CSS links and injected restored styles!")
