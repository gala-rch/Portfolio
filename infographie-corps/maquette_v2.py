"""
Variante de la maquette : annotations À CÔTÉ du graphique (comme l'affiche d'origine),
reliées au ruban par un trait. Libère la place prise par les annotations au-dessus
des graphiques, qui deviennent plus hauts.

Reprend les choix faits dans Illustrator : pas de libellés à droite, pouce en gris,
pas de pictogrammes, couleurs relevées sur le fichier de travail.

À lancer après analyse.py :  python3 maquette_v2.py  → maquette/maquette_A4_v2.svg
"""

import pandas as pd

import maquette as m
from maquette import (CRIT, CRIT_COURT, COND, ENCRE, ENCRE_2, FOND, GRIS_CTX, GRIS_GRP, H, L, M,
                      SEMI, SERIF, T_INTER, T_MINI, T_PANNEAU, T_TEXTE, comment_lire, ecarter,
                      entete, para, ruban, sources, t)

# Couleurs du fichier Illustrator (relevées sur la capture)
COULEURS = {
    "Fonctions & sens": "#A15E77",
    "Bras & mains": "#5C79A4",
    "Jambes & pieds": "#B9934A",
    "Visage, dents & intimité": "#646444",
}
LARG_LIBELLES = 80        # colonne des noms à gauche (noms en 8 pt)
T_LIB = 8                 # taille des noms des parties
LARG_ANNOT = 74           # colonne des annotations à droite
ECART = 10                # entre le graphique et l'annotation


def panneau(rangs, grp, ox, oy, pw, top, ch):
    col = COULEURS[grp]
    _, vedette = m.REGIONS[grp]
    annot = [a for a in m.ANNOT[grp] if a[1] == vedette][0]   # le pouce est retiré
    _, partie, k, titre, texte = annot

    g = [f'<g id="panneau-{grp.split()[0].lower()}">',
         f'<rect x="{ox}" y="{oy}" width="{T_PANNEAU * 0.75:.1f}" height="{T_PANNEAU * 0.75:.1f}" fill="{col}"/>',
         t(ox + T_PANNEAU * 1.1, oy + T_PANNEAU * 0.75, grp.upper(), T_PANNEAU, COND, weight="bold")]

    x0 = ox + LARG_LIBELLES
    x1 = ox + pw - LARG_ANNOT - ECART
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    pas = ch / 34
    Y = lambda r: top + (r - 1) * pas

    g.append(f'<g id="graphique-{grp.split()[0].lower()}">')
    for x, c in zip(xs, ["Difficulté", "Colère", "Gratitude", "Prix", "Dédomm."]):
        g.append(f'<line x1="{x:.1f}" y1="{top - 5:.1f}" x2="{x:.1f}" y2="{Y(35) + 4:.1f}" stroke="{ENCRE_2}" stroke-width="0.3" stroke-dasharray="0.8 1.6"/>')
        g.append(t(x, top - 14, c, T_MINI, COND, "middle", ENCRE_2))   # condensé : 5 mots courts dans une colonne étroite
    membres = rangs[rangs.groupe == grp]
    for _, r in rangs[rangs.groupe != grp].iterrows():
        g.append(ruban(xs, [Y(r[c]) for c in CRIT], GRIS_CTX, 0.8))
    for p, r in membres.iterrows():
        if p != vedette:
            g.append(ruban(xs, [Y(r[c]) for c in CRIT], GRIS_GRP, 1.2))
    ys = [Y(membres.loc[vedette, c]) for c in CRIT]
    g.append(ruban(xs, ys, FOND, 5.2))
    g.append(ruban(xs, ys, col, 3.2))
    # noms à gauche seulement
    vrais = {p: Y(r[CRIT[0]]) for p, r in membres.iterrows()}
    for p, y in ecarter(list(vrais.items()), T_LIB * 1.12):
        fort = p == vedette
        c, w = (ENCRE, "bold") if fort else (ENCRE_2, "normal")
        if abs(y - vrais[p]) > 0.8:
            g.append(f'<polyline points="{x0 - 1.5:.1f},{vrais[p]:.1f} {x0 - 4:.1f},{vrais[p]:.1f} {x0 - 7:.1f},{y:.1f}" '
                     f'fill="none" stroke="{GRIS_GRP}" stroke-width="0.3"/>')
        g.append(t(x0 - 9, y + T_LIB * 0.35, p, T_LIB, SEMI, "end", c, w))
    for x, kk in zip(xs, CRIT):
        r = int(membres.loc[vedette, kk])
        g.append(f'<circle cx="{x:.1f}" cy="{Y(r):.1f}" r="2.8" fill="{col}" stroke="{FOND}" stroke-width="0.7"/>')
        g.append(t(x, Y(r) - 5.5, r, T_LIB + 0.5, SEMI, "middle", ENCRE, "bold"))
    g.append("</g>")

    # annotation à droite, alignée sur le point qu'elle commente, reliée par un trait
    xa = ox + pw - LARG_ANNOT
    cible_x, cible_y = xs[k], Y(membres.loc[vedette, CRIT[k]])
    ya = min(max(cible_y - 4, top), top + ch - 90)        # reste dans la hauteur du graphique
    ga = [f'<g id="annotation-{grp.split()[0].lower()}">']
    pt, y = para(xa, ya, titre, T_INTER, LARG_ANNOT, COND, interligne=1.1, weight="bold")
    ga.append(pt)
    pt, y = para(xa, y + 3, texte, T_TEXTE, LARG_ANNOT)
    ga.append(pt)
    # trait : du bord gauche de l'annotation jusqu'au point, + petit point noir au bout
    ga.append(f'<polyline points="{xa - 3:.1f},{ya - 3:.1f} {cible_x + 6:.1f},{ya - 3:.1f} {cible_x:.1f},{cible_y:.1f}" '
              f'fill="none" stroke="{ENCRE}" stroke-width="0.5"/>')
    ga.append(f'<circle cx="{cible_x:.1f}" cy="{cible_y:.1f}" r="1.3" fill="{ENCRE}"/>')
    ga.append("</g>")
    g += ga
    g.append("</g>")
    return "\n".join(g)


def entete_v2():
    """En-tête sans bandeau : la règle de lecture passe à la fin du chapô."""
    from maquette import T_RUBRIQUE, T_TITRE, T_CHAPO
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
    g.append(p)
    g.append(t(M, y + 2, "Chaque ruban suit une partie du corps d'un critère à l'autre : plus il est haut, plus elle est jugée précieuse (rang 1 à 35).",
               T_TEXTE, SERIF, fill=ENCRE_2, style=' font-style="italic"'))
    g.append("</g>")
    return "\n".join(g), y + 2


def comment_lire_bas(x, y, w):
    """Les 5 critères, une ligne chacun, en bas de page."""
    defs = [("Difficulté", "à vivre sans cette partie"),
            ("Colère", "si un tiers nous la fait perdre"),
            ("Gratitude", "envers qui nous la rend"),
            ("Prix", "sur un marché fictif"),
            ("Dédommagement", "qu'un juge devrait verser")]
    g = ['<g id="comment-lire">', t(x, y, "LES CINQ CRITÈRES", T_INTER, COND, weight="bold")]
    yy = y + T_TEXTE * 1.6
    for i, (a, b) in enumerate(defs):
        g.append(f'<text x="{x}" y="{yy:.1f}" font-size="{T_TEXTE}" fill="{ENCRE}">'
                 f'<tspan font-family="BarlowCondensed-Bold, {COND}" font-weight="bold" font-size="{T_TEXTE + 0.5}">{i + 1}. {a}</tspan>'
                 f'<tspan font-family="{SERIF}" fill="{ENCRE_2}"> {b}</tspan></text>')
        yy += T_TEXTE * 1.3
    g.append("</g>")
    return "\n".join(g), yy


def main():
    rangs = pd.read_excel(m.RES, sheet_name="rangs", index_col=0)
    gouttiere = 20
    pw = (L - 2 * M - gouttiere) / 2
    tete, y = entete_v2()
    corps = [tete]
    folio_y = H - 16
    # bas de page en 2 colonnes : les 5 critères à gauche, les sources à droite
    _, fin_cl = comment_lire_bas(M, 0, pw)
    _, fin_so = sources(M, 0, pw)
    bas_y = folio_y - 12 - (max(fin_cl, fin_so) + 2)
    cl, _ = comment_lire_bas(M, bas_y + T_INTER, pw)
    so, _ = sources(M + pw + gouttiere, bas_y + T_INTER, pw)
    corps.append(cl)

    haut = y + 22
    tete_panneau = T_PANNEAU + 26          # titre + en-têtes de colonnes
    ch = (bas_y - 12 - haut - 14 - 2 * (tete_panneau + 8)) / 2
    oy = haut
    groupes = list(m.REGIONS)
    for rangee in (groupes[:2], groupes[2:]):
        top = oy + tete_panneau
        for i, grp in enumerate(rangee):
            corps.append(panneau(rangs, grp, M + i * (pw + gouttiere), oy, pw, top, ch))
        oy = top + ch + 8 + 14
    corps.append(f'<line x1="{M}" y1="{bas_y - 6}" x2="{L - M}" y2="{bas_y - 6}" stroke="{ENCRE}" stroke-width="0.4"/>')
    corps.append(so)
    corps.append(t(M, folio_y, "38  |  Pour vous abonner : epsiloon.com", T_MINI, SEMI, fill=ENCRE_2))
    corps.append(t(L - M, folio_y, "PAR GALA RACHEDI, D'APRÈS LÉA DESRAYAUD", T_MINI, SEMI, "end", ENCRE_2))
    print(f"Hauteur d'un graphique : {ch:.0f} pt, soit {ch / 34:.1f} pt entre deux rangs")
    svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
           f'width="{L}pt" height="{H}pt" viewBox="0 0 {L} {H}">\n'
           f'<g id="fond"><rect width="{L}" height="{H}" fill="{FOND}"/></g>\n' + "\n".join(corps) + "\n</svg>\n")
    (m.OUT / "maquette_A4_v2.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
