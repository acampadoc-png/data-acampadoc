# Globo de la comunidad ACAMPADOC

Sitio público: https://acampadoc-png.github.io/data-acampadoc/ (GitHub Pages, rama `main`). Enlazado desde acampadoc.com → "Memorias documentales".

## Cómo está organizado (dos chats, sin pisarse)
| Archivo | Qué es | Quién lo cambia |
|---|---|---|
| `plantilla.html` | Diseño y funcionamiento del globo (colores, textos, botones, reproductor, adaptación a pantallas) | Chat **Globo** |
| `datos/estudiantes.json` | Estudiantes: `n` nombre, `ci` ciudad, `pa` país, `la`/`lo` coordenadas, `y` años {año: {p: programas, c: confirmado}}, `pr` proyecto, `f` foto, `v` videos [[título, enlace]] | Chat **Datos** |
| `datos/capas_extra.json` | `peliculas` del festival (t, y, d, pa, la, lo) y `docentes` = equipo y docentes (n, y, m rol, pa, ci, la, lo, v) | Chat **Datos** |
| `construir.py` | Une plantilla + datos → `index.html` | Los dos, después de cada cambio |
| `index.html` | Resultado publicado. **No editar a mano** | — |

Después de cualquier cambio: `python construir.py`, revisar, y subir `index.html` junto con lo modificado.

## Funcionamiento
- **Sin depender de otros servidores:** la librería del globo, la de mapas y el mapa de países están en `lib/` (globe.gl 2.33.1, topojson-client 3.1.0, world-atlas 2). Solo la fuente Inter viene de Google y, si no llega, se usa la del sistema sin frenar la apertura.
- **Pantalla de carga** con el logo; si el globo no puede cargar, lo dice y ofrece volver a intentar.
- **Giro automático:** el planeta vuelve a girar solo tras 20 s sin que nadie lo toque.
- **Un solo estilo en todas las pantallas:** computador, proyector y celular usan el diseño del celular (cabecera compacta, barra "Capas y años", ficha desde abajo). En pantallas anchas va en una columna de 420 px a la izquierda. Decisión de ACAMPADOC, 19 oct 2026; el modo proyección se descartó.
- **Tema anual:** franja "TEMA 2026 · …" sobre la barra de abajo; cambia al tocar un año y enlaza a acampadoc.com/somos/temas. La ficha de la sede lista los temas (tocables) y la trayectoria. Al sumar un año nuevo, agregar su tema en `TEMAS` dentro de `plantilla.html`.
- **Lema:** "Cine al rescate de los patrimonios" en la carga, la cabecera, la sede y el texto para compartir (#CineAlRescate).

## Música
Las 15 pistas de `musica/` son interpretaciones del acordeonista **Gelo Córdoba** (Mogollón, Los Santos), figura del patrimonio musical de Panamá; el concurso de acordeón del Festival de Guararé lleva su nombre. Él compuso *La espigadilla* y *Pica pica*; los demás temas son de otros compositores (Paris Vásquez, Artemio Vargas, Toñito Sáenz, Casimiro Pimentel, Alberto Rodríguez, Colaco Cortez, José de la Rosa Cedeño, Sacramento Córdoba) o tradicionales. El reproductor muestra el nombre de la canción que suena y el crédito "Música de Gelo Córdoba" (decisión de ACAMPADOC, 19 oct 2026); no muestra compositores.
**Derechos:** pendiente guardar aquí la autorización escrita (familia de Gelo Córdoba o titular de la grabación) antes de presentar la música como libre de derechos.

## Reglas
- **Mapas: nunca la proyección de Mercator.** El globo 3D no deforma tamaños. Todo mapa plano (vistas, imágenes, informes, redes) usa **Equal Earth** (en web: `d3.geoEqualEarth`; referencia: https://www.equal-earth.com). Decisión de ACAMPADOC, octubre 2026, en línea con la campaña Correct The Map respaldada por la Unión Africana.
- Solo datos públicos: nombre, ciudad, país, programa, años, proyecto, rol y enlace al video. Nunca correos, teléfonos, direcciones, documentos ni datos de salud o bancarios.
- Los estudiantes aceptaron aparecer (confirmado por ACAMPADOC, octubre 2026).
- Cortos de estudiantes de 2025 y 2026 no se enlazan (siguen en festivales).
- Videos permitidos: vimeo.com y exquisite.tube (PeerTube).
