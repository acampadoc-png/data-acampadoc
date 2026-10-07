# data.acampadoc.com

Sitio público de datos de ACAMPADOC (GitHub Pages).

- `index.html`: globo de la comunidad (estudiantes, equipo y docentes, películas del festival; cortos de estudiantes 2012–2024).
- Se genera con `acampadoc_censo/exportar.py` y `preparar_sitio_data.py` (repo `tareas`). No editar a mano: regenerar y volver a subir.
- Solo datos públicos: nombre, ciudad, país, programa, años, proyecto y enlace al corto. Nunca correos, teléfonos ni documentos.
- **Modo revisión**: `robots.txt` y la etiqueta `noindex` impiden que Google lo indexe. Se quitan al lanzar (`preparar_sitio_data.py --lanzar`).
