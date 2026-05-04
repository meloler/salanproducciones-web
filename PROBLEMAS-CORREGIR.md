# PROBLEMAS A CORREGIR — Salán Producciones

Lista de hallazgos de la auditoría. Orden: 🔴 crítico → 🟠 importante → 🟢 menor → 🔒 seguridad.

---

## 🔴 CRÍTICOS

### 1. GTM con ID falso (`GTM-XXXXXX`)
**Problema:** 4 páginas tienen el script de Google Tag Manager pero con el ID de contenedor de ejemplo `GTM-XXXXXX`. GTM no carga nada — no hay analítica real.
**Archivos afectados:** `index.html`, `pub-la-calle/index.html`, `conciertos-anteriores/index.html`, `contacto/index.html`
**Acción:** ⚠️ NECESITO QUE ME DES tu ID real de GTM (formato `GTM-XXXXXXX`, lo encuentras en tu cuenta de Google Tag Manager). Yo lo reemplazo en todos los archivos.

---

### 2. Variables CSS `--white` y `--grey` no definidas
**Problema:** 7 landings antiguas usan `var(--white)` y `var(--grey)` en sus estilos, pero esas variables no existen en el CSS global. El resultado es que el color falla silenciosamente y el texto hereda un color incorrecto.
**Archivos afectados:** landings más antiguas (Andromeda Jones, Boney Fields, etc.)
**Acción:** Puedo añadir `--white: #e8e8e8` y `--grey: #888888` al `:root` de `main.css`. Dame la orden y lo hago.

---

### 3. Formulario de newsletter no funciona
**Problema:** El formulario de suscripción en la homepage captura el email visualmente, pero el JS de `main.js` no hace ninguna petición HTTP real. Los emails no se guardan en ningún sitio.
**Acción:** ⚠️ Necesitas elegir un servicio: Mailchimp, Brevo, Formspree, o similar. Una vez me des el endpoint o API key, conecto el formulario. Sin eso, el formulario es decorativo.

---

### 4. Formulario de contacto no funciona
**Problema:** Mismo problema que la newsletter. El botón "Enviar" cambia de texto pero no manda ningún email ni petición real.
**Acción:** ⚠️ Necesitas elegir cómo recibir los mensajes (Formspree es lo más sencillo para un sitio estático — gratis hasta 50 mensajes/mes). Dame el endpoint y lo conecto.

---

## 🟠 IMPORTANTES

### 5. Doble definición de `.section` en CSS
**Problema:** La clase `.section` está definida dos veces en `main.css` (líneas 307 y 1019) con propiedades distintas. La segunda sobrescribe a la primera, lo que puede generar comportamiento inesperado en el futuro.
**Acción:** Puedo fusionar ambas definiciones en una sola limpia. Dame la orden.

---

### 6. Sin `robots.txt`
**Problema:** El sitio no tiene archivo `robots.txt`. Los buscadores lo buscan siempre; su ausencia genera un 404 silencioso en cada rastreo.
**Acción:** Puedo crearlo con un contenido correcto (permitir todo + apuntar al sitemap). Dame la orden.

---

### 7. Sin `sitemap.xml`
**Problema:** No hay sitemap. Google indexa el sitio pero sin guía explícita de qué páginas existen.
**Acción:** Puedo generar un `sitemap.xml` con todas las URLs actuales. Dame la orden.

---

### 8. Meta Pixel de Facebook no configurado
**Problema:** No hay ningún píxel de Meta en el sitio, lo que impide medir conversiones de los anuncios de Facebook/Instagram y crear audiencias personalizadas.
**Acción:** ⚠️ NECESITO QUE ME DES tu ID de Meta Pixel (lo encuentras en Meta Business Manager → Eventos → Píxeles). Yo lo instalo en todas las páginas.

---

### 9. Favicon inconsistente entre páginas
**Problema:** Algunas páginas apuntan a `/favicon.ico` y otras a `/assets/images/favicon.png`. Si el archivo no está en la ruta correcta, el navegador muestra el icono genérico en blanco.
**Acción:** ⚠️ Confirma qué archivo de favicon quieres usar y dónde está. Yo unifico todas las rutas.

---

### 10. Copyright con año fijo en el footer
**Problema:** El footer dice `© 2026 Salán Producciones SL` con el año hardcodeado. En 2027 quedará desactualizado automáticamente.
**Acción:** Puedo cambiarlo a JS dinámico (`new Date().getFullYear()`). Dame la orden.

---

### 11. Fechas estimadas en schema de Acantha Tour (Toledo, Madrid, etc.)
**Problema:** La landing `acantha-lang-tour-espana-28-06-2026` tiene fechas aproximadas en el schema de Schema.org (Toledo 28 jun, Madrid 29 jun…). Si son incorrectas, Google puede marcar el evento como inválido.
**Acción:** ⚠️ Confírmame las fechas reales de cada ciudad (o dime que son TBA) y lo actualizo.

---

### 12. Código CSS muerto (clases `.event-hero`, `.event-poster`, etc.)
**Problema:** `main.css` contiene ~120 líneas de estilos de landings antiguas (`.event-hero`, `.event-date-badge`, `.event-grid`, `.event-card`, `.event-past-banner`) que ya ninguna página usa. Aumentan el peso del CSS sin beneficio.
**Acción:** Puedo eliminar ese bloque completo. Dame la orden (es reversible con git).

---

### 13. `og:locale` y `meta theme-color` ausentes
**Problema:** Ninguna página tiene `<meta property="og:locale" content="es_ES">` ni `<meta name="theme-color">`. El primero mejora cómo Facebook muestra los links; el segundo controla el color de la barra del navegador en móvil.
**Acción:** Puedo añadir ambos a todas las páginas. Dame la orden.

---

### 14. Archivo `kenny blues.png` en la raíz
**Problema:** Hay un archivo `kenny blues.png` suelto en la raíz del proyecto (probablemente subido por accidente). No lo usa ninguna página y se despliega a Vercel innecesariamente.
**Acción:** Puedo borrarlo con `git rm`. Dame la orden.

---

## 🟢 MENORES

### 15. Meta `robots` ausente en algunas páginas
**Problema:** No todas las páginas tienen `<meta name="robots" content="index, follow">`. No es crítico (Google indexa por defecto) pero es buena práctica declararlo explícitamente.
**Acción:** Puedo añadirlo a todas las páginas de una vez. Dame la orden.

---

### 16. Carpeta `2019/` y archivo `2019.zip` en el repositorio
**Problema:** Existe contenido del año 2019 en el repo que se despliega a Vercel sin que ninguna página lo enlace.
**Acción:** ⚠️ Confirma si quieres borrarlo definitivamente o añadirlo al `.vercelignore` para que no se publique. Yo ejecuto lo que decidas.

---

### 17. `og:image` sin dimensiones explícitas en algunas páginas
**Problema:** Facebook y WhatsApp prefieren imágenes OG de exactamente 1200×630px. Los posters actuales son verticales y pueden recortarse de forma extraña al compartir.
**Acción:** ⚠️ Idealmente habría que crear versiones 1200×630 de cada poster. Esto requiere trabajo manual de imagen — te aviso para que lo tengas en cuenta.

---

### 18. `conciertos.json` sin campo `status`
**Problema:** El JSON de conciertos no tiene un campo que distinga conciertos agotados o cancelados. Si un evento se agota, no hay forma de marcarlo como `sold-out` en la card sin editar el HTML.
**Acción:** Puedo proponer un esquema mejorado para el JSON. Dime si te interesa.

---

### 19. Imágenes sin `width` y `height` en el HTML
**Problema:** Varios `<img>` no tienen los atributos `width` y `height` explícitos. Esto provoca Cumulative Layout Shift (CLS) — el contenido "salta" mientras carga, lo que penaliza en Core Web Vitals.
**Acción:** Puedo añadir las dimensiones correctas a cada imagen. Dame la orden.

---

### 20. `lang` del HTML siempre `es` pero sin región
**Problema:** Todas las páginas usan `<html lang="es">`. Lo correcto para España sería `lang="es-ES"` para mayor precisión con lectores de pantalla y herramientas de localización.
**Acción:** Puedo corregirlo en todas las páginas. Dame la orden.

---

## 🔒 SEGURIDAD

### 21. Headers de seguridad HTTP ausentes
**Problema:** El sitio no tiene headers como `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options` ni `Referrer-Policy`. Esto es configurable en Vercel sin tocar el código.
**Acción:** Puedo crear un archivo `vercel.json` con los headers correctos. Dame la orden.

---

### 22. Links externos sin `rel="noopener noreferrer"`
**Problema:** Algunos `<a target="_blank">` a sitios externos les falta `rel="noopener noreferrer"`. Esto expone al sitio a un ataque de "tabnabbing" (la página externa puede redirigir la pestaña original).
**Acción:** Puedo revisar y corregir todos los links externos. Dame la orden.

---

### 23. No hay `<meta name="referrer">`
**Problema:** Sin esta etiqueta, cuando un usuario hace clic en un link de compra de entradas, la URL completa del sitio (incluyendo posibles parámetros UTM) se envía al servidor de la ticketera en la cabecera Referer.
**Acción:** Puedo añadir `<meta name="referrer" content="strict-origin-when-cross-origin">` a todas las páginas. Dame la orden.

---

## RESUMEN DE LO QUE NECESITO DE TI

| # | Qué necesito |
|---|---|
| 1 | ID de tu contenedor GTM (formato `GTM-XXXXXXX`) |
| 3 | Servicio de newsletter elegido (Mailchimp, Brevo, Formspree…) |
| 4 | Servicio para recibir mensajes del formulario de contacto |
| 8 | ID de Meta Pixel |
| 9 | Qué favicon usar y dónde está el archivo |
| 11 | Fechas reales de Acantha Tour (Toledo, Madrid, Zaragoza, Valladolid) |
| 16 | ¿Borrar o ignorar carpeta `2019/` y `2019.zip`? |
| 17 | Crear versiones 1200×630px de los posters OG (trabajo de imagen) |

**Todo lo demás puedo hacerlo yo cuando me des la orden**, ítem por ítem o varios a la vez.
