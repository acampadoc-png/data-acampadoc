"""Conecta la cuenta de Vimeo de ACAMPADOC con el globo: propone el video de cada estudiante que aún no tiene enlace.

Uso (desde esta carpeta, con Python 3.9+ y sin instalar nada):
  1) export VIMEO_TOKEN=xxxx          # token personal, scopes: public + private (developer.vimeo.com/apps)
  2) python vimeo_enlazar.py          # lee todos los videos de la cuenta y escribe vimeo_propuestas.csv
  3) abre vimeo_propuestas.csv, escribe "si" en la columna "aceptar" de las filas correctas y guarda
  4) python vimeo_enlazar.py --aplicar vimeo_propuestas.csv   # añade esos enlaces a datos/estudiantes.json
  5) python construir.py              # regenera index.html

Cómo busca: el nombre del estudiante en el título o la descripción (créditos) del video, el nombre de su
proyecto en el título y el año. Solo propone; nada entra al globo sin el "si".
Respeta las reglas del README: no propone cortos de estudiantes que solo estuvieron en 2025/2026 y
avisa de los videos que Vimeo no deja insertar (privacidad) o que no son públicos.
El token nunca se guarda; vimeo_propuestas.csv está en .gitignore y no se publica.
"""
import csv, json, os, re, sys, unicodedata, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(AQUI, "datos", "estudiantes.json")
SALIDA = os.path.join(AQUI, "vimeo_propuestas.csv")
API = os.environ.get("VIMEO_API", "https://api.vimeo.com")
NO_ENLAZAR = {"2025", "2026"}          # cortos que siguen en festivales
COLUMNAS = ["aceptar", "estudiante", "años", "proyecto", "titulo_vimeo", "enlace", "privacidad", "insercion", "puntos", "motivo"]


def norm(t):
    t = unicodedata.normalize("NFD", str(t or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return " " + re.sub(r"[^a-z0-9ñ]+", " ", t).strip() + " "


def pedir(ruta, token):
    req = urllib.request.Request(API + ruta, headers={
        "Authorization": "bearer " + token, "Accept": "application/vnd.vimeo.*+json;version=3.4"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def videos_de_vimeo(token):
    ruta = "/me/videos?per_page=100&fields=name,link,description,privacy.view,privacy.embed"
    todos = []
    while ruta:
        pagina = pedir(ruta, token)
        todos += pagina.get("data", [])
        ruta = (pagina.get("paging") or {}).get("next")
        print(f"  {len(todos)} videos leídos…", end="\r")
    print()
    return todos


def puntuar(p, v):
    """Puntos de que el video v sea del estudiante p, con el motivo."""
    titulo, texto = norm(v.get("name")), norm(v.get("name")) + norm(v.get("description"))
    partes = [w for w in norm(p["n"]).split() if len(w) >= 3]
    puntos, motivos = 0, []
    if len(partes) >= 2 and partes[0] in texto.split() and sum(w in texto.split() for w in partes[1:]) >= 1:
        completos = all(w in texto.split() for w in partes)
        puntos += 4 if completos else 3
        motivos.append("nombre completo" if completos else "nombre y apellido")
    pr = norm(p.get("pr")).strip()
    if len(pr) >= 4 and f" {pr} " in titulo:
        puntos += 3; motivos.append("proyecto en el título")
    años = re.findall(r"20[12]\d", v.get("name") or "")
    if años:
        if set(años) & set(p["y"]):
            puntos += 1; motivos.append("año")
        else:
            puntos -= 3; motivos.append("año distinto")
    return puntos, ", ".join(motivos)


def titulo_para(p, v):
    """Mismo estilo que los enlaces ya cargados: «TÍTULO [Programa año]»."""
    nombre = (v.get("name") or "").strip()
    if re.search(r"\[.+\]", nombre):
        return nombre
    año = max(p["y"])
    prog = (p["y"][año].get("p") or [""])[0]
    return f"{nombre} [{prog} {año}]".replace(" ]", "]")


def proponer():
    token = os.environ.get("VIMEO_TOKEN")
    if not token:
        sys.exit("Falta VIMEO_TOKEN (créalo en https://developer.vimeo.com/apps → Generate token, scopes public y private).")
    est = json.load(open(EST, encoding="utf-8"))
    print("Leyendo la cuenta de Vimeo…")
    vids = [v for v in videos_de_vimeo(token) if v.get("link")]
    usados = {u for p in est for _, u in p.get("v", [])}

    # 1) enlaces que ya están en el globo pero que Vimeo no dejará ver
    por_link = {v["link"]: v for v in vids}
    for p in est:
        for t, u in p.get("v", []):
            v = por_link.get(u)
            if v and ((v.get("privacy") or {}).get("embed") == "private" or (v.get("privacy") or {}).get("view") in ("nobody", "contacts")):
                print(f"⚠ No se verá en el globo (privacidad en Vimeo): {p['n']} – {t} – {u}")

    # 2) propuestas para quien no tiene video
    filas = []
    candidatos = [p for p in est if not p.get("v") and not set(p["y"]) <= NO_ENLAZAR]
    for p in candidatos:
        opciones = sorted(((*puntuar(p, v), v) for v in vids if v["link"] not in usados), key=lambda x: -x[0])
        for puntos, motivo, v in [o for o in opciones if o[0] >= 3][:3]:
            priv = v.get("privacy") or {}
            filas.append({"aceptar": "", "estudiante": p["n"], "años": " ".join(sorted(p["y"])), "proyecto": p.get("pr") or "",
                          "titulo_vimeo": v.get("name", ""), "enlace": v["link"], "privacidad": priv.get("view", ""),
                          "insercion": priv.get("embed", ""), "puntos": puntos, "motivo": motivo})
    with open(SALIDA, "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig: Excel muestra bien las tildes
        w = csv.DictWriter(f, COLUMNAS); w.writeheader(); w.writerows(filas)
    print(f"{len(vids)} videos en Vimeo · {len(candidatos)} estudiantes sin enlace · "
          f"{len({r['estudiante'] for r in filas})} con propuesta → {os.path.basename(SALIDA)}")
    print('Marca "si" en la columna aceptar y luego: python vimeo_enlazar.py --aplicar vimeo_propuestas.csv')


def aplicar(ruta):
    est = json.load(open(EST, encoding="utf-8"))
    por_nombre = {p["n"]: p for p in est}
    vimeo = re.compile(r"^https://vimeo\.com/\d+(/[0-9a-f]{6,})?$")
    n = 0
    with open(ruta, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if norm(r.get("aceptar")).strip() not in ("si", "x", "yes"):
                continue
            p, u = por_nombre.get(r["estudiante"]), r["enlace"].strip()
            if not p or not vimeo.match(u):
                print(f"Omitido (estudiante o enlace no válido): {r['estudiante']} – {u}"); continue
            if set(p["y"]) <= NO_ENLAZAR:
                print(f"Omitido (2025/2026 no se enlazan): {p['n']}"); continue
            if any(x == u for _, x in p.get("v", [])):
                continue
            p.setdefault("v", []).append([titulo_para(p, {"name": r["titulo_vimeo"]}), u]); n += 1
    with open(EST, "w", encoding="utf-8") as f:
        json.dump(est, f, ensure_ascii=False)   # mismo formato que ya tiene el archivo
    print(f"{n} enlaces añadidos a datos/estudiantes.json. Ahora: python construir.py")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--aplicar":
        aplicar(sys.argv[2])
    elif len(sys.argv) == 1:
        proponer()
    else:
        sys.exit(__doc__)
