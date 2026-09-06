> Revisión posterior: la home original se ha restaurado y Juan ha confirmado Santiago a las 20:00. El aviso se ha retirado. El mantenimiento actual y los cambios SEO están en [seo-preview.md](seo-preview.md). Lo siguiente documenta la primera propuesta.

# Preview de venta de entradas · Kenny · 5 septiembre 2026

Rama: `mejora/entradas-kenny-preview`. No fusionar ni publicar en producción sin la revisión de Juan.

## Cambios

- Portada orientada a la gira y a elegir ciudad. La historia de Juan permanece debajo de la agenda.
- Selector accesible con diez ciudades, total con gastos, ticketera concreta y acceso al vídeo existente.
- Información y compra antes del cartel en móvil. Barra inferior sincronizada con la ciudad, oculta mientras se muestra el consentimiento de cookies.
- Diez enlaces estáticos dentro de “Todas las fechas y entradas” como alternativa sin JavaScript.
- Compra desde portada/agenda lleva al selector completo, incluyendo Santiago.
- Horas, zona horaria peninsular en septiembre (`+02:00`), precios, biografía y número de ciudades corregidos en ES/EN/DE. Se eliminan horas de finalización no contrastadas.
- Popup automático de newsletter desactivado en las páginas de conciertos ES/EN/DE. Formularios de suscripción existentes conservados.
- Selector de idioma usa rutas internas, conserva campaña y ciudad en Kenny y permite revisar idiomas dentro de Vercel preview.
- Conciertos caducados de junio retirados del HTML inicial de portada y agenda. La actualización dinámica sigue funcionando.

La mayoría de los archivos modificados solo reciben `?v=20260905` en la referencia a main.js: Vercel sirve `/assets` con caché inmutable durante un año. Al cambiar otra vez un recurso compartido, cambiar también su versión en todos sus consumidores.

## Fuentes de horarios y precios

Consulta del 5 septiembre 2026. Los precios son de una entrada general; no se ha completado ninguna compra.

| Ciudad | Septiembre | Hora | Total con gastos |
|---|---:|---:|---:|
| Donosti | 9 | 20:30 | 27,25 € |
| Bilbao | 10 | 21:30 | 27,25 € |
| Ponferrada | 11 | 21:00 | 27,25 € |
| Santiago | 13 | 20:00* | 27,50 € |
| A Coruña | 15 | 20:30 | 27,25 € |
| Valladolid | 16 | 21:00 | 27,25 € |
| Zaragoza | 17 | 21:45 | 27,25 € |
| Castellón | 18 | 21:00 | 27,25 € |
| Valencia | 19 | 19:30 | 27,25 € |
| Barcelona | 20 | 20:00 | 35,97 € |

Horarios: [listado Tickety](https://tickety.es/entity/kenny-blues-boss-wayne). Los enlaces individuales están en `data/kenny-tour-2026.json`. Los totales de Tickety se comprobaron seleccionando una entrada sin continuar: 25 + 2,25 € salvo Barcelona, 33 + 2,97 €.

*Santiago: [Sala Capitol](https://www.salacapitol.com/) y el [formulario de compra](https://salacapitol.entradas.plus/entradas/es/comprarEvento?idEvento=21027) muestran 20:00. La [descripción de la ticketera](https://salacapitol.entradas.plus/entradas/es/kennybluesbosswayneband-capitol) dice 19:00. Se usa 20:00 y se muestra un aviso en la preview. Confirmar con Capitol y corregir la descripción antes de difusión. Entrada general 25 € + 2,50 €; acceso desde 16 años.

Biografía y premios: [web oficial de Kenny](https://kennybluesboss.com/bio). Spokane; más de 50 años; Juno 2006, Hall of Fame 2017 y premio Pinetop Perkins 2024. No se reutiliza la afirmación “ganador de un Grammy” de algunas tiqueteras.

El cartel original no se ha rediseñado: contiene textos sobre premios que conviene revisar con la persona que lo diseñó. La copia de texto de la web ya usa los datos contrastados.

## Revisión y mantenimiento

- `python tools/check_kenny_sales.py`: 30 fichas equivalentes, diez URLs concretas, precios, fechas, zona horaria, enlaces sin JS, assets y feeds.
- `node --check assets/js/main.js` y `node --check assets/js/kenny-tour.js`.
- `tools/qa-responsive.html?width=375` permite revisar la página en un iframe de 375 píxeles CSS. Admite 320, 375, 390, 768 y 1280. `path` permite elegir otra ruta local. Es una utilidad de revisión sin indexación, no una página enlazada al público. No equivale a probar en un dispositivo iOS real.
- Revisar en navegador: ciudad, hora y precio; ambas compras con el mismo destino; campañas UTM; cambio de idioma; vídeo; menú; cookies; ausencia de popup en conciertos.
- Los clics a ticketera no equivalen a ventas. El seguimiento existente sigue sujeto al consentimiento. Para confirmar ventas y atribución hacen falta los informes de las tiqueteras.
- El bloque destacado de portada es editorial: retirarlo o sustituirlo al terminar la gira, el 20 de septiembre. El filtro de agenda ya excluye eventos caducados automáticamente.
- `data/kenny-tour-2026.json` es la instantánea contrastada usada por la comprobación; cambiarla no regenera el HTML. Si cambia una fecha/precio, actualizar las tres páginas (datos embebidos, enlaces estáticos y schema), los feeds si procede, y pasar la comprobación.
- El generador multidioma histórico no se ha ejecutado; puede sobrescribir traducciones de estas páginas. Conservar las nuevas secciones al regenerar y ejecutar la comprobación antes de publicar.

## Enlaces para campañas

Ejemplo para Valencia, cambiando la fuente según quién comparta:

`https://www.salanproducciones.com/conciertos/2026/kenny-blues-boss-wayne-gira-espana-2026/?utm_source=instagram&utm_medium=social&utm_campaign=kenny_2026&utm_content=valencia_video#valencia`

Ciudades admitidas en el fragmento: `donosti`, `bilbao`, `ponferrada`, `santiago`, `coruna`, `valladolid`, `zaragoza`, `castellon`, `valencia`, `barcelona`.

Preparar un vídeo y texto por ciudad reutilizando material autorizado; dirigir cada publicación a su fragmento. No se han enviado mensajes, publicado anuncios ni gastado presupuesto en esta intervención.

## Resultado de revisión

- Preview Vercel lista; las diez selecciones muestran su ciudad, hora, total y enlace correctos. El botón móvil comparte destino y campaña con el principal.
- Navegación ES → EN conservando Santiago y UTM verificada. Portada muestra cinco próximos conciertos, sin las tarjetas de junio.
- Diseño revisado en escritorio y en iframes móviles de 390 y 320 píxeles CSS; alemán incluido. Se corrige el ajuste de los botones de cookies en pantallas estrechas.
- Enlace al vídeo y activación del reproductor comprobados. No se verifica la entrega de entradas ni se realiza un pago.
- La revisión detecta logs ajenos a la web (extensión del navegador y login de Vercel), sin error de aplicación observado en las acciones probadas.
