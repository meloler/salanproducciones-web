# Revisión SEO · 5 septiembre 2026

Estado: rama de prueba; producción sin modificar. No es una certificación de Google ni una garantía de posicionamiento.

## Cambios de esta revisión

- Portada ES/EN/DE: restaurada la cabecera original con el texto de trayectoria, 35+ años y 700+ conciertos, según petición de Juan. Se conserva la compra desde la agenda hacia la landing de Kenny.
- Santiago: Juan confirma inicio del show a las 20:00. Eliminado el aviso de discrepancia; se mantiene información de acceso desde 16 años.
- Kenny: página de gira conservada. Se publican en la rama 10 fichas de concierto en cada idioma (30 URLs), cada una centrada en una fecha real, con compra directa, precio total, dirección visible y un solo MusicEvent. No se usan fragmentos #ciudad como URLs independientes para Google.
- La gira usa ItemList y enlaces HTML a las fichas. Las seis páginas de giras pasadas de Acantha usan CollectionPage, evitando presentar un calendario de varias actuaciones como una página apta para resultados de un único evento.
- Canonical propio y alternates recíprocos ES/EN/DE/x-default; title, description y metadatos sociales propios para cada ficha de Kenny. Breadcrumbs con la jerarquía real home → gira → ciudad.
- Sitemap ampliado a 105 URLs canónicas; sin URLs de preview ni herramientas internas. Herramientas en /tools reciben X-Robots-Tag noindex.
- Corregidos títulos repetidos de conciertos y avisos legales. Se conserva robots.txt permitiendo el rastreo y declarando el sitemap.
- Se reutilizan los WebP existentes y sus variantes responsive. No se añade un framework ni dependencias de ejecución.

## Evidencia y pruebas

- `python tools/check_seo.py`: 105 URLs existentes, canonical propio, metadescripción, título único por idioma, alternates recíprocos y JSON-LD parseable; sin noindex en páginas del sitemap.
- `python tools/check_kenny_sales.py`: 30 fichas con fecha, precio, lugar y ticketera coherentes con la fuente; diez enlaces de compra sin JavaScript en cada página de gira.
- `node --check assets/js/kenny-tour.js`.
- Se ha intentado validar el HTML completo de Santiago en Rich Results Test. Google devuelve “Inicia sesión e inténtalo de nuevo”. No existe un resultado aprobado del validador oficial en esta revisión.
- Los campos recomendados desconocidos, como hora de finalización y fecha de inicio de venta, se omiten. No se inventan para eliminar advertencias.

## Mantenimiento reproducible

`data/kenny-tour-2026.json` contiene fechas, precios, direcciones y fuentes. Las páginas de gira sirven como plantillas visuales y las traducciones de las fichas están en el generador.

1. Actualizar los datos contrastados y las plantillas si cambia el diseño.
2. Ejecutar `python tools/build_kenny_events.py`.
3. Ejecutar ambas comprobaciones y revisar una ficha por idioma en la preview.
4. Versionar los recursos CSS/JS si cambian, pues Vercel usa caché inmutable para assets.

El generador multidioma histórico puede sobrescribir las plantillas: revisar sus cambios y ejecutar este generador después. Conservar las URL cuando termine un concierto y actualizar su información/estado real; no redirigir indiscriminadamente todas las páginas antiguas a la home.

## Límites y comprobaciones tras aprobación de publicación

La preview está protegida y no es la versión indexable. Después de publicar, validar las URL públicas con Rich Results Test y Search Console, enviar el sitemap y revisar indexación. Estas acciones no se han realizado porque producción sigue pendiente de aprobación.

Core Web Vitals requiere mediciones: no se afirma un 100/100 ni aprobación de LCP, INP y CLS. Deben medirse en la URL pública con PageSpeed Insights y, cuando haya suficiente tráfico, con datos reales de Search Console/CrUX. Tampoco se han comprobado acciones manuales ni el estado privado de Search Console.

La revisión técnica de las 105 páginas no verifica cada dato histórico, derecho de imagen o afirmación editorial de toda la web. El cartel de Kenny original conserva textos de premios pendientes de revisión de diseño. Las páginas nuevas reutilizan el cartel autorizado existente, sin modificarlo ni inventar premios.

## Documentación oficial de Google consultada

- [Search Essentials](https://developers.google.com/search/docs/essentials): requisitos y buenas prácticas; cumplirlos no garantiza rastreo, indexación o aparición.
- [Event: directrices técnicas](https://developers.google.com/search/docs/appearance/structured-data/event#technical-guidelines): URL propia y página centrada en un solo evento; coherencia de datos y fechas.
- [Versiones localizadas](https://developers.google.com/search/docs/specialty/international/localized-versions): enlaces de idioma completos y recíprocos.
- [Rich Results Test](https://search.google.com/test/rich-results): prueba oficial pendiente de acceso.

Las direcciones proceden de las fichas de Tickety, [Sala Capitol](https://www.salacapitol.com/contacto/), [Aclam Club](https://www.aclamclub.cat/) y [Enterticket / La Bohemia](https://www.enterticket.es/eventos/eterno-tour-kadec-santa-anna-en-castellon-548992). Cada fila del JSON conserva su fuente. Santiago 20:00 confirmado directamente por Juan en esta conversación.
