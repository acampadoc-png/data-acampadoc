# Globo de la comunidad ACAMPADOC

Sitio público: https://acampadoc-png.github.io/data-acampadoc/ (GitHub Pages, rama `main`). Enlazado desde acampadoc.com → "Memorias documentales".

## Cómo está organizado (dos chats, sin pisarse)
| Archivo | Qué es | Quién lo cambia |
|---|---|---|
| `plantilla.html` | Diseño y funcionamiento del globo (colores, textos, botones, reproductor, adaptación a pantallas) | Chat **Globo** |
| `datos/estudiantes.json` | Estudiantes: `n` nombre, `ci` ciudad, `pa` país, `la`/`lo` coordenadas, `y` años {año: {p: programas, c: confirmado}}, `pr` proyecto, `f` foto, `v` videos [[título, enlace]] | Chat **Datos** |
| `datos/capas_extra.json` | `peliculas` del festival (t, y, d, pa, la, lo) y `docentes` = equipo y docentes (n, y, m rol, pa, ci, la, lo, v) | Chat **Datos** |
| `vimeo_enlazar.py` | Conecta con la cuenta de Vimeo y propone el video de cada estudiante sin enlace (se aprueba a mano) | Chat **Datos** |
| `construir.py` | Une plantilla + datos → `index.html` | Los dos, después de cada cambio |
| `index.html` | Resultado publicado. **No editar a mano** | — |

Después de cualquier cambio: `python construir.py`, revisar, y subir `index.html` junto con lo modificado.

## Reglas
- Solo datos públicos: nombre, ciudad, país, programa, años, proyecto, rol y enlace al video. Nunca correos, teléfonos, direcciones, documentos ni datos de salud o bancarios.
- Los estudiantes aceptaron aparecer (confirmado por ACAMPADOC, octubre 2026).
- Cortos de estudiantes de 2025 y 2026 no se enlazan (siguen en festivales).
- Videos permitidos: vimeo.com y exquisite.tube (PeerTube).

## Enlazar películas desde Vimeo
1. Crea un token en https://developer.vimeo.com/apps → *Generate access token* (scopes `public` y `private`). No lo subas nunca al repo.
2. `VIMEO_TOKEN=xxxx python vimeo_enlazar.py` → crea `vimeo_propuestas.csv` (no se publica) con candidatos por estudiante: busca su nombre en los créditos, su proyecto en el título y el año.
3. Abre el CSV, escribe `si` en la columna `aceptar` de las filas correctas.
4. `python vimeo_enlazar.py --aplicar vimeo_propuestas.csv` y luego `python construir.py`.
5. En Vimeo, cada video debe permitir insertarse: *Privacidad → Dónde se puede insertar* = cualquier lugar, o lista con `acampadoc-png.github.io`. El script avisa de los que no se verán.
