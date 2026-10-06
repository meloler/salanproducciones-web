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

- Preview Vercel lista: https://salanproducciones-eouzsoxez-juans-projects-8e14424d.vercel.app. Requiere iniciar sesión en Vercel.
- En esa preview se comprobaron portada, agenda y las dos fichas de Clearwater en ES/EN/DE; enlaces a entradas y campañas conservados; fechas del ItemList enlazadas a cada idioma; las seis imágenes WOMEX cargaron en los tres idiomas. También cargaron las imágenes de seis páginas culturales EN/DE y las cinco referencias corregidas del archivo.
- La preview sigue mostrando 26,20 € con gastos incluidos para Telde. Tureserva presenta además un precio desde 25 €; queda pendiente confirmar el total con cargos.
- Producción no se ha actualizado. Espera la revisión y autorización expresa de Juan antes de publicar.

La vuelta atrás del cambio es revertir el commit de esta rama o cerrar la rama sin integrarla. Producción permanece en el commit base.
