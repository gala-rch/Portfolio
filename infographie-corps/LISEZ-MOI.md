# Ce que vaut notre corps — analyse des données (USA)

Dossier de travail pour la refonte de l'infographie Epsiloon (p. 38, L. Desrayaud).
Tout est reproductible : on relance les deux scripts et on retrouve exactement les mêmes chiffres.

## Contenu du dossier

| Fichier | À quoi il sert |
|---|---|
| `donnees/Data.xlsx` | Données brutes de l'étude (Dryad), telles que téléchargées. **Ne pas modifier.** |
| `analyse.py` | Script de calcul : filtre, moyennes, rangs, écarts, hommes/femmes, stabilité. |
| `graphiques.py` | Script qui dessine les brouillons SVG à partir des résultats. |
| `sorties/resultats_USA.xlsx` | **Le fichier à ouvrir en premier.** Tous les tableaux, un onglet par sujet, avec un onglet LISEZ-MOI. |
| `sorties/*.csv` | Les mêmes tables en CSV (séparateur `;`, virgule décimale : s'ouvrent directement dans Excel FR). |
| `graphiques/*.svg` | Brouillons vectoriels à ouvrir dans Illustrator / Figma. |
| `graphiques/apercus/*.png` | Les mêmes en image, pour un coup d'œil rapide. |

### Relancer
```bash
pip install pandas openpyxl
python3 analyse.py      # recalcule tout → sorties/
python3 graphiques.py   # redessine → graphiques/
```
Les réglages (filtre oui/non, parties mises en avant, couleurs) sont en haut de chaque script, dans une section `RÉGLAGES`.

## Méthode, étape par étape

1. **Structure du fichier** : 2 feuilles, `US data` (306 lignes) et `India Data` (308). On ne garde que les USA.
   48 colonnes : participant, pays, condition, sexe, 39 parties du corps, âge, études, test d'attention, domaine, inclusion.
2. **Filtre** : on garde `Data inclusion = 1` (critères des auteurs) → **282 participants sur 306**.
   Chaque personne n'a répondu qu'à **un seul critère**, donc **39 à 42 personnes par critère** (onglet `effectifs`).
3. **Parties gardées** : les 35 de l'affiche. On écarte « Both testicles », « One testicle » (question réservée aux hommes, en pratique),
   « One ear » et « One eye » (doublons avec l'ouïe et la vue).
4. **Échelles** : Difficulté, Colère, Gratitude sont notées de 0 à 100 ; Prix et Dédommagement de **0 à 10**.
   On ne compare donc jamais les valeurs d'un critère à l'autre, seulement les **rangs**.
5. **Calcul** : pour chaque critère, moyenne des notes de chaque partie, puis classement de 1 (moyenne la plus haute = la plus précieuse) à 35.
   La médiane est aussi calculée mais inutilisable pour classer : beaucoup de parties ont une médiane de 100 (tout le monde met le maximum).
6. **Mouvements** (onglet `mouvements`). **Signe : + = la partie monte (devient plus précieuse), − = elle descend.**
   - `amplitude` = pire rang − meilleur rang, en comparant **tous** les critères entre eux. C'est la mesure principale, et elle ne dépend pas de l'ordre des colonnes.
     Les ex æquo sont départagés par `ecart_type_des_rangs`.
   - Colonnes `A → B` : les 10 couples de critères possibles, voisins ou non.
   - `zigzag_sur_le_graphique` = somme des sauts entre colonnes **voisines** de l'affiche (colonnes `voisins ·`).
     Cette mesure dépend de l'ordre des colonnes : elle dit combien le ruban ondule à l'œil, pas combien la partie change vraiment.
7. **Hommes / femmes** (onglet `hommes_femmes`) : rangs recalculés séparément par sexe, puis moyennés sur les 5 critères.
8. **Stabilité** (onglet `stabilite_rangs`) : bootstrap. On retire au hasard, avec remise, les ~40 répondants d'un critère,
   on recalcule les rangs, 2000 fois. On garde l'intervalle qui contient 95 % des rangs obtenus.
   Si l'intervalle est large, le rang dépend de quelques personnes : il ne faut pas en faire une annotation.

## Vérifications

- **La colonne Difficulté retrouve l'ordre de l'affiche**, à 4 inversions près entre voisins (11↔12, 16↔17, 19↔20, 29↔30). La méthode est donc la bonne.
- **L'affiche a probablement utilisé les 306 répondants sans filtre**, comme l'indique sa mention « 306 Américains ».
  Sans filtre, la motricité est 1ʳᵉ en Dédommagement, comme sur l'affiche ; avec filtre, elle est 2ᵉ. L'onglet `filtre_ou_non` compare les deux.
  Je conseille de garder le filtre, qui correspond à la méthode des auteurs, et d'écrire « 282 Américains » dans les sources.

## Ce que disent les données

### Les parties qui bougent le plus (amplitude, tous critères comparés)
| Partie | Rangs (Diff. → Colère → Gratitude → Prix → Dédomm.) | Meilleur → pire | Amplitude | Zigzag |
|---|---|---|---|---|
| **Parties génitales** | 20 → 8 → 21 → 12 → 8 | 8 (Colère) → 21 (Gratitude) | 13 | 38 |
| **Les 2 pieds** | 8 → 18 → 15 → 9 → 5 | 5 (Dédomm.) → 18 (Colère) | 13 | 23 |
| **Les 10 doigts** | 10 → 3 → 10 → 16 → 11 | 3 (Colère) → 16 (Prix) | 13 | 25 |
| **Parole et mastication** | 7 → 12 → 1 → 7 → 9 | 1 (Gratitude) → 12 (Colère) | 11 | 24 |
| Vue d'un œil | 19 → 22 → 18 → 11 → 18 | 11 (Prix) → 22 (Colère) | 11 | 21 |
| Ouïe d'une oreille | 22 → 25 → 20 → 14 → 21 | 14 (Prix) → 25 (Colère) | 11 | 21 |

Les trois premières sont **ex æquo** à 13 places d'écart. Les parties génitales ne se distinguent que par le zigzag : elles montent et descendent plusieurs fois.

Il y en a une par région : c'est ce choix qu'utilisent les graphiques, et c'est un réglage modifiable dans `graphiques.py`.

### Trois annotations de l'affiche à revoir
- **Le pouce** (15 → 17 → 14 → 21 → 20) bouge peu. L'affiche parle des **codes légaux réels**, qui ne sont **pas dans Data.xlsx** : ici, « Dédommagement » est l'avis du public, pas la loi.
  Garder cette annotation demande de citer l'article. En revanche, le pouce est **la partie où hommes et femmes divergent le plus** : rang moyen 15 chez les hommes, 19 chez les femmes.
- **Les orteils et les hommes** : ce n'est pas visible en rangs (« Les 10 orteils » : rang moyen 18 chez les deux sexes). L'article s'appuie sans doute sur un test statistique sur les valeurs et sur les deux pays.
  À ne pas reprendre tel quel.
- **Les femmes et la paralysie / défiguration** : confirmé. Les femmes placent plus haut les capacités mentales (2 contre 5), la motricité (2,6 contre 4,4) et le visage (7 contre 9,4).

### Prudence sur les colonnes Colère et Gratitude
Sur ces deux critères, beaucoup de parties sont notées près de 100 : les premiers rangs sont presque à égalité, donc fragiles (voir `05_stabilite_rangs`).
- **Solides** : génitaux, de 14–20 en Difficulté à 4–11 en Dédommagement ; les 2 pieds, qui chutent en Colère (6–10 → 11–25) ; la parole, 1ʳᵉ en Gratitude (1–8) ; le **visage**, qui grimpe en Prix (10–14 → 1–7).
- **Fragiles** : le 3ᵉ rang des 10 doigts en Colère (1–12) ; le 12ᵉ de la parole en Colère (6–22).

Le visage (13 → 11 → 6 → 4 → 7) est un bon candidat de remplacement dans la région « Visage, dents & intimité ».

## Les graphiques (brouillons)

| Fichier | Description |
|---|---|
| `01_rubans_35_parties.svg` | L'affiche d'origine redessinée : 35 rubans gris, 4 mis en couleur. |
| `02_petits_multiples_4_regions.svg` | **La forme retenue** : 4 panneaux par région, même échelle 1→35, une partie en couleur par panneau. |
| `03_heatmap_rangs.svg` | Tableau de rangs coloré, par région. Utile pour vérifier, ou comme encadré. |
| `04_hommes_femmes.svg` | Rang moyen hommes contre femmes. Matière pour une annotation. |
| `05_stabilite_rangs.svg` | Outil de travail, pas pour la page : montre quels rangs sont fiables. |

Dans Illustrator, chaque SVG est découpé en calques nommés (`fond`, `grille`, `rubans-contexte`, `rubans-accent`, `libelles`…).
Le texte reste modifiable et la police (Helvetica) est provisoire. 1 unité = 1 pt : le fichier 02 fait environ 183 × 226 mm, la bonne échelle pour une page A4.

Couleurs provisoires : les 4 accents (bleu, orange, vert d'eau, violet) ont été vérifiés pour rester distincts pour les daltoniens.
Le vert d'eau est peu contrasté sur fond clair : c'est acceptable parce que chaque ruban coloré porte son nom en toutes lettres.
La palette finale sera à définir pendant la phase design.

## Source
Wee, Y. N., Sznycer, D., & Krems, J. A. (2025). *Laws about bodily damage originate from shared intuitions about the value of body parts*. Science Advances, 11(2). DOI 10.1126/sciadv.ads3688.
Données : Dryad, DOI 10.5061/dryad.7m0cfxq4c (licence CC BY-NC).
