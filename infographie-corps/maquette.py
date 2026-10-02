"""
Maquette A4 de la page magazine (SVG, 1 unité = 1 pt, 595 × 842 = A4).
À lancer après analyse.py :  python3 maquette.py  → maquette/maquette_A4.svg

Polices : Barlow Condensed + Source Serif 4 (Google Fonts, gratuites).
Installe-les sur ton ordi pour qu'Illustrator les affiche.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd

ICI = Path(__file__).parent
RES = ICI / "sorties" / "resultats_USA.xlsx"
OUT = ICI / "maquette"
OUT.mkdir(exist_ok=True)

L, H = 595, 842
M = 34                                   # marge 12 mm
COND = "'Barlow Condensed', 'Arial Narrow', sans-serif"
SERIF = "'Source Serif 4', Georgia, serif"
FOND, ENCRE, ENCRE_2 = "#F7EFDF", "#1E1B18", "#6E665A"
GRIS_CTX, GRIS_GRP = "#E3D9C6", "#A39A8A"

# Région → (couleur, partie vedette)
REGIONS = {
    "Fonctions & sens":         ("#CC3D2A", "Parole et mastication"),
    "Bras & mains":             ("#1A7BB0", "Les 10 doigts"),
    "Jambes & pieds":           ("#D99200", "Les 2 pieds"),
    "Visage, dents & intimité": ("#7D3FA0", "Parties génitales"),
}
SECONDAIRE = {"Pouce": "#4E473E"}        # partie annotée sans couleur vive
CRIT = ["Difficulté à s'en passer", "Colère si on en perd l'usage",
        "Gratitude si on en retrouve l'usage", "Prix sur le marché", "Dédommagement à verser"]
CRIT_COURT = ["Difficulté", "Colère", "Gratitude", "Prix", "Dédommag."]

# Annotations : (numéro, partie, colonne où poser le repère, titre, texte)
ANNOT = {
    "Fonctions & sens": [
        (1, "Parole et mastication", 2, "C'est après coup que l'on accorde du prix à notre bouche",
         "Notre gratitude envers qui nous en rend l'usage est immense (1re place), alors qu'on n'imaginait pas, a priori, si difficile de s'en passer (7e)."),
    ],
    "Bras & mains": [
        (2, "Les 10 doigts", 1, "On surréagit à la perte de nos 10 doigts",
         "Elle nous choque plus (3e) que celle des deux mains (6e). Peut-être parce qu'elle semble forcément causée par une action délibérée."),
        (3, "Pouce", 4, "On surestime notre pouce",
         "Les codes légaux, en particulier le droit émirati, lui accordent une valeur moindre que celle estimée par des non-spécialistes."),
    ],
    "Jambes & pieds": [
        (4, "Les 2 pieds", 1, "Les pieds, une perte qui révolte peu",
         "Les perdre nous met peu en colère (18e), mais on réclame pour eux un fort dédommagement (5e)."),
    ],
    "Visage, dents & intimité": [
        (5, "Parties génitales", 1, "Le grand écart des parties génitales",
         "On s'en passerait sans trop de difficulté (20e), mais leur perte nous révolte (8e) et appelle un gros dédommagement (8e)."),
    ],
}


# ---------------------------------------------------------------- outils
def t(x, y, s, size, font=COND, anchor="start", fill=ENCRE, weight="normal", style=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{style}>{escape(str(s))}</text>')


def para(x, y, s, size, largeur, font=SERIF, interligne=1.3, **kw):
    """Texte sur plusieurs lignes (coupure approximative par nombre de caractères)."""
    max_car = int(largeur / (size * 0.47))
    lignes, cur = [], ""
    for mot in s.split():
        if len(cur) + len(mot) + 1 > max_car and cur:
            lignes.append(cur)
            cur = mot
        else:
            cur = f"{cur} {mot}".strip()
    lignes.append(cur)
    out = [t(x, y + i * size * interligne, l, size, font, **kw) for i, l in enumerate(lignes)]
    return "\n".join(out), y + len(lignes) * size * interligne


def ruban(xs, ys, col, ep):
    d = f"M{xs[0]:.1f},{ys[0]:.1f}"
    for i in range(1, len(xs)):
        xm = (xs[i - 1] + xs[i]) / 2
        d += f" C{xm:.1f},{ys[i-1]:.1f} {xm:.1f},{ys[i]:.1f} {xs[i]:.1f},{ys[i]:.1f}"
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{ep}" stroke-linecap="round"/>'


def ecarter(items, ecart):
    """Décale vers le bas les libellés trop proches (items = [(nom, y)])."""
    items = sorted(items, key=lambda i: i[1])
    out, dernier = [], -1e9
    for nom, y in items:
        y = max(y, dernier + ecart)
        out.append((nom, y))
        dernier = y
    return out


def pastille(x, y, n, col):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}" stroke="{FOND}" stroke-width="1"/>'
            + t(x, y + 2.3, n, 6.5, COND, "middle", "#FFFFFF", "bold"))


# ---------------------------------------------------------------- blocs
def entete():
    g = ['<g id="entete">',
         t(M, M + 14, "Big data", 20, SERIF, weight="bold"),
         f'<line x1="{M}" y1="{M + 22}" x2="{L - M}" y2="{M + 22}" stroke="{ENCRE}" stroke-width="0.6"/>',
         t(M, M + 72, "Ce que vaut notre corps", 52, COND, weight="bold"),
         ]
    chapo = ("Plus d'un million de dollars pour notre motricité ou nos capacités mentales, quelques centaines pour un ongle : "
             "282 Américains ont estimé la valeur de 35 parties de leur corps selon cinq critères. "
             "Leur classement, proche de celui des codes légaux, est presque toujours le même… sauf pour quelques parties qui font le grand écart.")
    p, _ = para(M, M + 98, chapo, 9.5, L - 2 * M - 10)
    g += [p, "</g>"]
    return "\n".join(g)


def comment_lire(y):
    g = ['<g id="comment-lire">',
         f'<rect x="{M}" y="{y}" width="{L - 2*M}" height="58" fill="#EFE4CE"/>',
         t(M + 10, y + 15, "COMMENT LIRE", 8.5, COND, weight="bold")]
    defs = [("Difficulté", "à vivre sans cette partie"),
            ("Colère", "si un tiers nous la fait perdre"),
            ("Gratitude", "envers qui nous la rend"),
            ("Prix", "sur un marché fictif"),
            ("Dédommagement", "qu'un juge devrait accorder")]
    x0, w = M + 10, (L - 2 * M - 20) / 5
    for i, (a, b) in enumerate(defs):
        g.append(t(x0 + i * w, y + 31, f"{i+1}. {a}", 8, COND, weight="bold"))
        g.append(t(x0 + i * w, y + 41, b, 7, SERIF, fill=ENCRE_2))
    g.append(t(M + 10, y + 53, "Chaque ruban suit une partie du corps d'un critère à l'autre. Plus il est haut, plus la partie est jugée précieuse (rang 1 à 35).",
               7, SERIF, fill=ENCRE_2, style=' font-style="italic"'))
    g.append("</g>")
    return "\n".join(g)


def panneau(rangs, grp, ox, oy, pw, ph):
    col, vedette = REGIONS[grp]
    g = [f'<g id="panneau-{grp.split()[0].lower()}">',
         f'<rect x="{ox}" y="{oy + 3}" width="9" height="9" fill="{col}"/>',
         t(ox + 14, oy + 11.5, grp.upper(), 11, COND, weight="bold")]

    # annotations en tête de panneau
    y = oy + 24
    for n, partie, _, titre, texte in ANNOT[grp]:
        c = col if partie == vedette else SECONDAIRE.get(partie, col)
        g.append(pastille(ox + 5, y - 2.5, n, c))
        g.append(t(ox + 14, y, titre, 8, COND, weight="bold"))
        p, y = para(ox + 14, y + 9, texte, 6.8, pw - 18)
        g.append(p)
        y += 4

    # graphique
    top = oy + 96
    pas = (oy + ph - top - 14) / 34
    x0, x1 = ox + 66, ox + pw - 66
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    Y = lambda r: top + (r - 1) * pas
    for x, c in zip(xs, CRIT_COURT):
        g.append(f'<line x1="{x:.1f}" y1="{top - 4:.1f}" x2="{x:.1f}" y2="{Y(35) + 4:.1f}" stroke="{ENCRE_2}" stroke-width="0.3" stroke-dasharray="0.8 1.6"/>')
        g.append(t(x, top - 8, c, 6.5, COND, "middle", ENCRE_2))
    membres = rangs[rangs.groupe == grp]
    for p, r in rangs[rangs.groupe != grp].iterrows():
        g.append(ruban(xs, [Y(r[c]) for c in CRIT], GRIS_CTX, 0.8))
    for p, r in membres.iterrows():
        if p != vedette and p not in SECONDAIRE:
            g.append(ruban(xs, [Y(r[c]) for c in CRIT], GRIS_GRP, 1.2))
    for p, c, ep in [(s, SECONDAIRE[s], 1.6) for s in SECONDAIRE if s in membres.index] + [(vedette, col, 3)]:
        ys = [Y(membres.loc[p, k]) for k in CRIT]
        g.append(ruban(xs, ys, FOND, ep + 2))
        g.append(ruban(xs, ys, c, ep))
    # libellés (écartés s'ils se chevauchent)
    for k, x, anc in [(CRIT[0], x0 - 5, "end"), (CRIT[-1], x1 + 5, "start")]:
        for p, y in ecarter([(p, Y(r[k])) for p, r in membres.iterrows()], 5.4):
            fort = p == vedette or p in SECONDAIRE
            c, w = (ENCRE, "bold") if fort else (ENCRE_2, "normal")
            g.append(t(x, y + 2, p, 5.8, COND, anc, c, w))
    # repères numérotés posés sur les rubans
    for n, partie, k, _, _ in ANNOT[grp]:
        c = col if partie == vedette else SECONDAIRE.get(partie, col)
        g.append(pastille(xs[k], Y(membres.loc[partie, CRIT[k]]), n, c))
    g.append("</g>")
    return "\n".join(g)


def hommes_femmes(x, y, w):
    s = pd.read_excel(RES, sheet_name="hommes_femmes", index_col=0)
    lignes = ["Capacités mentales", "Motricité globale", "Visage", "Pouce"]
    g = ['<g id="hommes-femmes">',
         t(x, y, "HOMMES ET FEMMES", 8.5, COND, weight="bold")]
    p, yy = para(x, y + 10, "Les femmes craignent particulièrement d'être paralysées, défigurées ou de perdre leurs capacités mentales ; les hommes tiennent plus à leur pouce.", 6.8, w)
    g.append(p)
    gx0, gx1 = x + 70, x + w - 6
    X = lambda r: gx0 + (r - 1) / 19 * (gx1 - gx0)
    yy += 4
    for r in (1, 5, 10, 15, 20):
        g.append(t(X(r), yy, r, 5.5, COND, "middle", ENCRE_2))
    for i, nom in enumerate(lignes):
        ly = yy + 10 + i * 10
        h, f = s.loc[nom, "rang_moyen_hommes"], s.loc[nom, "rang_moyen_femmes"]
        g.append(t(gx0 - 6, ly + 2, nom, 6.5, COND, "end"))
        g.append(f'<line x1="{X(h):.1f}" y1="{ly}" x2="{X(f):.1f}" y2="{ly}" stroke="{GRIS_GRP}" stroke-width="1"/>')
        g.append(f'<circle cx="{X(h):.1f}" cy="{ly}" r="2.8" fill="{ENCRE}"/>')
        g.append(f'<circle cx="{X(f):.1f}" cy="{ly}" r="2.6" fill="{FOND}" stroke="{ENCRE}" stroke-width="1"/>')
    ly = yy + 10 + len(lignes) * 10
    g += [f'<circle cx="{gx0}" cy="{ly}" r="2.8" fill="{ENCRE}"/>', t(gx0 + 5, ly + 2, "Hommes", 6.5),
          f'<circle cx="{gx0 + 42}" cy="{ly}" r="2.6" fill="{FOND}" stroke="{ENCRE}" stroke-width="1"/>', t(gx0 + 47, ly + 2, "Femmes", 6.5),
          t(gx1, ly + 2, "rang moyen (1 = le plus précieux)", 5.5, COND, "end", ENCRE_2), "</g>"]
    return "\n".join(g)


def sources(x, y, w):
    g = ['<g id="sources">', t(x, y, "D'OÙ VIENNENT CES DONNÉES", 8.5, COND, weight="bold")]
    p, _ = para(x, y + 10,
                "Des chercheurs en psychologie ont demandé à 306 Américains d'estimer la valeur de parties de leur corps, "
                "puis ont comparé ces estimations avec cinq codes légaux médiévaux et actuels. 282 réponses retenues après "
                "les critères d'exclusion des auteurs ; chaque critère a été noté par une quarantaine de personnes. "
                "Le classement repose sur la note moyenne. Wee et al., Science Advances (2025).", 6.8, w)
    g += [p, "</g>"]
    return "\n".join(g)


def main():
    rangs = pd.read_excel(RES, sheet_name="rangs", index_col=0)
    style = ("<style>@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700"
             "&amp;family=Source+Serif+4:ital,wght@0,400;0,700;1,400&amp;display=swap');</style>")
    corps = [entete(), comment_lire(176)]
    pw, ph, gap = (L - 2 * M - 18) / 2, 232, 8
    for i, grp in enumerate(REGIONS):
        ox = M + (i % 2) * (pw + 18)
        oy = 246 + (i // 2) * (ph + gap)
        corps.append(panneau(rangs, grp, ox, oy, pw, ph))
    yb = 246 + 2 * ph + gap + 12
    corps.append(f'<line x1="{M}" y1="{yb - 8}" x2="{L - M}" y2="{yb - 8}" stroke="{ENCRE}" stroke-width="0.4"/>')
    corps.append(hommes_femmes(M, yb + 4, pw))
    corps.append(sources(M + pw + 18, yb + 4, pw))
    corps.append(t(M, H - 14, "38  |  Pour vous abonner : epsiloon.com", 7, COND, fill=ENCRE_2))
    corps.append(t(L - M, H - 14, "PAR [TON NOM], D'APRÈS LÉA DESRAYAUD", 7, COND, "end", ENCRE_2))
    svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
           f'width="{L}pt" height="{H}pt" viewBox="0 0 {L} {H}">\n{style}\n'
           f'<g id="fond"><rect width="{L}" height="{H}" fill="{FOND}"/></g>\n' + "\n".join(corps) + "\n</svg>\n")
    (OUT / "maquette_A4.svg").write_text(svg, encoding="utf-8")
    print("Maquette écrite :", OUT / "maquette_A4.svg")


if __name__ == "__main__":
    main()
