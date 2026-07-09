# Guia multidioma ES / EN / DE

Esta web usa paginas estaticas reales para cada idioma. No se usa un traductor automatico en vivo.

## Estructura

- Espanol principal: `/`
- Ingles: `/en/`
- Aleman: `/de/`
- Conciertos en ingles: `/en/concerts/2026/<slug>/`
- Conciertos en aleman: `/de/konzerte/2026/<slug>/`

Los slugs de conciertos se mantienen iguales entre idiomas para reducir errores.

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
