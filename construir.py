"""Arma index.html (el globo) a partir de plantilla.html y los datos públicos de la carpeta datos/.

Uso:  python construir.py
- plantilla.html          diseño del globo (lo edita el chat "Globo")
- datos/estudiantes.json  estudiantes: n, ci, pa, la, lo, y, pr, f, v   (lo actualiza el chat "Datos")
- datos/capas_extra.json  películas del festival y equipo/docentes       (lo actualiza el chat "Datos")
Solo datos públicos: nunca correos, teléfonos, direcciones ni documentos.
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
leer = lambda *p: open(os.path.join(AQUI, *p), encoding="utf-8").read()
COMPACTO = dict(ensure_ascii=False, separators=(",", ":"))

est = json.loads(leer("datos", "estudiantes.json"))
extra = json.loads(leer("datos", "capas_extra.json"))
html = leer("plantilla.html")
for marca in ("/*__DATA__*/[]", "/*__EXTRA__*/{}"):
    assert marca in html, f"falta {marca} en plantilla.html"
html = html.replace("/*__DATA__*/[]", json.dumps(est, **COMPACTO)).replace("/*__EXTRA__*/{}", json.dumps(extra, **COMPACTO))
open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8").write(html)
print(f"index.html listo: {len(est)} estudiantes, {len({d['n'] for d in extra.get('docentes', [])})} equipo/docentes, "
      f"{len({(f['t'], f['y']) for f in extra.get('peliculas', [])})} películas")
