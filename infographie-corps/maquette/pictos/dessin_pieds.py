"""Pieds nus, version lisible en petit : trait plus épais, orteils pleins.
python3 make2.py <deux|un> <largeur> <hauteur>"""
import sys
C = "#BDB3A2"
EP = 14   # même épaisseur relative que les icônes Phosphor « light » (12/256)
SOLE = ("M64,262 C46,262 38,248 36,228 C33,200 22,170 19,140 C16,112 32,90 62,88 "
        "C92,86 110,100 108,124 C106,146 80,158 78,182 C76,202 92,216 92,236 C92,254 80,262 64,262 Z")
# orteils pleins, plus gros et bien séparés (gros orteil à gauche, côté intérieur)
TOES = [(38, 54, 15, 19), (70, 36, 10.5, 13), (95, 40, 8.5, 10.5), (113, 55, 7, 8.5), (124, 75, 6, 7)]

def pied(dx, dy, miroir=False):
    tr = f"translate({dx + (128 if miroir else 0)},{dy})" + (" scale(-1,1)" if miroir else "")
    s = f'<path d="{SOLE}" fill="none" stroke="{C}" stroke-width="{EP}" stroke-linejoin="round"/>'
    t = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{C}"/>' for x, y, rx, ry in TOES)
    return f'<g transform="{tr}">{s}{t}</g>'

mode, w, h = sys.argv[1], sys.argv[2], sys.argv[3]
if mode == "deux":
    contenu, vb = pied(0, 0, miroir=True) + pied(144, 0), "-8 14 288 258"
else:
    contenu, vb = pied(0, 0), "4 14 132 258"
print('<?xml version="1.0" encoding="UTF-8"?>\n'
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">\n'
      f'<title>Pieds nus</title>\n<g id="pieds-nus">{contenu}</g>\n</svg>')
