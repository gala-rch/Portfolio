"""
Pictogrammes des annotations (dessins au trait, gris discret).
Main, pouce, empreintes de pieds et feuille : Phosphor Icons, style « light »,
licence MIT (c) 2023 Phosphor Icons, phosphoricons.com.
Lèvres : dessinées pour ce projet, dans le même style.
Toutes les icônes sont dans une boîte de 256 × 256.
"""

# Formes pleines (contour déjà épaissi) : on les remplit
PLEIN = {
    "main": "M188,90a25.8,25.8,0,0,0-14,4.11V60a26,26,0,0,0-40.59-21.51A26,26,0,0,0,82,44V54.11A26,26,0,0,0,42,76v76a86,86,0,0,0,172,0V116A26,26,0,0,0,188,90Zm14,62a74,74,0,0,1-148,0V76a14,14,0,0,1,28,0v44a6,6,0,0,0,12,0V44a14,14,0,0,1,28,0v68a6,6,0,0,0,12,0V60a14,14,0,0,1,28,0v70.39A46.07,46.07,0,0,0,122,176a6,6,0,0,0,12,0,34,34,0,0,1,34-34,6,6,0,0,0,6-6V116a14,14,0,0,1,28,0Z",
    "pouce": "M232.49,81.44A22,22,0,0,0,216,74H158V56a38,38,0,0,0-38-38,6,6,0,0,0-5.37,3.32L76.29,98H32a14,14,0,0,0-14,14v88a14,14,0,0,0,14,14H204a22,22,0,0,0,21.83-19.27l12-96A22,22,0,0,0,232.49,81.44ZM30,200V112a2,2,0,0,1,2-2H74v92H32A2,2,0,0,1,30,200ZM225.92,97.24l-12,96A10,10,0,0,1,204,202H86V105.42l37.58-75.17A26,26,0,0,1,146,56V80a6,6,0,0,0,6,6h64a10,10,0,0,1,9.92,11.24Z",
    "pieds": "M104,162H48a6,6,0,0,0-6,6v12a34,34,0,0,0,68,0V168A6,6,0,0,0,104,162Zm-6,18a22,22,0,0,1-44,0v-6H98ZM76,18C65.2,18,54.56,27.91,46,45.9c-13.66,28.82-18.29,71.53,0,93.9a6,6,0,0,0,4.65,2.2h50.53a6,6,0,0,0,4.65-2.2c18.32-22.37,13.69-65.08,0-93.9C97.41,27.91,86.77,18,76,18ZM98.23,130H53.74c-10.09-15.18-11.69-47.65,3.14-79C64.24,35.51,71.77,30,76,30s11.75,5.51,19.1,21C109.92,82.35,108.32,114.82,98.23,130ZM208,186H152a6,6,0,0,0-6,6v12a34,34,0,0,0,68,0V192A6,6,0,0,0,208,186Zm-6,18a22,22,0,0,1-44,0v-6h44Zm-47.27-38h50.53a6,6,0,0,0,4.65-2.2c18.32-22.37,13.69-65.08,0-93.9C201.44,51.91,190.8,42,180,42s-21.43,9.91-30,27.9c-13.66,28.82-18.29,71.53,0,93.9A6,6,0,0,0,154.75,166Zm6.17-91c7.35-15.53,14.88-21,19.1-21s11.74,5.51,19.1,21c14.83,31.31,13.23,63.78,3.14,79H157.77C147.68,138.82,146.08,106.35,160.92,75Z",
    "feuille": "M221.45,40.19a6,6,0,0,0-5.64-5.64C140.43,30.11,80.14,52.71,54.53,95c-17.44,28.79-16.76,62.8,1.79,96.2L35.76,211.76a6,6,0,1,0,8.48,8.48L64.8,199.68c17.27,9.59,34.7,14.41,51.49,14.41A85.38,85.38,0,0,0,161,201.47C203.29,175.86,225.88,115.57,221.45,40.19Zm-66.66,151c-24.08,14.58-52.64,14.37-81.13-.39l90.59-90.59a6,6,0,0,0-8.48-8.48L65.18,182.34c-14.76-28.49-15-57-.39-81.13,22.68-37.43,76.63-57.8,145-54.95C212.59,114.58,192.22,168.54,154.79,191.21Z",
}

# Formes au trait : on les dessine avec un contour de 12 (même épaisseur que Phosphor light)
TRAIT = {
    "levres": [
        "M28,130 C60,98 90,80 110,92 C119,97 123,101 128,101 C133,101 137,97 146,92 C166,80 196,98 228,130",
        "M28,130 C70,196 186,196 228,130",
        "M28,130 C80,142 176,142 228,130",
    ],
}

# Partie annotée → pictogramme(s) (« main ×2 » = deux mains pour les 10 doigts)
PICTO_DE = {
    "Parole et mastication": ["levres"],
    "Les 10 doigts": ["main", "main_miroir"],
    "Pouce": ["pouce"],
    "Les 2 pieds": ["pieds"],
    "Parties génitales": ["feuille"],
}


def dessin(nom, x, y, taille, couleur):
    """SVG d'un pictogramme dont le coin haut-gauche est (x, y)."""
    miroir = nom.endswith("_miroir")
    nom = nom.replace("_miroir", "")
    k = taille / 256
    tr = (f"translate({x + taille:.1f},{y:.1f}) scale({-k:.4f},{k:.4f})" if miroir
          else f"translate({x:.1f},{y:.1f}) scale({k:.4f})")
    if nom in PLEIN:
        return f'<path transform="{tr}" d="{PLEIN[nom]}" fill="{couleur}"/>'
    return "".join(f'<path transform="{tr}" d="{d}" fill="none" stroke="{couleur}" stroke-width="12" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>' for d in TRAIT[nom])


def groupe(partie, cx, cy, taille, couleur):
    """Pictogramme(s) d'une partie, centrés sur (cx, cy)."""
    noms = PICTO_DE[partie]
    larg = taille * len(noms) + 2 * (len(noms) - 1)
    x = cx - larg / 2
    out = []
    for n in noms:
        out.append(dessin(n, x, cy - taille / 2, taille, couleur))
        x += taille + 2
    return f'<g id="picto-{partie.split()[-1].lower()}">' + "".join(out) + "</g>"
