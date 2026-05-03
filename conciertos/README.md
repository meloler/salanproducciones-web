# Añadir nuevo concierto: Guía rápida

## 3 pasos principales

### 1️⃣ Crear la página del evento
```
Carpeta: /conciertos/2026/nombre-artista-dd-mm-yyyy/
Archivos:
  ├── index.html  (usa PLANTILLA-evento.html como base)
  └── poster.webp (convierte tu imagen JPG a WebP)
```

### 2️⃣ Subir al servidor
- SFTP → `/conciertos/2026/nombre-artista-dd-mm-yyyy/`
- Sube: `index.html` + `poster.webp`

### 3️⃣ Actualizar lista de próximos conciertos
- Abre `/index.html`
- Busca: `<section class="upcoming-concerts">`
- Añade una tarjeta:
```html
<div class="concert-card" data-date="2026-06-15">
    <a href="/conciertos/2026/juan-acela-15-06-2026/">
        <img src="/assets/images/conciertos/poster.webp" alt="Juan Acela">
        <h3>Juan Acela & The Violets</h3>
        <p class="date">15 de junio 2026</p>
    </a>
</div>
```

**Dato crítico**: `data-date="YYYY-MM-DD"` (JavaScript usa esto para ordenar)

---

## Convertir imagen a WebP (reduce 80% tamaño)

```powershell
# Terminal (PowerShell)
cwebp -q 85 tu-poster.jpg -o poster.webp
```

---

## Mover a "Anteriores" (después de la fecha)

El concierto se muestra automáticamente como pasado en su página.

Luego (tu elección):
1. **Opción A**: Déjalo en próximos 1 semana, después quítalo
2. **Opción B**: Muévelo manualmente a `/conciertos-anteriores/index.html`

---

## Estructura de carpetas actual

```
/conciertos/
├── 2026/
│   ├── juan-acela-15-06-2026/
│   │   ├── index.html
│   │   └── poster.webp
│   └── ...más conciertos...
│
└── PLANTILLA-evento.html  ← COPIA ESTO
```

---

## Validación rápida

- [ ] `data-date="YYYY-MM-DD"` (ej: `2026-06-15`)
- [ ] Poster en WebP (no JPG)
- [ ] Carpeta sin espacios, minúsculas
- [ ] index.html completo (sin placeholders vacíos)
- [ ] URL en botón "Comprar Entradas"

---

**Documentación completa**: `PROTOCOLO-NUEVOS-CONCIERTOS.md`
**Cheat sheet**: `CHEAT-SHEET-conciertos.txt`
