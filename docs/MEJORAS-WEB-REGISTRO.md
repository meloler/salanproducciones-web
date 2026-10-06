# Registro de mejoras de Salán Producciones

Fecha de revisión: 6 de octubre de 2026

Rama: codex/mejoras-web-salan

Commit base: 1156a45c9437b2b98e398c8daa8d42f8884218f5

Producción: https://www.salanproducciones.com

## Alcance

Este primer lote cubre las fases 0 y 1 del plan. Conserva la identidad visual, las páginas de WOMEX y las fichas de Kenny. No se han enviado formularios, suscripciones, compras ni eventos de analítica a producción.

Las capturas locales de referencia están en output/playwright/phase0/. Incluyen portada con y sin JavaScript, agenda, una ficha de concierto, WOMEX y pruebas móviles. Son archivos de esta carpeta de trabajo, no se incorporan al sitio.

## Situación inicial

Se revisaron README.md, CLAUDE.md, STYLE_GUIDE.md, GUIA-MULTIDIOMA.md, docs/seo-preview.md y docs/kenny-sales-preview.md, además de los feeds, páginas, scripts y generadores actuales. El remoto main estaba en el mismo commit base. La única modificación preexistente era el plan adjunto guardado en docs/PLAN-MEJORA-SEGURA-WEB.md; se dejó fuera de los cambios del lote.

La web funciona como HTML, CSS y JavaScript estáticos. conciertos.json alimenta los feeds traducidos y assets/js/main.js; la portada y la agenda también incluyen HTML estático para funcionar sin JavaScript. El generador multidioma reescribe muchas páginas, por lo que no se ejecutó completo.

## Medidas iniciales

Una muestra de laboratorio por página, sin caché comparativa garantizada. Escritorio a 1280 × 720; móvil a 390 × 844. La primera sesión de cada contexto conservó el consentimiento de cookies sin decidir. No son mediciones de usuarios reales ni medianas.

| Página | Vista | Peticiones | Transferencia | LCP | CLS |
| --- | --- | ---: | ---: | ---: | ---: |
| Portada | Escritorio | 16 | 402.072 bytes | 460 ms | 0,0165 |
| Agenda | Escritorio | 13 | 252.155 bytes | 460 ms | 0,0194 |
| Clearwater El Sauzal | Escritorio | 11 | 153.855 bytes | 648 ms | 0,0403 |
| WOMEX | Escritorio | 8 | 159.640 bytes | 508 ms | 0,0048 |
| Portada | Móvil | 20 | 676.332 bytes | 528 ms | 0,0176 |
| Agenda | Móvil | 12 | 342.097 bytes | 444 ms | 0,0520 |
| Clearwater El Sauzal | Móvil | 11 | 153.855 bytes | 560 ms | 0,0109 |
| WOMEX | Móvil | 7 | 77.742 bytes | 400 ms | 0,0140 |

No se propone una optimización de rendimiento en este lote; estas cifras sirven de referencia y requieren mediciones repetidas antes de comparar.

## Hallazgos reproducidos y cambios

### Conciertos que ya habían terminado

El 6 de octubre de 2026, siete eventos seguían como programados en los feeds aunque su fecha final ya había pasado: Poseidón, Bywater Call en La Laguna y Las Palmas, Acantha Lang, Kenny Wayne y las dos fechas de Rebrote. JavaScript ocultaba las tarjetas vencidas, pero el HTML inicial de portada y agenda todavía mostraba Kenny y Rebrote. Al desactivar JavaScript, los botones de entradas caducados seguían visibles. El ItemList de agenda también conservaba esos eventos.

Se marcaron esos siete registros como pasados en los tres feeds. Se quitaron las tres tarjetas caducadas de las portadas y agendas ES/EN/DE, se mantuvieron las dos fechas futuras de Clearwater en el carrusel móvil y se dejó el ItemList de agenda con esas mismas dos fechas y enlaces a la ficha del idioma correspondiente. También se actualizaron las descripciones de agenda para no anunciar conciertos ya celebrados.

### Datos de Clearwater

Tickety muestra El Sauzal el 13 de noviembre a las 20:00. Tureserva muestra Telde el 14 de noviembre a las 20:30. Ambas fechas son horario de invierno en Canarias, UTC+00:00. La guía de estilos ya no prescribe +01:00 para todas las fechas; ahora pide usar la zona y el cambio horario oficial que corresponden al lugar y al día.

Se corrigió el desplazamiento horario en las seis fichas ES/EN/DE y se eliminaron las horas finales y fechas de inicio de venta que no tenían una fuente confirmada. Las páginas de agenda expresan las fechas sin hora, que es la información que contiene ese resumen.

El sitio muestra 26,20 € con gastos incluidos para Telde; la ficha pública de Tureserva también expone un precio desde 25 €. La diferencia entre precio base y total con cargos queda pendiente de confirmación con la ticketera. Se conserva el dato del sitio y no se completó una compra.

### Imágenes compartidas e histórico

La revisión inicial encontró 60 rutas de imagen que no resolvían como archivos locales; una era el cartel de ejemplo deliberado de la plantilla de concierto. Las demás eran referencias de archivo o de páginas de proyectos culturales en inglés y alemán. En WOMEX, las seis imágenes compartidas ya funcionaban y se conservaron.

Se cambiaron las rutas de Cinezín y Festival Sonora para usar los recursos existentes bajo /proyectosculturales/ en todos los idiomas. Se corrigieron cinco nombres de imagen del archivo EN/DE para que coincidan con los archivos guardados. El generador ahora conserva las rutas compartidas y normaliza esos nombres después de traducir texto.

### Mantenimiento y documentación

- Se añadió tools/check_site_resources.py, que comprueba recursos locales de páginas públicas, coincidencia de fechas y estados entre los feeds, tarjetas estáticas y las seis imágenes compartidas de WOMEX.
- tools/check_kenny_sales.py ahora lee sus archivos como UTF-8 explícitamente. Antes fallaba con la página de códigos predeterminada de Windows; con UTF-8 ya pasaba.
- README.md y CLAUDE.md describen HTML estático y el flujo seguro: rama de trabajo, preview y autorización antes de publicar en main.
- GUIA-MULTIDIOMA.md explica el feed de entrada y la alternativa HTML sin JavaScript. Los protocolos antiguos de SFTP y data-date se han marcado como históricos sin borrar su contenido.
- STYLE_GUIDE.md documenta la zona horaria por lugar y fecha y prohíbe inventar horas de finalización o fechas de venta.
- .vercelignore excluye la documentación de trabajo y las capturas locales del paquete del sitio.

## Comprobaciones

| Comprobación | Resultado |
| --- | --- |
| python tools/check_seo.py | Correcta: 105 URLs, canonicals, idiomas recíprocos y JSON-LD parseable |
| python tools/check_kenny_sales.py | Correcta después de fijar lectura UTF-8: 10 fechas por idioma, compras y recursos |
| python tools/check_site_resources.py | Correcta: 1.248 referencias locales, tres feeds, tarjetas estáticas y recursos WOMEX |
| node --check para main.js, cookies.js, kenny-tour.js y lite-yt-embed.js | Correcta |
| Navegador, ES/EN/DE | Portadas y agendas muestran las dos fechas de Clearwater; información y destinos de entradas correctos |
| Navegador, WOMEX ES/EN/DE | Las seis imágenes compartidas cargan |
| Navegador móvil | El menú abre y cierra; cookies pueden aceptarse; newsletter y formulario observados sin enviar datos |

Las comprobaciones de navegador se hicieron en la vista local del lote y, para la referencia inicial, en el sitio publicado. No se hizo compra, no se completó contacto o newsletter y no se midieron ventas. El popup actual de newsletter puede cubrir parte de la vista móvil; se conserva para una revisión posterior de uso.

## Estado de la preview

- Preview Vercel lista: https://salanproducciones-bll1mbudl-juans-projects-8e14424d.vercel.app. Requiere iniciar sesión en Vercel.
- En esa preview se comprobaron portada, agenda y las dos fichas de Clearwater en ES/EN/DE; enlaces a entradas y campañas conservados; fechas del ItemList enlazadas a cada idioma; las seis imágenes WOMEX cargaron en los tres idiomas. También cargaron las imágenes de seis páginas culturales EN/DE y las cinco referencias corregidas del archivo.
- La preview sigue mostrando 26,20 € con gastos incluidos para Telde. Tureserva presenta además un precio desde 25 €; queda pendiente confirmar el total con cargos.
- Producción no se ha actualizado. Espera la revisión y autorización expresa de Juan antes de publicar.

La vuelta atrás del cambio es revertir el commit de esta rama o cerrar la rama sin integrarla. Producción permanece en el commit base.

## WOMEX Festival: enlace de entradas y tarjeta (6 de octubre de 2026)

- Se añadió el enlace de entradas facilitado por Juan a las páginas de WOMEX en español, inglés y alemán. El enlace al sitio oficial de WOMEX se conserva como segundo botón.
- Se agregó WOMEX Festival a los feeds, las tarjetas estáticas de portada y agenda y el carrusel móvil. La tarjeta enlaza a la página cultural del idioma correspondiente; el botón de compra conserva el enlace facilitado, incluidos sus parámetros, sin añadir etiquetas de seguimiento.
- La tarjeta no superpone una etiqueta al cartel y muestra la imagen completa, para mantener legible el texto cercano a sus bordes.
- El cartel facilitado se guardó como `assets/images/womex-festival-2026.webp` (495 × 619 px, 81.572 bytes). La tarjeta no muestra un precio único porque la venta ofrece opciones distintas.
- La web oficial de WOMEX y el cartel indican que el festival completo va del 21 al 25 de octubre. La ficha de venta del Auditorio anuncia conciertos con entrada del 22 al 24, desde las 21:00. Las tarjetas y agendas muestran las fechas completas del festival y aclaran por separado qué noches tienen conciertos con entrada.
- La nota del Ayuntamiento sobre la sede de 2026 conserva el rango 22–26 de octubre. Para las fechas generales se sigue el calendario y el cartel oficial de WOMEX; el enlace de entradas conserva la página específica del Auditorio.
- El generador multidioma conserva enlaces de información externos a las fichas culturales, omite WOMEX de la creación de fichas de concierto y del sitemap duplicado, y mantiene intacto el parámetro `preview_secret` que Juan pidió incluir.
- La vista previa actual se comprobó en ES/EN/DE: portada, carrusel móvil, agendas y páginas culturales. Las tarjetas muestran 21–25 de octubre, las agendas estructuradas coinciden y la página de entradas respondió.

Fuentes consultadas: [WOMEX 26](https://womex-festival.com/), [ficha de WOMEX Festival del Auditorio](https://auditorioalfredokraus.es/evento/womex-festival) y [nota del Ayuntamiento](https://www.laspalmasgc.es/es/ayuntamiento/prensa-y-comunicacion/notas-de-prensa/nota-de-prensa/Las-Palmas-de-Gran-Canaria-se-consolida-como-referente-cultural-internacional-con-la-celebracion-de-WOMEX-2026/).

## Fase 2 — Medición de interés por entradas (7 de octubre de 2026)

- Se conservó el nombre de evento Meta `TicketClick` y las propiedades existentes `content_name` y `content_category`. Cada activación añade un ID estable de concierto, ciudad conocida, idioma, ubicación del botón y ticketera normalizada.
- El seguimiento acepta solo enlaces HTTPS a los siete dominios observados en las páginas y feeds. Usa un único clic real y descarta clics cancelados; ya no cuenta eventos separados de puntero, tacto ni teclado.
- El evento solo se envía con consentimiento `all`. No incluye la URL de venta, campañas, el parámetro `preview_secret`, texto de página ni datos personales. Se conserva la navegación original del enlace aunque falte o falle `fbq`.
- Se añadieron identificadores a las tarjetas estáticas y generadas, a los botones de WOMEX y Clearwater, y a los selectores de ciudad de Kenny. Se actualizaron las versiones de caché de CSS y JavaScript en 106 páginas y la del script de gira en 33, porque `/assets/` tiene caché inmutable por un año.
- El contrato, proveedores, límites y migración del antiguo campo `destination_url` están en `docs/medicion-interes-entradas.md`. No hay acceso a las cuentas privadas de GTM, GA4 o Meta; no se verificó su configuración ni la recepción final del evento. Clics no equivalen a ventas.

**Verificación:** sintaxis JS y `git diff --check` correctos. En preview protegida, un navegador automatizado usó Meta Pixel simulado y bloqueó todos los destinos de venta. Pasaron consentimiento necesario y completo, activación única, clic cancelado, ratón, teclado y tacto, ES/EN/DE, siete proveedores, exclusión de un dominio parecido, ausencia de URL y parámetros en el payload y continuidad de navegación al faltar o fallar la analítica. No se efectuó una compra ni se enviaron eventos a producción.

Preview lista: https://salanproducciones-244xynhi8-juans-projects-8e14424d.vercel.app. La preview requiere autorización de Vercel. Esta dirección sustituye a la preview de WOMEX citada en la anotación anterior para revisar el estado actual de la rama. Producción no se ha actualizado.

## Fase 3 — Revisión de rendimiento (7 de octubre de 2026)

Se hicieron tres cargas independientes por página y tamaño, con consentimiento solo necesario, navegador Chromium, caché vacía en cada contexto y la misma preview. La transferencia es la medida de Chrome `Network.loadingFinished.encodedDataLength`. Las cifras son laboratorio, no datos de usuarios reales; no se comparan directamente con la muestra única del 6 de octubre, que se obtuvo con otro método.

| Página | Vista | Peticiones (mediana) | Transferencia (mediana) | LCP (mediana) | CLS (mediana) |
| --- | --- | ---: | ---: | ---: | ---: |
| Portada | Escritorio | 17 | 442.168 bytes | 404 ms | 0,0147 |
| Portada | Móvil | 18 | 512.420 bytes | 412 ms | 0,0176 |
| Agenda | Escritorio | 17 | 409.753 bytes | 392 ms | 0,0166 |
| Agenda | Móvil | 16 | 424.960 bytes | 400 ms | 0,0511 |
| Clearwater El Sauzal | Escritorio | 14 | 231.348 bytes | 404 ms | 0,0385 |
| Clearwater El Sauzal | Móvil | 14 | 231.355 bytes | 468 ms | 0,0105 |
| WOMEX | Escritorio | 14 | 344.648 bytes | 388 ms | 0,0033 |
| WOMEX | Móvil | 12 | 214.533 bytes | 364 ms | 0,0142 |

No se reprodujo una demora grande en estas condiciones. El desplazamiento de la agenda móvil fue 0,0511, por debajo del umbral de 0,1 usado habitualmente para clasificar CLS bueno, y cercano a la medición inicial de 0,0520. No hay una mejora puntual de suficiente beneficio demostrado que justifique un cambio visual o de carga ahora; por tanto, la fase queda revisada sin modificar recursos. Las cifras no predicen el rendimiento en todos los teléfonos ni sustituyen mediciones de campo.

## Fase 4 — Revisión de señales para buscadores y asistentes

- El HTML conserva texto de eventos, enlaces de navegación y datos estructurados visibles. No se propone añadir Markdown negociado: la publicación actual es estática en Vercel y no se ha demostrado que el proveedor entregue una variante sincronizada de forma automática. Añadir una segunda versión exigiría mantenerla junto al HTML en tres idiomas.
- No se añaden cabeceras `Link` solo para mejorar un escáner. Hreflang, canonical y enlaces ya están en HTML; falta demostrar una necesidad adicional concreta.
- La política principal documenta tres usos: `search`, `ai-input` y `ai-train`. La ausencia de una preferencia significa que ese uso queda sin expresar, no que se autorice o prohíba. Cloudflare documenta además `use` como una extensión opcional en pruebas para limitar cuánto se conserva o reutiliza el contenido; no se trata como una cuarta señal establecida.
- En producción, `robots.txt` responde 200 y declara `Allow: /` y el sitemap, sin Content Signals. La portada responde 200 como HTML también cuando se solicita `Accept: text/markdown`; no envía `Vary` ni cabecera `Link`. El archivo local `robots.txt` coincide con la respuesta pública.
- No se tocaron `robots.txt`, DNS ni ajustes de Cloudflare. Queda pendiente que Juan decida qué señales expresa para búsqueda, uso como entrada de IA y entrenamiento; la extensión `use` queda aparte. La decisión se registrará antes de modificar reglas.

Referencias consultadas el 7 de octubre de 2026: [Cloudflare: Content Signals Policy](https://blog.cloudflare.com/content-signals-policy/), [Cloudflare: directivas y extensión `use` en `robots.txt`](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/), [Cloudflare: tipos de señal leídos por su API](https://developers.cloudflare.com/api/resources/ai_audit/subresources/robots/) y [Google: funciones de IA y sitios web](https://developers.google.com/search/docs/appearance/ai-features). Google indica que sus funciones de búsqueda con IA no requieren marcado ni archivos especiales aparte de los fundamentos SEO. La página del escáner no ofreció contenido legible en esta consulta; sus resultados se citan únicamente como la instantánea descrita en el plan.
