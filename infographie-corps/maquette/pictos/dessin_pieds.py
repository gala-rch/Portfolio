import sys
C = "#BDB3A2"
EP = 9
# Pied gauche vu de dessous (gros orteil à droite, voûte creusée côté intérieur), boîte 128 × 270
SOLE = ("M64,262 C46,262 38,248 36,228 C33,200 22,170 19,140 C16,112 32,90 62,88 "
        "C92,86 110,100 108,124 C106,146 80,158 78,182 C76,202 92,216 92,236 C92,254 80,262 64,262 Z")
TOES = [(36, 58, 14, 18), (66, 38, 10, 12.5), (91, 39, 7.5, 9.5), (111, 51, 6.5, 8), (124, 70, 5.5, 6.5)]

def pied(dx, dy, miroir=False):
    tr = f"translate({dx + (128 if miroir else 0)},{dy})" + (" scale(-1,1)" if miroir else "")
    els = [f'<path d="{SOLE}"/>'] + [f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in TOES]
    return f'<g transform="{tr}">' + "".join(els) + "</g>"

# pied droit (miroir du gauche) à gauche, pied gauche à droite : gros orteils vers le centre
contenu = (f'<g fill="none" stroke="{C}" stroke-width="{EP}" stroke-linejoin="round">'
           + pied(0, 0, miroir=True) + pied(144, 0) + "</g>")
w, h = sys.argv[1], sys.argv[2]
print('<?xml version="1.0" encoding="UTF-8"?>\n'
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 20 284 250" width="{w}" height="{h}">\n'
      f'<title>Pieds nus</title>\n<g id="pieds-nus">{contenu}</g>\n</svg>')
