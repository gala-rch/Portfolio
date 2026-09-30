"""
Brouillons de graphiques en SVG, à ouvrir dans Illustrator / Figma / Inkscape.

À lancer APRÈS analyse.py (il lit sorties/resultats_USA.xlsx) :
    python3 graphiques.py

Unités : 1 unité SVG = 1 point typographique (1 pt = 0,353 mm).
Chaque fichier est découpé en groupes nommés (fond, grille, rubans-contexte,
rubans-accent, libelles...) qui deviennent des calques dans Illustrator.
Le texte reste du vrai texte (modifiable), police générique à remplacer.

Pour changer les parties mises en avant ou les couleurs : section RÉGLAGES.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd

ICI = Path(__file__).parent
RES = ICI / "sorties" / "resultats_USA.xlsx"
OUT = ICI / "graphiques"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- RÉGLAGES
# Une partie mise en avant par région (clé = libellé exact de l'affiche)
ACCENTS = {
    "Parole et mastication": "#2a78d6",  # bleu
    "Les 10 doigts":         "#eb6834",  # orange
    "Les 2 pieds":           "#1baf7a",  # vert d'eau
    "Parties génitales":     "#4a3aa7",  # violet
}
# (palette vérifiée daltonisme : les 4 couleurs restent distinctes entre elles)

GROUPES = ["Fonctions & sens", "Bras & mains", "Jambes & pieds", "Visage, dents & intimité"]
CRIT = ["Difficulté à s'en passer", "Colère si on en perd l'usage",
        "Gratitude si on en retrouve l'usage", "Prix sur le marché", "Dédommagement à verser"]
CRIT_2L = [("Difficulté", "à s'en passer"), ("Colère si on", "en perd l'usage"),
           ("Gratitude si on", "en retrouve l'usage"), ("Prix sur", "le marché"),
           ("Dédommagement", "à verser")]
CRIT_COURT = ["Difficulté", "Colère", "Gratitude", "Prix", "Dédomm."]

POLICE = "Helvetica, Arial, sans-serif"
ENCRE = "#1a1a1a"        # texte principal
ENCRE_2 = "#6b6962"      # texte secondaire
GRIS_CTX = "#dcd9d0"     # rubans de contexte (autres régions)
GRIS_GRP = "#a19e94"     # rubans de la région, non mis en avant
FOND = "#fbf7ee"         # crème (calque « fond », à supprimer si besoin)
SEQ = ["#104281", "#1c5cab", "#2a78d6", "#5598e7", "#86b6ef", "#b7d3f6", "#e6effb"]  # 1 → 35


# ---------------------------------------------------------------- OUTILS SVG
def svg(largeur, hauteur, contenu, titre):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}pt" height="{hauteur}pt" '
            f'viewBox="0 0 {largeur} {hauteur}" font-family="{POLICE}">\n'
            f'<title>{escape(titre)}</title>\n'
            f'<g id="fond"><rect width="{largeur}" height="{hauteur}" fill="{FOND}"/></g>\n'
            f'{contenu}</svg>\n')


def texte(x, y, s, taille=7, ancre="start", couleur=ENCRE, gras=False, extra=""):
    g = ' font-weight="bold"' if gras else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{taille}" text-anchor="{ancre}" '
            f'fill="{couleur}"{g}{extra}>{escape(str(s))}</text>')


def ruban(xs, ys, couleur, epaisseur, ident=""):
    """Courbe lisse passant par (xs[i], ys[i]) : un S entre chaque colonne."""
    d = f"M{xs[0]:.1f},{ys[0]:.1f}"
    for i in range(1, len(xs)):
        xm = (xs[i - 1] + xs[i]) / 2
        d += f" C{xm:.1f},{ys[i-1]:.1f} {xm:.1f},{ys[i]:.1f} {xs[i]:.1f},{ys[i]:.1f}"
    i = f' id="{ident}"' if ident else ""
    return (f'<path{i} d="{d}" fill="none" stroke="{couleur}" stroke-width="{epaisseur}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def ident(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower())


def entetes(xs, y, taille=7):
    out = []
    for x, (l1, l2) in zip(xs, CRIT_2L):
        out.append(texte(x, y, l1, taille, "middle", ENCRE, True))
        out.append(texte(x, y + taille + 1.5, l2, taille, "middle", ENCRE, True))
    return "\n".join(out)


def lire():
    rangs = pd.read_excel(RES, sheet_name="rangs", index_col=0)
    return rangs


# ---------------------------------------------------------------- 1. RUBANS 35 LIGNES
def rubans_complet(rangs):
    L, H = 520, 520
    x0, x1 = 118, L - 118                 # colonnes extrêmes
    y0, pas = 60, 12.4                    # rang 1 à y0, puis +pas par rang
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    Y = lambda r: y0 + (r - 1) * pas

    grille = [f'<line x1="{x:.1f}" y1="{Y(1)-6:.1f}" x2="{x:.1f}" y2="{Y(35)+6:.1f}" '
              f'stroke="{ENCRE_2}" stroke-width="0.4" stroke-dasharray="1 2"/>' for x in xs]
    ctx, acc, lib = [], [], []
    for partie, r in rangs.iterrows():
        ys = [Y(r[c]) for c in CRIT]
        if partie in ACCENTS:
            col = ACCENTS[partie]
            acc.append(ruban(xs, ys, FOND, 5.5))                 # liseré pour détacher
            acc.append(ruban(xs, ys, col, 3.2, ident(partie)))
            for x, y in zip(xs, ys):
                acc.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{col}" stroke="{FOND}" stroke-width="0.8"/>')
        else:
            ctx.append(ruban(xs, ys, GRIS_CTX, 1.6, ident(partie)))
        g = partie in ACCENTS
        c = ENCRE if g else ENCRE_2
        lib.append(texte(x0 - 8, ys[0] + 2.4, partie, 7, "end", c, g))
        lib.append(texte(x1 + 8, ys[-1] + 2.4, partie, 7, "start", c, g))

    # rangs repères
    reperes = [texte(x0 - 104, Y(r) + 2.4, r, 6, "start", ENCRE_2) for r in (1, 5, 10, 15, 20, 25, 30, 35)]
    contenu = "\n".join([
        f'<g id="grille">{"".join(grille)}</g>',
        f'<g id="entetes">{entetes(xs, 22)}</g>',
        f'<g id="rubans-contexte">{"".join(ctx)}</g>',
        f'<g id="rubans-accent">{"".join(acc)}</g>',
        f'<g id="libelles">{"".join(lib)}</g>',
        f'<g id="reperes-rangs">{"".join(reperes)}</g>',
        texte(x0 - 104, Y(35) + 22, "Rang 1 = la partie jugée la plus précieuse. 282 Américains, ~40 par critère.", 6, "start", ENCRE_2),
    ])
    (OUT / "01_rubans_35_parties.svg").write_text(svg(L, H, contenu, "Rubans — 35 parties, 4 mises en avant"), encoding="utf-8")


# ---------------------------------------------------------------- 2. PETITS MULTIPLES
def petits_multiples(rangs):
    L, H = 520, 640
    pw, ph = 250, 290                         # taille d'un panneau
    origines = [(10, 30), (260, 30), (10, 340), (260, 340)]
    blocs = []
    for (ox, oy), grp in zip(origines, GROUPES):
        x0, x1 = ox + 72, ox + pw - 72
        xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
        y0, pas = oy + 48, 6.6
        Y = lambda r: y0 + (r - 1) * pas
        membres = rangs[rangs.groupe == grp]
        autres = rangs[rangs.groupe != grp]
        accent = [p for p in membres.index if p in ACCENTS]

        g = [f'<g id="panneau-{ident(grp)}">',
             texte(ox + 8, oy + 10, grp.upper(), 8.5, "start", ENCRE, True)]
        for x in xs:
            g.append(f'<line x1="{x:.1f}" y1="{Y(1)-4:.1f}" x2="{x:.1f}" y2="{Y(35)+4:.1f}" stroke="{ENCRE_2}" stroke-width="0.3" stroke-dasharray="1 2"/>')
        for x, mot in zip(xs, CRIT_COURT):                     # en-têtes courts
            g.append(texte(x, oy + 30, mot, 5.2, "middle", ENCRE_2))
        g.append('<g id="contexte">')
        for p, r in autres.iterrows():
            g.append(ruban(xs, [Y(r[c]) for c in CRIT], GRIS_CTX, 0.6))
        g.append('</g><g id="region">')
        for p, r in membres.iterrows():
            if p not in ACCENTS:
                g.append(ruban(xs, [Y(r[c]) for c in CRIT], GRIS_GRP, 1.3, ident(p)))
        g.append('</g><g id="accent">')
        for p in accent:
            r = membres.loc[p]
            ys = [Y(r[c]) for c in CRIT]
            g.append(ruban(xs, ys, FOND, 4.2))
            g.append(ruban(xs, ys, ACCENTS[p], 2.6, ident(p)))
            for x, y in zip(xs, ys):
                g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{ACCENTS[p]}" stroke="{FOND}" stroke-width="0.6"/>')
                g.append(texte(x, y - 3.8, int(r[CRIT[xs.index(x)]]), 5, "middle", ENCRE, True))
        g.append('</g><g id="libelles">')
        for p, r in membres.iterrows():
            a = p in ACCENTS
            c = ENCRE if a else ENCRE_2
            g.append(texte(x0 - 5, Y(r[CRIT[0]]) + 1.9, p, 5.6, "end", c, a))
            g.append(texte(x1 + 5, Y(r[CRIT[-1]]) + 1.9, p, 5.6, "start", c, a))
        g.append('</g></g>')
        blocs.append("\n".join(g))
    blocs.append(texte(18, H - 12, "Chaque panneau : la même échelle de rangs 1 → 35 (haut = plus précieux). "
                       "Gris clair = les parties des autres régions.", 6, "start", ENCRE_2))
    (OUT / "02_petits_multiples_4_regions.svg").write_text(
        svg(L, H, "\n".join(blocs), "Petits multiples par région du corps"), encoding="utf-8")


# ---------------------------------------------------------------- 3. HEATMAP
def heatmap(rangs):
    cw, ch = 62, 12                       # cellule
    x0, y = 140, 40
    L = x0 + 5 * cw + 20
    lignes = []
    for grp in GROUPES:
        m = rangs[rangs.groupe == grp].sort_values(CRIT[0])
        lignes.append(("titre", grp))
        lignes += [("partie", p) for p in m.index]
    H = y + len(lignes) * ch + 4 * 6 + 40
    cells, lib = [], []
    xs = [x0 + i * cw + cw / 2 for i in range(5)]
    for kind, nom in lignes:
        if kind == "titre":
            y += 6
            lib.append(texte(12, y + 9, nom.upper(), 7, "start", ENCRE, True))
            y += ch
            continue
        r = rangs.loc[nom]
        a = nom in ACCENTS
        lib.append(texte(x0 - 6, y + 8.4, nom, 7, "end", ENCRE if a else ENCRE_2, a))
        if a:
            lib.append(f'<circle cx="{x0 - 8 - len(nom) * 3.6 - 6:.1f}" cy="{y + 6:.1f}" r="2.4" fill="{ACCENTS[nom]}"/>')
        for i, c in enumerate(CRIT):
            k = int(r[c])
            idx = min(int((k - 1) / 35 * len(SEQ)), len(SEQ) - 1)
            fill = SEQ[idx]
            cells.append(f'<rect x="{x0 + i * cw + 1:.1f}" y="{y + 1:.1f}" width="{cw - 2}" height="{ch - 2}" rx="1.5" fill="{fill}"/>')
            tc = "#ffffff" if idx <= 2 else ENCRE
            cells.append(texte(xs[i], y + 8.6, k, 6.5, "middle", tc, a))
        y += ch
    leg = [texte(x0, H - 22, "Rang :", 6, "start", ENCRE_2)]
    for i, c in enumerate(SEQ):
        leg.append(f'<rect x="{x0 + 26 + i * 22}" y="{H - 29}" width="20" height="8" fill="{c}"/>')
    leg.append(texte(x0 + 26, H - 12, "1 (précieux)", 5.5, "start", ENCRE_2))
    leg.append(texte(x0 + 26 + 7 * 22 - 2, H - 12, "35", 5.5, "end", ENCRE_2))
    contenu = "\n".join([f'<g id="entetes">{entetes(xs, 22, 6.5)}</g>',
                         f'<g id="cellules">{"".join(cells)}</g>',
                         f'<g id="libelles">{"".join(lib)}</g>',
                         f'<g id="legende">{"".join(leg)}</g>'])
    (OUT / "03_heatmap_rangs.svg").write_text(svg(L, H, contenu, "Heatmap des rangs"), encoding="utf-8")


# ---------------------------------------------------------------- 4. HOMMES / FEMMES
def hommes_femmes():
    s = pd.read_excel(RES, sheet_name="hommes_femmes", index_col=0)
    s["moy"] = (s.rang_moyen_hommes + s.rang_moyen_femmes) / 2
    s = s.sort_values("moy")
    H_COL, F_COL = "#2a78d6", "#eb6834"
    x0, x1, y0, pas = 120, 480, 50, 12
    X = lambda r: x0 + (r - 1) / 34 * (x1 - x0)
    L, H = 510, y0 + len(s) * pas + 40
    g = []
    for r in (1, 5, 10, 15, 20, 25, 30, 35):
        g.append(f'<line x1="{X(r):.1f}" y1="{y0-8}" x2="{X(r):.1f}" y2="{y0 + len(s)*pas - 4}" stroke="{ENCRE_2}" stroke-width="0.3" stroke-dasharray="1 2"/>')
        g.append(texte(X(r), y0 - 12, r, 6, "middle", ENCRE_2))
    pts = []
    for i, (p, r) in enumerate(s.iterrows()):
        y = y0 + i * pas
        fort = abs(r.ecart_H_moins_F) >= 2.5
        pts.append(texte(x0 - 8, y + 2.4, p, 6.5, "end", ENCRE if fort else ENCRE_2, fort))
        pts.append(f'<line x1="{X(r.rang_moyen_hommes):.1f}" y1="{y}" x2="{X(r.rang_moyen_femmes):.1f}" y2="{y}" stroke="{GRIS_GRP}" stroke-width="1.2"/>')
        pts.append(f'<circle cx="{X(r.rang_moyen_hommes):.1f}" cy="{y}" r="2.8" fill="{H_COL}"/>')
        pts.append(f'<circle cx="{X(r.rang_moyen_femmes):.1f}" cy="{y}" r="2.8" fill="{F_COL}"/>')
    leg = [f'<circle cx="{x0}" cy="16" r="3" fill="{H_COL}"/>', texte(x0 + 6, 18.4, "Hommes (n≈19/critère)", 7),
           f'<circle cx="{x0 + 110}" cy="16" r="3" fill="{F_COL}"/>', texte(x0 + 116, 18.4, "Femmes (n≈22/critère)", 7),
           texte(x0 + 230, 18.4, "Rang moyen sur les 5 critères (1 = plus précieux)", 6, "start", ENCRE_2)]
    contenu = "\n".join([f'<g id="grille">{"".join(g)}</g>', f'<g id="points">{"".join(pts)}</g>',
                         f'<g id="legende">{"".join(leg)}</g>',
                         texte(x0, H - 14, "En gras : écart ≥ 2,5 rangs. Petits effectifs : ces écarts sont indicatifs, pas significatifs.", 6, "start", ENCRE_2)])
    (OUT / "04_hommes_femmes.svg").write_text(svg(L, H, contenu, "Hommes / femmes"), encoding="utf-8")


# ---------------------------------------------------------------- 5. STABILITÉ
def stabilite(rangs):
    b = pd.read_excel(RES, sheet_name="stabilite_rangs")
    L, H = 520, 250
    pw = 125
    blocs = []
    for k, (p, col) in enumerate(ACCENTS.items()):
        ox = 10 + k * (pw + 2)
        x0, x1 = ox + 18, ox + pw - 20
        xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
        y0, pas = 50, 5.2
        Y = lambda r: y0 + (r - 1) * pas
        g = [f'<g id="stabilite-{ident(p)}">', texte(ox + 4, 16, p, 7.5, "start", ENCRE, True)]
        for r in (1, 10, 20, 30):
            g.append(f'<line x1="{x0-4}" y1="{Y(r):.1f}" x2="{x1+4}" y2="{Y(r):.1f}" stroke="{GRIS_CTX}" stroke-width="0.4"/>')
            if k == 0:
                g.append(texte(ox + 2, Y(r) + 2, r, 5, "start", ENCRE_2))
        bp = b[b.partie == p].set_index("critere")
        for x, c in zip(xs, CRIT):
            lo, hi = bp.loc[c, "rang_bas_2.5%"], bp.loc[c, "rang_haut_97.5%"]
            g.append(f'<rect x="{x-3:.1f}" y="{Y(lo):.1f}" width="6" height="{max(Y(hi)-Y(lo),1):.1f}" rx="3" fill="{col}" opacity="0.25"/>')
        ys = [Y(rangs.loc[p, c]) for c in CRIT]
        g.append(ruban(xs, ys, col, 1.6))
        for x, y in zip(xs, ys):
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{col}"/>')
        for x, (l1, _) in zip(xs, CRIT_2L):
            g.append(texte(x, 34, CRIT_COURT[xs.index(x)], 4.6, "middle", ENCRE_2))
        g.append("</g>")
        blocs.append("\n".join(g))
    blocs.append(texte(12, H - 12, "Bande claire = intervalle à 95 % du rang (bootstrap, 2000 tirages). "
                       "Bande longue = rang peu fiable : ne pas bâtir une annotation dessus.", 6, "start", ENCRE_2))
    (OUT / "05_stabilite_rangs.svg").write_text(svg(L, H, "\n".join(blocs), "Stabilité des rangs"), encoding="utf-8")


def main():
    rangs = lire()
    rubans_complet(rangs)
    petits_multiples(rangs)
    heatmap(rangs)
    hommes_femmes()
    stabilite(rangs)
    print("SVG écrits dans", OUT)


if __name__ == "__main__":
    main()
