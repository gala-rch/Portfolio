"""
Maquette A4 de la page magazine (SVG, 1 unité = 1 pt, 595 × 842 = A4).
À lancer après analyse.py :  python3 maquette.py  → maquette/maquette_A4.svg

Polices : Barlow Condensed + Source Serif 4 (Google Fonts, gratuites).
Installe-les sur ton ordi pour qu'Illustrator les affiche.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd

import pictos

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
PICTO = "#BDB3A2"            # gris des pictogrammes, discret

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
         "Notre gratitude envers qui nous la rend est immense (1re), alors qu'on n'imaginait pas si dur de s'en passer (7e)."),
    ],
    "Bras & mains": [
        (2, "Les 10 doigts", 1, "On surréagit à la perte de nos 10 doigts",
         "Elle nous choque plus (3e) que celle des deux mains (6e), peut-être parce qu'elle semble forcément délibérée."),
        (3, "Pouce", 4, "On surestime notre pouce",
         "Les codes légaux, surtout le droit émirati, lui accordent moins de valeur que les non-spécialistes."),
    ],
    "Jambes & pieds": [
        (4, "Les 2 pieds", 1, "Les pieds, une perte qui révolte peu",
         "Les perdre nous met peu en colère (18e), mais on réclame pour eux un fort dédommagement (5e)."),
    ],
    "Visage, dents & intimité": [
        (5, "Parties génitales", 1, "Le grand écart des parties génitales",
         "On s'en passerait sans trop de difficulté (20e), mais leur perte révolte (8e) et appelle un gros dédommagement (8e)."),
    ],
}


# ---------------------------------------------------------------- outils
def t(x, y, s, size, font=COND, anchor="start", fill=ENCRE, weight="normal", style=""):
    # Illustrator retrouve mieux une police par son nom PostScript que par famille + graisse
    if font == COND and weight == "bold":
        font = "BarlowCondensed-Bold, " + COND
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{style}>{escape(str(s))}</text>')


def para(x, y, s, size, largeur, font=SERIF, interligne=1.3, **kw):
    """Texte sur plusieurs lignes (coupure approximative par nombre de caractères)."""
    max_car = int(largeur / (size * 0.5))
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


# ---------------------------------------------------------------- typographie
# Échelle typographique : chaque niveau ≈ 1,2 × le précédent (7 → 8 → 9,5 → 11 → 13).
# Pour tout agrandir ou réduire, ne modifier que ces valeurs.
T_MINI = 7          # noms de parties, en-têtes de colonnes, axes, folio
T_TEXTE = 8         # annotations, définitions, sources, encadré
T_INTER = 9.5       # titres d'annotation, intertitres, critères
T_CHAPO = 10.5       # chapô
T_PANNEAU = 13      # titres de panneaux
T_RUBRIQUE = 18     # « Big data »
T_TITRE = 46        # titre
INTERLIGNE = 1.3


TAILLE_PICTO = 26      # côté d'un pictogramme, en pt


def bloc_annotations(grp, x, y, w, rendu=True):
    """Annotations d'un panneau, chacune avec son pictogramme à droite ; renvoie (svg, y de fin)."""
    col, vedette = REGIONS[grp]
    g = []
    for _, partie, _, titre, texte in ANNOT[grp]:
        c = col if partie == vedette else SECONDAIRE.get(partie, col)
        n = len(pictos.PICTO_DE[partie])
        zone = TAILLE_PICTO * n + 2 * (n - 1) + 10       # largeur réservée au picto
        y0 = y
        g.append(t(x + 11, y, titre, T_INTER, COND, weight="bold"))
        p, y = para(x + 11, y + T_TEXTE * 1.45, texte, T_TEXTE, w - 11 - zone)
        g.append(p)
        haut = y0 - T_INTER * 0.8
        g.append(pictos.groupe(partie, x + w - (zone - 10) / 2, (haut + y - 2) / 2, TAILLE_PICTO, PICTO))
        g.append(f'<rect x="{x}" y="{y0 - T_INTER * 0.8:.1f}" width="2.5" height="{y - y0 + T_INTER * 0.5:.1f}" fill="{c}"/>')
        y += 7
    return "\n".join(g), y


# ---------------------------------------------------------------- blocs
def entete():
    y = M + T_RUBRIQUE * 0.8
    g = ['<g id="entete">', t(M, y, "Big data", T_RUBRIQUE, SERIF, weight="bold")]
    y += 7
    g.append(f'<line x1="{M}" y1="{y}" x2="{L - M}" y2="{y}" stroke="{ENCRE}" stroke-width="0.6"/>')
    y += T_TITRE * 0.95
    g.append(t(M, y, "Ce que vaut notre corps", T_TITRE, COND, weight="bold"))
    chapo = ("Plus d'un million de dollars pour notre motricité ou nos capacités mentales, quelques centaines pour un ongle : "
             "282 Américains ont estimé la valeur de 35 parties de leur corps selon cinq critères. Leur classement, "
             "proche de celui des codes légaux, change peu… sauf pour quelques parties.")
    p, y = para(M, y + T_CHAPO * 1.8, chapo, T_CHAPO, L - 2 * M)
    g += [p, "</g>"]
    return "\n".join(g), y


def comment_lire(y):
    h = 14 + T_INTER + 6 + T_TEXTE * 1.3 + 8
    g = ['<g id="comment-lire">',
         f'<rect x="{M}" y="{y}" width="{L - 2*M}" height="{h:.1f}" fill="#EFE4CE"/>',
         t(M + 10, y + 14, "COMMENT LIRE", T_INTER, COND, weight="bold")]
    defs = [("Difficulté", "à vivre sans elle"),
            ("Colère", "si un tiers nous la prend"),
            ("Gratitude", "envers qui nous la rend"),
            ("Prix", "sur un marché fictif"),
            ("Dédommagement", "qu'un juge devrait verser")]
    x0, w = M + 10, (L - 2 * M - 20) / 5
    yc = y + 14 + T_INTER + 6
    for i, (a, b) in enumerate(defs):
        g.append(t(x0 + i * w, yc, f"{i+1}. {a}", T_INTER, COND, weight="bold"))
        g.append(t(x0 + i * w, yc + T_TEXTE * 1.3, b, T_TEXTE, SERIF, fill=ENCRE_2))
    g.append(t(L - M - 10, y + 14, "Chaque ruban suit une partie du corps. "
               "Plus il est haut, plus elle est jugée précieuse (rang 1 à 35).",
               T_TEXTE, SERIF, "end", ENCRE_2, style=' font-style="italic"'))
    g.append("</g>")
    return "\n".join(g), y + h


def panneau(rangs, grp, ox, oy, pw, top, ch):
    """oy = haut du panneau, top = y du rang 1, ch = hauteur du rang 1 au rang 35."""
    col, vedette = REGIONS[grp]
    g = [f'<g id="panneau-{grp.split()[0].lower()}">',
         f'<rect x="{ox}" y="{oy}" width="{T_PANNEAU * 0.75:.1f}" height="{T_PANNEAU * 0.75:.1f}" fill="{col}"/>',
         t(ox + T_PANNEAU * 1.1, oy + T_PANNEAU * 0.75, grp.upper(), T_PANNEAU, COND, weight="bold")]
    a, _ = bloc_annotations(grp, ox + 2, oy + T_PANNEAU + 11, pw - 2)
    g.append(a)

    pas = ch / 34
    x0, x1 = ox + 74, ox + pw - 74
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    Y = lambda r: top + (r - 1) * pas
    for x, c in zip(xs, CRIT_COURT):
        g.append(f'<line x1="{x:.1f}" y1="{top - 5:.1f}" x2="{x:.1f}" y2="{Y(35) + 4:.1f}" stroke="{ENCRE_2}" stroke-width="0.3" stroke-dasharray="0.8 1.6"/>')
        g.append(t(x, top - 14, c, T_MINI, COND, "middle", ENCRE_2))
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
    # libellés : écartés s'ils se chevauchent, reliés à leur ruban par un filet
    occupe = {-1: [], 1: []}       # y des libellés de chaque colonne (pour placer les pictos)
    for k, xl, sens in [(CRIT[0], x0, -1), (CRIT[-1], x1, 1)]:
        vrais = {p: Y(r[k]) for p, r in membres.iterrows()}
        for p, y in ecarter(list(vrais.items()), T_MINI * 1.08):
            occupe[sens].append(y)
            fort = p == vedette or p in SECONDAIRE
            c, w = (ENCRE, "bold") if fort else (ENCRE_2, "normal")
            if abs(y - vrais[p]) > 0.8:
                g.append(f'<polyline points="{xl + sens * 1.5:.1f},{vrais[p]:.1f} {xl + sens * 4:.1f},{vrais[p]:.1f} {xl + sens * 7:.1f},{y:.1f}" '
                         f'fill="none" stroke="{GRIS_GRP}" stroke-width="0.3"/>')
            g.append(t(xl + sens * 9, y + T_MINI * 0.35, p, T_MINI, COND, "end" if sens < 0 else "start", c, w))
    # rang écrit au-dessus de chaque point du ruban coloré
    for x, k in zip(xs, CRIT):
        r = int(membres.loc[vedette, k])
        g.append(f'<circle cx="{x:.1f}" cy="{Y(r):.1f}" r="2.6" fill="{col}" stroke="{FOND}" stroke-width="0.7"/>')
        g.append(t(x, Y(r) - 4.8, r, T_MINI + 0.5, COND, "middle", ENCRE, "bold"))
    g.append("</g>")
    return "\n".join(g)


def hommes_femmes(x, y, w):
    s = pd.read_excel(RES, sheet_name="hommes_femmes", index_col=0)
    lignes = ["Capacités mentales", "Motricité globale", "Visage", "Pouce"]
    g = ['<g id="hommes-femmes">', t(x, y, "HOMMES ET FEMMES", T_INTER, COND, weight="bold")]
    p, yy = para(x, y + T_TEXTE * 1.6, "Les femmes redoutent surtout paralysie, défiguration et perte des capacités "
                 "mentales ; les hommes tiennent plus à leur pouce.", T_TEXTE, w)
    g.append(p)
    gx0, gx1 = x + 78, x + w - 6
    X = lambda r: gx0 + (r - 1) / 19 * (gx1 - gx0)
    yy += 2
    for r in (1, 5, 10, 15, 20):
        g.append(t(X(r), yy, r, T_MINI, COND, "middle", ENCRE_2))
    pas = 9
    for i, nom in enumerate(lignes):
        ly = yy + 9 + i * pas
        h, f = s.loc[nom, "rang_moyen_hommes"], s.loc[nom, "rang_moyen_femmes"]
        g.append(t(gx0 - 8, ly + 2.4, nom, T_MINI, COND, "end"))
        g.append(f'<line x1="{X(h):.1f}" y1="{ly}" x2="{X(f):.1f}" y2="{ly}" stroke="{GRIS_GRP}" stroke-width="1"/>')
        g.append(f'<circle cx="{X(h):.1f}" cy="{ly}" r="3" fill="{ENCRE}"/>')
        g.append(f'<circle cx="{X(f):.1f}" cy="{ly}" r="2.7" fill="{FOND}" stroke="{ENCRE}" stroke-width="1"/>')
    # légende sur la ligne du titre, à droite
    lx = x + w - 92
    g += [f'<circle cx="{lx}" cy="{y - 2.5}" r="3" fill="{ENCRE}"/>', t(lx + 5, y, "Hommes", T_MINI),
          f'<circle cx="{lx + 46}" cy="{y - 2.5}" r="2.7" fill="{FOND}" stroke="{ENCRE}" stroke-width="1"/>',
          t(lx + 51, y, "Femmes", T_MINI), "</g>"]
    return "\n".join(g), yy + 9 + (len(lignes) - 1) * pas + 4


def sources(x, y, w):
    g = ['<g id="sources">', t(x, y, "D'OÙ VIENNENT CES DONNÉES", T_INTER, COND, weight="bold")]
    p, yy = para(x, y + T_TEXTE * 1.6,
                 "Des chercheurs en psychologie ont demandé à 306 Américains d'estimer la valeur de parties de leur corps, "
                 "puis comparé ces estimations à cinq codes légaux médiévaux et actuels. 282 réponses retenues (critères "
                 "d'exclusion des auteurs), soit une quarantaine par critère ; classement selon la note moyenne. "
                 "Wee et al., Science Advances (2025).", T_TEXTE, w)
    g += [p, "</g>"]
    return "\n".join(g), yy


def main():
    rangs = pd.read_excel(RES, sheet_name="rangs", index_col=0)
    style = ("<style>@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700"
             "&amp;family=Source+Serif+4:ital,wght@0,400;0,700;1,400&amp;display=swap');</style>")
    gouttiere = 20
    pw = (L - 2 * M - gouttiere) / 2
    tete, y = entete()
    cl, y = comment_lire(y + 12)
    corps = [tete, cl]

    # bas de page : on le place d'abord pour savoir quelle hauteur reste aux graphiques
    folio_y = H - 16
    # encadré hommes/femmes retiré pour laisser la place aux graphiques
    # (la fonction hommes_femmes() reste disponible plus haut si besoin)
    _, fin = sources(M, 0, L - 2 * M)
    bas_h = fin + 2
    bas_y = folio_y - 12 - bas_h
    so, _ = sources(M, bas_y + T_INTER, L - 2 * M)

    # hauteur des en-têtes de panneaux (titre + annotations), par rangée
    def entete_h(grp):
        _, fin = bloc_annotations(grp, 0, T_PANNEAU + 11, pw)
        return fin
    groupes = list(REGIONS)
    rangees = [groupes[:2], groupes[2:]]
    h_tetes = [max(entete_h(g) for g in r) for r in rangees]
    haut_panneaux = y + 16
    marge_graph = 17 + 8          # en-têtes de colonnes au-dessus + respiration dessous
    ch = (bas_y - 12 - haut_panneaux - 12 - sum(h_tetes) - 2 * marge_graph) / 2
    oy = haut_panneaux
    for r, ht in zip(rangees, h_tetes):
        top = oy + ht + 17
        for i, grp in enumerate(r):
            corps.append(panneau(rangs, grp, M + i * (pw + gouttiere), oy, pw, top, ch))
        oy = top + ch + 8 + 12
    corps.append(f'<line x1="{M}" y1="{bas_y - 6}" x2="{L - M}" y2="{bas_y - 6}" stroke="{ENCRE}" stroke-width="0.4"/>')
    corps.append(so)
    corps.append(t(M, folio_y, "38  |  Pour vous abonner : epsiloon.com", T_MINI, COND, fill=ENCRE_2))
    corps.append(t(L - M, folio_y, "PAR [TON NOM], D'APRÈS LÉA DESRAYAUD", T_MINI, COND, "end", ENCRE_2))
    print(f"Hauteur d'un graphique : {ch:.0f} pt, soit {ch / 34:.1f} pt entre deux rangs")
    svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
           f'width="{L}pt" height="{H}pt" viewBox="0 0 {L} {H}">\n{style}\n'
           f'<g id="fond"><rect width="{L}" height="{H}" fill="{FOND}"/></g>\n' + "\n".join(corps) + "\n</svg>\n")
    (OUT / "maquette_A4.svg").write_text(svg, encoding="utf-8")
    print("Maquette écrite :", OUT / "maquette_A4.svg")


if __name__ == "__main__":
    main()
