# Protocolo: Añadir Nuevos Conciertos

## Resumen
Cuando haya un nuevo concierto:
1. **Crear evento** (15 min): Copiar plantilla → Rellenar datos → Crear poster
2. **Subir archivo** (2 min): Subirlo al servidor vía SFTP
3. **Actualizar índice** (1 min): Una línea en HTML
4. **Después de la fecha**: El concierto se mueve automáticamente a "anteriores"

---

## Paso 1: Preparar los datos del concierto

Necesitas:
- **Fecha exacta**: YYYY-MM-DD (ej: 2026-06-15)
- **Nombre del evento**: "Juan Acela & The Violets"
- **Artistas**: Lista de nombres (separados por coma)
- **Aforo**: "450 personas"
- **Precio**: "25€"
- **Descripción corta**: 1-2 frases
- **Imagen poster**: Archivo JPG/PNG (~500x700px) + nombre sin espacios
- **Enlace web** (si existe): URL de Eventbrite, Instagram, etc.

---

## Paso 2: Usar la plantilla HTML

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[NOMBRE EVENTO] - Salan Producciones</title>
    <meta name="description" content="[DESCRIPCION CORTA]. Salan Producciones, espacio de live music en Canarias.">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="/assets/css/main.css">
    <style>
        /* Vars rápidas para esta página */
        :root {
            --event-date: "[FECHA YYYY-MM-DD]";
        }
    </style>
</head>
<body>
    <header>
        <nav class="navbar">
            <a href="/" class="logo">Salan Producciones</a>
            <ul class="nav-links">
                <li><a href="/">Inicio</a></li>
                <li><a href="/pub-la-calle/">Pub La Calle</a></li>
                <li><a href="/conciertos-anteriores/">Anteriores</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <!-- HERO CON POSTER -->
        <section class="event-hero">
            <img src="/assets/images/conciertos/[NOMBRE-ARCHIVO-POSTER].webp" alt="[NOMBRE EVENTO] poster" class="event-poster">
            <div class="event-hero-content">
                <h1>[NOMBRE EVENTO]</h1>
                <div class="event-date-badge">
                    <time datetime="[FECHA]">[FECHA FORMATEADA: "15 de junio de 2026"]</time>
                </div>
            </div>
        </section>

        <!-- INFO PRINCIPAL -->
        <section class="event-info">
            <div class="event-grid">
                <div class="event-card">
                    <h3>Artistas</h3>
                    <div class="event-artists">
                        [ARTISTA 1], [ARTISTA 2], [ARTISTA 3]
                    </div>
                </div>
                
                <div class="event-card">
                    <h3>Aforo</h3>
                    <p>[AFORO]</p>
                </div>

                <div class="event-card">
                    <h3>Precio</h3>
                    <p class="price">[PRECIO]</p>
                </div>
            </div>

            <div class="event-description">
                <h2>Descripción</h2>
                <p>[DESCRIPCIÓN CORTA: 2-3 frases]</p>
            </div>

            <!-- CTA OPCIONAL -->
            [SI HAY ENLACE WEB]:
            <a href="[URL]" class="btn btn-primary" target="_blank">Entradas</a>
            [FIN SI]
        </section>
    </main>

    <footer>
        <p>&copy; 2026 Salan Producciones. Todos los derechos reservados.</p>
    </footer>

    <script>
        // Script para detectar si el evento ha pasado
        const eventDate = new Date("[FECHA]");
        const today = new Date();
        
        if (today > eventDate) {
            // Mostrar banner "Este evento ya pasó"
            const banner = document.createElement('div');
            banner.className = 'event-past-banner';
            banner.textContent = 'Este evento ya ha pasado. Ver en Anteriores';
            document.querySelector('main').prepend(banner);
        }
    </script>
</body>
</html>
```

---

## Paso 3: Estructura de carpetas

Cuando crees un nuevo concierto, crea esta estructura:

```
/conciertos/
├── 2026/
│   ├── juan-acela-26-06-2026/
│   │   ├── index.html          ← Tu archivo (rellenado)
│   │   └── poster.webp         ← Imagen (convertida a WebP)
│   └── ...más conciertos...
```

**Nombres de carpeta**: `[artista-principal]-[fecha-dmy].` Siempre minúsculas, sin espacios.

**Ejemplo real**: `/conciertos/2026/the-vaccines-21-09-2026/index.html`

---

## Paso 4: Conversión de imagen a WebP (importante para rendimiento)

En tu terminal (Windows PowerShell):

```powershell
# Instalar cwebp (solo una vez)
choco install webp -y

# Convertir tu poster JPG/PNG a WebP
cwebp -q 85 tu-poster.jpg -o poster.webp

# Resultado: 500KB JPG → 80KB WebP
```

O usar herramienta online: [CloudConvert.com](https://cloudconvert.com)

---

## Paso 5: Subir al servidor Raiola (SFTP)

Usar **WinSCP** o **FileZilla**:

1. Abre WinSCP → New Site
2. Host: `tu-dominio.es` / User: `tu-usuario` / Password: `tu-contraseña`
3. Navega a: `/public_html/conciertos/2026/[tu-carpeta]/`
4. Sube: `index.html` + `poster.webp`

Listo. El evento ya está vivo en `salanproducciones.com/conciertos/2026/juan-acela-26-06-2026/`

---

## Paso 6: Actualizar "Próximos conciertos" (index.html principal)

En `/index.html`, en la sección `<section class="upcoming-concerts">`, añade una línea:

```html
<div class="concert-card" data-date="2026-06-15">
    <a href="/conciertos/2026/juan-acela-26-06-2026/">
        <img src="/assets/images/conciertos/poster.webp" alt="Juan Acela poster">
        <h3>Juan Acela & The Violets</h3>
        <p class="date">15 de junio 2026</p>
    </a>
</div>
```

El JavaScript ya se encargará de:
- Mostrar en "Próximos" si la fecha es futura
- Mover automáticamente a "Anteriores" después de la fecha
- Ordenar por fecha

---

## Paso 7: Conciertos históricos (añadir a "Anteriores")

En `/conciertos-anteriores/index.html`, en el grupo del año correcto (`data-year="2026"`), añade:

```html
<div class="concert-item">
    <img src="/assets/images/conciertos/poster.webp" alt="Juan Acela poster" class="concert-poster">
    <div class="concert-details">
        <h3>Juan Acela & The Violets</h3>
        <p class="date">15 de junio 2026</p>
        <p class="venue">Salan Producciones</p>
    </div>
</div>
```

---

## Checklist rápido

Para cada nuevo concierto:

- [ ] Fecha en formato YYYY-MM-DD
- [ ] Artistas, aforo, precio listos
- [ ] Poster convertido a WebP (85% calidad)
- [ ] Carpeta creada: `/conciertos/2026/[nombre-fecha]/`
- [ ] `index.html` rellenado y subido
- [ ] `poster.webp` subido
- [ ] Línea añadida en `/index.html` (próximos)
- [ ] (Si pasó) Línea añadida en `/conciertos-anteriores/index.html`

---

## Rendimiento Google Lighthouse (100/100)

Ya está optimizado:
- ✅ WebP para todas las imágenes
- ✅ CSS minificado
- ✅ Lazy loading en imágenes
- ✅ Fuentes locales (no Google Fonts)
- ✅ Gzip en servidor

Supabase no es necesario para esta solución. HTML estático es más rápido.

---

## Soporte rápido

**¿Se puede automatizar más?**
Sí, pero añade complejidad. Con 2-3 conciertos/mes, el método manual es más que viable y tienes control total.

**¿Y si quiero un CMS?**
Luego. Primero prueba esto 6 meses, luego valora si necesita Headless CMS + API.
