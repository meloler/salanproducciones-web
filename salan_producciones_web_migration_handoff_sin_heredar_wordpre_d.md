# Salán Producciones — Plan final para pasar de WordPress a GitHub + Vercel

**Fecha:** 2026-05-05  
**Proyecto GitHub:** `meloler/salanproducciones-web`  
**Preview actual:** `https://salanproducciones.vercel.app`  
**Dominio final:** `https://www.salanproducciones.com`  
**Objetivo:** sustituir WordPress/Raiola por una web nueva 100% estática en GitHub + Vercel.

---

## 0. Decisión de base

La web nueva **no va a heredar el contenido del WordPress antiguo**.

La nueva web está hecha desde cero. Del WordPress solo interesa conservar o migrar:

1. Carteles/imágenes que todavía se estén usando en la web nueva.
2. Histórico visual de carteles, si Juan quiere conservarlo.
3. Alguna redirección mínima desde URLs antiguas importantes, solo por SEO/tráfico.

No hace falta migrar posts, páginas, categorías ni estructura interna de WordPress.

---

# FASE 1 — Migrar imágenes que dependen de WordPress

## Objetivo

Eliminar cualquier dependencia de:

```txt
https://www.salanproducciones.com/wp-content/uploads/...
```

Cuando WordPress desaparezca, esas URLs dejarán de funcionar si no se copian a Vercel/GitHub.

---

#### FASE 1 
## Imágenes detectadas que dependen de WordPress

### 1. Logo usado en schema Organization

```txt
https://www.salanproducciones.com/wp-content/uploads/2020/01/logo-salan.png
```

Uso:

```txt
index.html
```

Nota: esta URL ya devuelve 404. Sustituir por logo local:

```txt
https://www.salanproducciones.com/assets/images/logo-salan.png
```

---

### 2. Ana Curra

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/02/WhatsApp-Image-2026-01-30-at-12.47.06.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/ana-curra-11-04-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/ana-curra-11-04-2026/poster.webp
```

---

### 3. Álvaro Suite Tenerife

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/04/alvaro-suite-tenerife.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/alvaro-suite-tenerife-30-04-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/alvaro-suite-tenerife-30-04-2026/poster.webp
```

---

### 4. Álvaro Suite Gran Canaria

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/05/alvaro-suite-gran-canaria.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/alvaro-suite-gran-canaria-01-05-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/alvaro-suite-gran-canaria-01-05-2026/poster.webp
```

---

### 5. Acantha Lang — Gira junio

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/02/CARTEL-ACANTHA-LANG_4-7-JUNIO-2026_CON-HORARIOS_ACANTHA-LANG-REMAKE_02_RRSS-1.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/acantha-lang-junio-gira-e-04-06-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/acantha-lang-junio-gira-e-04-06-2026/poster.webp
```

---

### 6. Poseidón Rock Fest

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/01/poseidon-rock-fest.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/poseidon-rock-fest-13-06-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/poseidon-rock-fest-13-06-2026/poster.webp
```

---

### 7. Bywater Call Tenerife

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/01/WhatsApp-Image-2026-01-30-at-18.08.40.webp
```

Uso:

```txt
conciertos.json
```

Nota importante: en `conciertos.json`, este evento aparece como:

```txt
bywater-call-16-06-2026
```

pero su `linkInfo` apunta a:

```txt
/conciertos/2026/bywater-call-17-06-2026/
```

Hay que decidir una de estas opciones:

1. Crear landing propia para Bywater Call Tenerife.
2. Ajustar el evento para que sea claramente una card compartida.
3. Eliminar esa card si no debe aparecer como evento separado.

Ruta recomendada si se crea landing propia:

```txt
/conciertos/2026/bywater-call-tenerife-16-06-2026/poster.webp
```

---

### 8. Acantha Lang — Tour España

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/06/acantha-spain-2026.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/acantha-lang-tour-espana-28-06-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/acantha-lang-tour-espana-28-06-2026/poster.webp
```

---

### 9. Clearwater Creedence Revival — El Sauzal

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/02/Credence-Sauzal.webp
```

Usos:

```txt
conciertos.json
conciertos/2026/clearwater-creedence-revival-el-sauzal-13-11-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/clearwater-creedence-revival-el-sauzal-13-11-2026/poster.webp
```

---

### 10. Clearwater Creedence Revival — Telde

```txt
https://www.salanproducciones.com/wp-content/uploads/2026/02/Credence-Telde-1.jpeg
```

Usos:

```txt
conciertos.json
conciertos/2026/clearwater-creedence-revival-telde-14-11-2026/index.html
```

Ruta recomendada nueva:

```txt
/conciertos/2026/clearwater-creedence-revival-telde-14-11-2026/poster.webp
```

---

## Acciones para la IA/desarrollador

1. Descargar esas imágenes desde WordPress antes de apagarlo.
2. Guardarlas dentro del repo de GitHub.
3. Preferiblemente normalizar cada cartel como:

```txt
/conciertos/2026/<slug>/poster.webp
```

4. Actualizar referencias en:

```txt
conciertos.json
landings HTML
meta og:image
JSON-LD image
img src visibles
```

5. Buscar al final que no quede ninguna referencia a:

```txt
/wp-content/uploads
```

Comando sugerido:

```bash
grep -R "wp-content/uploads" .
```

El resultado final debe estar vacío.

## Acción de Juan

Confirmar si quiere que todos los carteles se llamen `poster.webp` dentro de cada carpeta de concierto. Recomendación: sí.

---

# FASE 2 — Backup mínimo del WordPress antiguo

## Objetivo

Tener una copia por seguridad antes de eliminar WordPress.

Esto no es para migrar contenido a la web nueva. Es solo por prudencia.

## Acciones recomendadas

1. Descargar un backup completo desde Raiola/cPanel si es fácil.
2. Como mínimo, guardar:
   - carpeta `wp-content/uploads`
   - export XML de WordPress
   - base de datos si el panel lo permite

## Acción de Juan

Decidir si quiere backup completo o solo guardar carteles/imágenes.

Recomendación: hacer backup completo una vez y guardarlo. No molesta, y evita lloros arqueológicos dentro de seis meses.

---

# FASE 3 — Noindex temporal del preview de Vercel

## Problema

La web nueva vive ahora en:

```txt
https://salanproducciones.vercel.app
```

Pero el dominio final será:

```txt
https://www.salanproducciones.com
```

Mientras el dominio real siga apuntando a WordPress, no interesa que Google indexe el preview de Vercel.

## Acciones para la IA/desarrollador

1. Mantener `salanproducciones.vercel.app` como entorno de preview.
2. Añadir `noindex` solo al preview si es posible.
3. Cuando `www.salanproducciones.com` apunte a Vercel, quitar el `noindex`.
4. Confirmar que:

```txt
robots.txt
sitemap.xml
canonical
```

apuntan al dominio final.

## Acción de Juan

No pedir indexación en Google Search Console hasta que el dominio real esté ya funcionando en Vercel.

---

# FASE 4 — Redirecciones mínimas desde WordPress antiguo

## Importante

Como la web nueva no hereda la anterior, no hace falta redirigir absolutamente todo.

Pero sí conviene crear redirecciones mínimas para evitar 404 en páginas antiguas con tráfico o enlaces externos.

## Redirecciones recomendadas

```txt
/contactar/ → /contacto/
/proximos-conciertos/ → /#proximos
/conciertos-anteriores/ → /conciertos-anteriores/
/pub-la-calle/ → /pub-la-calle/
```

Para posts antiguos de conciertos, si no se van a recrear páginas individuales:

```txt
/<slug-antiguo>/ → /conciertos-anteriores/
```

Ejemplos:

```txt
/vinnie-moore/ → /conciertos-anteriores/
/nik-west/ → /conciertos-anteriores/
/michaels-legacy/ → /conciertos-anteriores/
/depedro/ → /conciertos-anteriores/
/susan-santos/ → /conciertos-anteriores/
```

## Acciones para la IA/desarrollador

1. Crear redirects en `vercel.json`.
2. No obsesionarse con redirigir todos los attachments/media antiguos.
3. Priorizar páginas con valor real:
   - Pub La Calle
   - conciertos históricos importantes
   - páginas con enlaces externos
   - páginas que Juan recuerde como importantes

## Acción de Juan

Indicar si hay URLs antiguas concretas que quiera preservar sí o sí.

---

# FASE 5 — Hacer la home rastreable sin depender solo de JavaScript

## Problema actual

La home carga próximos conciertos mediante JavaScript desde:

```txt
/conciertos.json
```

El HTML inicial tiene el contenedor vacío.

## Riesgo

Google puede ejecutar JS, pero para SEO es mejor que los enlaces importantes estén ya en el HTML.

## Acciones para la IA/desarrollador

1. Generar las cards de próximos conciertos directamente en `index.html`.
2. Cada card debe tener enlace HTML real a su landing.
3. El JS puede quedarse para mejorar orden/filtros, pero no debe ser imprescindible.
4. Al añadir un concierto nuevo, actualizar:
   - landing
   - `conciertos.json`
   - card estática en home, o generar home automáticamente desde JSON.

## Acción de Juan

Validar que visualmente no cambia nada.

---

# FASE 6 — Corregir SEO técnico de landings

## Acciones para la IA/desarrollador

En cada landing de concierto:

1. H1 único y descriptivo.

Mejor:

```txt
Bywater Call en Las Palmas de Gran Canaria
```

Peor:

```txt
Bywater Call
```

2. Title entre 50 y 65 caracteres si se puede.
3. Meta description entre 145 y 160 caracteres.
4. Canonical apuntando a sí misma en dominio final.
5. `og:url`, `og:title`, `og:description`, `og:image` completos.
6. Twitter Card completa.
7. No usar imágenes de WordPress.
8. No usar `Salan Producciones` sin tilde si se puede evitar. Usar `Salán Producciones`.

---

# FASE 7 — Corregir Schema.org de eventos

## Acciones para la IA/desarrollador

1. Usar siempre:

```json
"@type": "MusicEvent"
```

2. Organizer:

```json
"organizer": {
  "@type": "Organization",
  "name": "Salán Producciones",
  "url": "https://www.salanproducciones.com"
}
```

3. Añadir zona horaria en fechas:

```json
"startDate": "2026-06-17T20:00:00+01:00"
```

4. Corregir precios y disponibilidad.
5. Si no hay venta activa, no marcar `InStock`.
6. Añadir `BreadcrumbList` si es posible.
7. Usar logo local en schema, no WordPress.

---

# FASE 8 — Open Graph / WhatsApp / Facebook

## Objetivo

Que al compartir enlaces se vean bien.

## Acciones para la IA/desarrollador

1. Crear imágenes OG 1200×630 para:
   - home
   - Pub La Calle
   - conciertos anteriores
   - cada concierto importante

2. Evitar usar posters verticales como única `og:image`, porque WhatsApp/Facebook pueden recortarlos mal.

3. Todas las páginas deben incluir:

```html
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.salanproducciones.com/...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="https://www.salanproducciones.com/.../og.jpg">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
```

## Acción de Juan

Confirmar si quiere una plantilla visual fija para las imágenes OG.

---

# FASE 9 — Rendimiento

## Imágenes grandes detectadas

```txt
assets/images/pub-la-calle-interior.jpeg — 2.2 MB
assets/images/juan-salan.jpeg — 1.4 MB
assets/images/logo-desde-1987.png — 412 KB
assets/favicon.ico — 408 KB
```

## Acciones para la IA/desarrollador

1. Optimizar esas imágenes.
2. Crear versiones WebP/AVIF si procede.
3. Reducir `favicon.ico`.
4. Revisar que todas las imágenes tienen `width` y `height`.
5. Sustituir iframes pesados de YouTube por lite embeds si afectan a rendimiento.
6. Evitar `@import` de Google Fonts dentro del CSS; mejor usar `<link>` en HTML o self-host.

---

# FASE 10 — Formularios, legal y cookies

## Problemas actuales

- Enlaces legales del footer están como `#`.
- Formulario de contacto no envía realmente.
- Hay Google Tag Manager, así que hay que revisar cookies/consentimiento.

## Acciones para la IA/desarrollador

1. Crear páginas:

```txt
/privacidad/
/aviso-legal/
/cookies/
```

2. Cambiar enlaces del footer.
3. Conectar formulario de contacto a un sistema real.
4. Revisar newsletter/Loops.
5. Revisar consentimiento de cookies si GTM dispara analítica o marketing.

## Acciones de Juan

Pasar datos legales:

```txt
Razón social
CIF
Domicilio legal
Email de contacto
Texto o criterio para privacidad/cookies
```

---

# FASE 11 — Revisión de conciertos y enlaces

## Hallazgos concretos

1. `bywater-call-16-06-2026` apunta a la landing de `bywater-call-17-06-2026`.
2. Álvaro Suite Tenerife devolvió 404 en prueba automatizada.
3. Teatro Guiniguada devolvió 403 al bot; puede ser normal por anti-bot, pero hay que probarlo manualmente.
4. Algunos títulos en `conciertos.json` incluyen HTML. Mejor separar título limpio y subtítulo.

## Acciones para la IA/desarrollador

1. Revisar todos los enlaces de compra.
2. Crear campo `status`:

```json
"status": "scheduled" | "sold-out" | "cancelled" | "past" | "coming-soon"
```

3. Evitar HTML dentro de `title`.
4. Decidir qué hacer con Bywater Tenerife.

## Acciones de Juan

Confirmar enlaces correctos de ticketera y si Bywater Tenerife debe tener landing propia.

---

# FASE 12 — Checklist antes de cambiar DNS

Antes de apuntar `www.salanproducciones.com` a Vercel:

- [ ] No queda ninguna referencia a `/wp-content/uploads`.
- [ ] Todas las imágenes usadas por la web nueva están en GitHub/Vercel.
- [ ] `robots.txt` correcto.
- [ ] `sitemap.xml` correcto.
- [ ] Canonicals apuntan al dominio final.
- [ ] Home tiene enlaces HTML reales a los conciertos.
- [ ] Landings principales funcionan en preview.
- [ ] OG images cargan.
- [ ] Redirecciones mínimas listas.
- [ ] No se tocan registros MX/correo.
- [ ] Juan aprueba explícitamente el cambio DNS.

---

# FASE 13 — Después del cambio DNS

## Probar URLs principales

```txt
https://www.salanproducciones.com/
https://www.salanproducciones.com/robots.txt
https://www.salanproducciones.com/sitemap.xml
https://www.salanproducciones.com/conciertos-anteriores/
https://www.salanproducciones.com/pub-la-calle/
https://www.salanproducciones.com/contacto/
```

## Probar landings

```txt
https://www.salanproducciones.com/conciertos/2026/bywater-call-17-06-2026/
https://www.salanproducciones.com/conciertos/2026/kenny-blues-boss-wayne-gira-espana-2026/
https://www.salanproducciones.com/conciertos/2026/poseidon-rock-fest-13-06-2026/
```

## Probar redirects antiguos

```txt
/contactar/
/proximos-conciertos/
/vinnie-moore/
/nik-west/
/michaels-legacy/
```

## Search Console

1. Inspeccionar home.
2. Enviar sitemap.
3. Revisar cobertura.
4. Revisar páginas 404.
5. Validar rich results de eventos.

---

# Resumen final para la IA/desarrollador

La web nueva no debe heredar WordPress. Pero antes de eliminar WordPress hay que hacer tres cosas sí o sí:

1. **Migrar los carteles/imágenes que aún cargan desde WordPress.**
2. **Evitar que el preview de Vercel se indexe antes del cambio definitivo.**
3. **Preparar redirecciones mínimas para no matar URLs antiguas importantes.**

Después de eso, GitHub + Vercel es la fuente única de verdad.

La regla de oro:

```txt
Si al buscar “wp-content/uploads” en el repo aparece algo, todavía no se puede apagar WordPress.
```
