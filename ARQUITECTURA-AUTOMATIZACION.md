# Arquitectura: Cómo se mueven los conciertos automáticamente

## El problema
Tienes 2-3 conciertos al mes. No quieres:
- ❌ Usar Supabase (complejidad innecesaria)
- ❌ Aprender APIs (quieres simplemente HTML)
- ❌ Scripts que actualicen bases de datos (overkill)

## La solución
**Conciertos = archivos HTML estáticos + atributo `data-date` + JavaScript simple**

---

## Cómo funciona el flujo automático

### Paso 1: Crear el evento
```
/conciertos/2026/juan-acela-15-06-2026/
├── index.html          ← Página con el concierto
└── poster.webp         ← Imagen

Contenido de index.html incluye:
<time datetime="2026-06-15">15 de junio 2026</time>
```

### Paso 2: Registrar en "próximos" (index.html principal)
```html
<section class="upcoming-concerts">
    <div class="concert-card" data-date="2026-06-15">
        <a href="/conciertos/2026/juan-acela-15-06-2026/">
            <img src="/assets/images/conciertos/poster.webp" alt="...">
            <h3>Juan Acela & The Violets</h3>
            <p class="date">15 de junio 2026</p>
        </a>
    </div>
</section>

<script>
document.querySelectorAll('[data-date]').forEach(card => {
    const eventDate = new Date(card.dataset.date);
    const today = new Date();
    
    if (today > eventDate) {
        // Pasado: ocultar o marcar como histórico
        card.style.opacity = '0.5';
        card.style.order = '-1'; // Va al final
    } else {
        // Futuro: mostrar destacado
        card.style.order = '999 - days_until_date';
    }
});
</script>
```

### Paso 3: El JavaScript hace el trabajo
**Sin intervención manual:**

```javascript
// Cada vez que se carga index.html:

1. Lee todos los concert-card con data-date
2. Compara fecha vs. hoy
3. Si fecha < hoy: 
   → Desatura visualmente (opacity)
   → Lo coloca al final (order)
   → Muestra badge "Pasado"
4. Si fecha > hoy:
   → Lo destaca (orden cronológico)
   → Mantiene color normal
```

**Resultado:**
- ✅ Conciertos futuros arriba (ordenados)
- ✅ Conciertos pasados abajo (desaturados)
- ✅ Ningún click manual necesario
- ✅ Sucede automáticamente al cargar la página

---

## Ejemplo: Ciclo de vida de un concierto

### DÍA 1: Anuncia el concierto (15 de junio)
**Tu acción:**
- Creas `/conciertos/2026/juan-acela-15-06-2026/index.html`
- Añades línea en `/index.html` con `data-date="2026-06-15"`
- Subes archivos

**JavaScript automático:**
- ✓ Lee `data-date="2026-06-15"`
- ✓ Compara: `today (15/06) < event (15/06)` → FUTURO
- ✓ Lo coloca en "próximos conciertos" arriba
- ✓ Color normal, fondo destacado

**Usuario ve:** Concierto grande arriba, con todos los detalles

### DÍA 16: Concierto ya pasó
**Nada de tu parte.** El JavaScript lo detecta:
- ✓ Lee `data-date="2026-06-15"`
- ✓ Compara: `today (16/06) > event (15/06)` → PASADO
- ✓ Lo desatura (opacity: 0.5)
- ✓ Lo coloca al final
- ✓ Badge: "Este evento ya pasó"

**Usuario ve:** Concierto pasado abajo, con link a "Anteriores"

### DÍA 30: Limpiar (opcional)
**Tu elección:**
- **Opción A:** Déjalo ahí 2 semanas, después quítalo de `/index.html`
- **Opción B:** Muévelo manualmente a `/conciertos-anteriores/index.html`

---

## Por qué NO necesitas Supabase

| Necesidad | Solución HTML estática | Supabase |
|-----------|----------------------|----------|
| Mostrar próximos conciertos | JavaScript compara fechas | API REST + polling |
| Mover a "anteriores" | Quitar línea manualmente | Webhooks + funciones edge |
| 2-3 conciertos/mes | 1 minuto manual | 10 minutos setup |
| Rendimiento | ⚡ 100/100 Lighthouse | ⚠️ Requiere API calls |
| Complejidad | Ninguna | Media-Alta |
| Costo | $0 | $0 (pero complejidad) |

**Conclusión:** HTML estático + JavaScript simple = suficiente para 2-3/mes

---

## Estructura del JavaScript (en index.html)

```javascript
<script>
// Al cargar la página
const updateConcerts = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const concertCards = document.querySelectorAll('[data-date]');
    
    concertCards.forEach(card => {
        const cardDate = new Date(card.dataset.date);
        cardDate.setHours(0, 0, 0, 0);
        
        if (cardDate < today) {
            // Pasado
            card.classList.add('concert-past');
            card.style.opacity = '0.6';
        } else {
            // Futuro
            card.classList.add('concert-upcoming');
            const daysUntil = Math.ceil((cardDate - today) / (1000 * 60 * 60 * 24));
            card.dataset.daysUntil = daysUntil;
            card.style.order = daysUntil;
        }
    });
    
    // Ordenar por fecha (próximos primero)
    const container = document.querySelector('.upcoming-concerts');
    Array.from(concertCards)
        .sort((a, b) => {
            const aDate = new Date(a.dataset.date);
            const bDate = new Date(b.dataset.date);
            return aDate - bDate;
        })
        .forEach((card, index) => {
            card.style.order = index;
        });
};

// Ejecutar al cargar
updateConcerts();

// Ejecutar cada hora (por si dejan la página abierta)
setInterval(updateConcerts, 3600000);
</script>
```

**Importante:**
- Este script ya está en tu `/index.html` (o debería)
- Se ejecuta automáticamente cada vez que cargas la página
- No requiere backend, API, ni base de datos

---

## Evolución futura (opcional, no ahora)

Si en 6 meses quieres automatizar más:

### Opción 1: JSON + Script helper
```javascript
// conciertos.json
{
    "conciertos": [
        {
            "fecha": "2026-06-15",
            "nombre": "Juan Acela & The Violets",
            "artistas": ["Juan Acela", "Miguel Santana"],
            "url": "/conciertos/2026/juan-acela-15-06-2026/"
        }
    ]
}

// Script que lee JSON y genera HTML automáticamente
fetch('/conciertos.json')
    .then(r => r.json())
    .then(data => {
        data.conciertos.forEach(concert => {
            // Generar tarjeta HTML automáticamente
        });
    });
```

### Opción 2: Supabase (si crece mucho)
- Edge Function que corre cada hora
- Actualiza automáticamente próximos/anteriores
- Sincroniza con tu app móvil (futura)

### Opción 3: Headless CMS (si quieres UX mejorada)
- Ghost, Strapi, o Sanity
- Dashboard para crear eventos
- API que genera HTML automáticamente

**Recomendación:** Empieza con HTML manual (ahora). Después de 6 meses y 20 conciertos, decides si necesitas más.

---

## Resumen: Por qué funciona

| Componente | Función |
|-----------|---------|
| `data-date="YYYY-MM-DD"` | Máquina lee fecha |
| JavaScript en `index.html` | Compara fecha vs. hoy |
| CSS `opacity`, `order` | Visualiza diferencia |
| Carpeta `/conciertos/2026/` | Organiza archivos |
| WebP para imágenes | ⚡ Rendimiento |

**Total:** 0 servidores, 0 APIs, 0 complejidad. Solo HTML + CSS + JS.

---

## Cuándo cambiar de estrategia

Cambia a Supabase/CMS cuando:
- [ ] Tienes >100 conciertos
- [ ] Quieres app móvil con datos en tiempo real
- [ ] Necesitas estadísticas/analítica
- [ ] Un equipo gestiona conciertos (colaboración)
- [ ] Anuncios automáticos en RRSS

Hasta entonces: **HTML estático = victoria** ✓
