# Guia multidioma ES / EN / DE

Esta web usa paginas estaticas reales para cada idioma. No se usa un traductor automatico en vivo.

## Estructura

- Espanol principal: `/`
- Ingles: `/en/`
- Aleman: `/de/`
- Conciertos en ingles: `/en/concerts/2026/<slug>/`
- Conciertos en aleman: `/de/konzerte/2026/<slug>/`

Los slugs de conciertos se mantienen iguales entre idiomas para reducir errores.

## Recursos compartidos entre idiomas

- Las imagenes compartidas por varias versiones de una pagina deben usar una ruta absoluta desde la raiz del sitio (`/ruta/al/archivo`), no una ruta relativa (`./archivo`).
- Antes de publicar, confirmar que el archivo existe en la ruta indicada. Una ruta relativa dentro de `/en/` o `/de/` se resuelve desde esa carpeta y puede dar 404 si el recurso solo esta guardado junto a la pagina en espanol.
- Las imagenes de WOMEX se guardan en `proyectosculturales/womex/` y se comparten mediante rutas como `/proyectosculturales/womex/logo.webp`.
- Las imagenes de Cinezín y Festival Sonora también se comparten desde `/proyectosculturales/<proyecto>/`. Al traducir una página, el generador debe conservar esas rutas compartidas y no convertirlas en rutas relativas al idioma.

## Datos y tarjetas de conciertos

- `conciertos.json` es la entrada que lee `tools/generate_multilang.py`; el generador crea `concerts.en.json` y `concerts.de.json`.
- `assets/js/main.js` usa los tres feeds para pintar las tarjetas dinámicas y separar próximos conciertos del archivo según su fecha de fin.
- La portada y la agenda también tienen tarjetas HTML iniciales para que la información y las entradas sigan disponibles sin JavaScript. Actualiza esos bloques, el carrusel móvil y el ItemList de datos estructurados junto con los feeds.
- No ejecutes el generador completo para arreglar una página sin revisar antes todos los archivos que sobrescribe. Después de editar, usa `python tools/check_site_resources.py` para comprobar recursos compartidos, feeds y tarjetas estáticas.

## SEO obligatorio

Cada pagina debe tener:

- `html lang` correcto: `es-ES`, `en` o `de`.
- Canonical apuntando a si misma.
- Enlaces `hreflang` reciprocos para `es`, `en`, `de` y `x-default`.
- `og:locale` correcto cuando exista Open Graph: `es_ES`, `en_US` o `de_DE`.
- Textos visibles, metadatos, breadcrumbs y Schema.org en el idioma de la pagina.

## Selector de idioma

El selector `ES | EN | DE` debe apuntar siempre a la pagina equivalente. Si una equivalencia no existe durante una migracion, se enlaza a la home del idioma.

## Conciertos nuevos

Cuando se cree una landing nueva de concierto hay que crear:

1. Landing en espanol.
2. Landing en ingles.
3. Landing en aleman.
4. Entrada en `conciertos.json`.
5. Entrada en `concerts.en.json`.
6. Entrada en `concerts.de.json`.
7. URLs de las tres versiones en `sitemap.xml`.

No se deben inventar datos. Los nombres de artistas, salas, ciudades, promotores y marcas de venta se mantienen tal como esten confirmados.

## Verificacion antes de publicar

- Abrir la landing en los tres idiomas.
- Comprobar selector de idioma.
- Comprobar canonical y hreflang.
- Comprobar que las tarjetas dinamicas cargan en el idioma correcto.
- Comprobar CTAs de compra y UTMs.
- Comprobar que no quedan placeholders.
