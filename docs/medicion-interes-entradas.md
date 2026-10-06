# Medición de interés por entradas

Actualizado: 7 de octubre de 2026.

## Objetivo

Contar activaciones válidas de enlaces de compra por concierto para entender qué eventos generan interés. Un clic indica intención de visitar la ticketera; no confirma una compra ni sus ingresos.

## Evento

Se conserva el evento personalizado de Meta `TicketClick` para mantener su nombre actual. Solo se envía después de aceptar todas las cookies, al hacer clic en un enlace HTTPS de una ticketera conocida y si el clic no fue cancelado. Un único listener de `click` cubre ratón, tacto y teclado sin contar por separado `pointerdown` o `touchstart`.

| Propiedad | Contenido | Ejemplo |
| --- | --- | --- |
| `concert_id` | Identificador estable del concierto o de la ciudad de una gira | `clearwater-creedence-revival-telde-14-11-2026` |
| `city` | Ciudad confirmada, cuando se conoce | `Telde` |
| `language` | Idioma de la página | `es`, `en`, `de` |
| `button_location` | Tipo de ubicación del botón | `concert_card`, `event_landing`, `tour_selector` |
| `ticket_provider` | Nombre normalizado de la ticketera | `tickety`, `tureservaonline` |

El código solo acepta estos destinos observados en el sitio: `auditorioalfredokraus.es`, `tickety.es`, `tureservaonline.es`, `entradium.com`, `entradas.babylonmadrid.com`, `entradas.elteatroguiniguada.com` y el dominio `entradas.plus` con sus subdominios. Se normalizan a nombres de proveedor estables.

## Datos y compra

- No se adjunta la URL de destino ni sus parámetros, campañas o secretos. Se conservan los enlaces originales y su navegación. El antiguo parámetro `destination_url` se retira; los informes que dependían de él deberán usar `concert_id` y `ticket_provider`.
- Se conservan `content_name` y `content_category` del evento existente para mantener informes agregados básicos.
- El código no impide la navegación ni espera a Meta. Si el píxel falta o falla, el enlace sigue abriendo la ticketera.
- No se envían nombres, textos de formularios, correos ni otros datos personales. No se registra una compra.

## Alcance comprobable y límite

La web carga el píxel de Meta y Google Tag Manager solo con el consentimiento `all`. El código de la página puede comprobarse, pero no se dispone de acceso a las cuentas privadas de Meta, GTM o GA4; por tanto, no se puede confirmar qué etiquetas o informes hay configurados allí ni la recepción final del evento. No se crean propiedades ni contenedores nuevos.

La comprobación de desarrollo usa una función simulada de Meta y bloquea los destinos externos de ticketing. Esto permite verificar las propiedades, el consentimiento y la navegación sin transmitir clics de prueba a las cuentas de producción ni enviar compras.

