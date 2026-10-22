# WOMEX · La prensa habla · 22 octubre2026

SolicitudJuan: incorporar cuatro noticias con carrusel mobilefirst y escritorio en páginaESWOMEX. Rama codex/womex-press-20261022 desde origin/main65471a5; worktree separado preserva cambios locales ajenos del repositorio principal.

## Cambios
Sección #prensa justo después de hero; cuatro tarjetas editoriales con titulares contrastados en páginas delmedio: Canarias7, RTVC/LaRadioCanaria, LaProvincia y LaVozCanaria. URLCanarias7 sin parámetro ref. No imágenes ni logos externos, no titulares inventados, no copia del cuerpo del artículo. Sin fechas porque algunas fuentes contienen fechas incoherentes. Antigua sección Enlosmedios conservada como Enlacesdeinterés con idenlaces-womex, sin perder vínculos originales.

HTMLestático con CSS/JS específicos assets/css/womex-press.css y assets/js/womex-press.js. No alterados globales ni traduccionesEN/DE ni CTAs/píxeles/eventos. Scrollsnap nativo; una tarjeta y siguiente visible móvil, dos tablet y tres escritorio; botones44px, teclado flechas/Home/End sobre pista, contador de tarjetas mayoritariamente visibles, sin autoplay, reducedmotion, focovisible y enlaces legibles sinJS. Sin dependencias.

## Evidencia de pruebas locales ChromeDevTools secuencial
-320/390/768/1440: documentWidth igualviewport, sección dentroancho, cuatrocards y controlesactivos.
-Clicsiguiente a320 movióscroll251px y habilitóAnterior; teclaEnd llevó712px(max712), Siguientedesactivado; Home restableceAnterior desactivado.
-Captura390inspeccionada visualmente, sin popups de cookies/newsletter en la captura (solo ocultados enDOMlocal paraQA; código original intacto). Captura fuera delrepo en workspace-main/reports/womex-press-mobile.png.
-node--check assets/js/womex-press.js correcto; gitdiff--check correcto.
-python tools/check_site_resources.py:1258referencias, feeds y tarjetasestáticasOK.
-python tools/check_seo.py:105URLs sitemap, canonicals, hreflang, títulos yJSON-LDOK.
-Preexistente: hero puede exceder body a320; la nueva sección encaja y documentWidth320. No corregido fueraalcance.

## Publicación
Requiere previewVercel segúnCLAUDE/README y aprobaciónlote antesmain. AccesoCLI Vercel inicialmente bloqueado403proxy; solicitados porvíasoportada loshostsvercel.com,api.vercel.com,www.salanproducciones.com conservandoactuales, pendiente aplicarreinicio. No rotarcredenciales ni desactivarproxy. ProducciónNOmodificada aún.

## Revisión de Juan · 19:12 · miniaturas
Juan solicita pequeñas fotos de las previews. Se añaden las cuatro imágenes OpenGraph originales, verificadas en cada medio y revisadas visualmente. Copias WebP reducidas a640px en assets/images/womex-prensa, total149588bytes(~146KiB); URLdelartículo e imagenoriginal en sources.json. Imágenes decorativas(altvacío porque título/medio ya describen enlace), width/height y aspectratio reservanespacio, lazy/async, sin hotlinking ni dependencia de terceros enrender. CartelRTVC contenido completo sinrecortar. ActualizadosCSSv2 yDESIGN.md.
Comprobaciones320/390/768/1440: lascuatroimágenes cargadas, secciónencajaancho, controlesactivos; capturas390/1440inspeccionadas en reports/womex-press-photos-*.png fuera delrepo.1262referenciaslocalesOK ySEO105URLsOK. Solo ramaPreview; sigue pendiente aprobación expresa para producción.
