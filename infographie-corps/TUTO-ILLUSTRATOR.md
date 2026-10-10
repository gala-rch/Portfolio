# Tuto Illustrator (Windows, interface en anglais)

Fichier de départ : `maquette/maquette_A4.svg`. Le format A4 et les chiffres sont déjà bons : il te reste les finitions.

> ⚠️ **Règle d'or** : si tu veux changer les données (parties en couleur, filtre…), fais-le **avant** de commencer dans Illustrator. Relancer les scripts recrée un SVG neuf et tes retouches seraient perdues.

Les raccourcis sont ceux de Windows (Ctrl, Alt, Shift). Les menus sont en anglais.

---

## 0. Polices : déjà fait ✅
Barlow Condensed (Regular + Bold) et Source Serif 4 doivent être installées. Si Illustrator les affiche, passe à l'étape 1.

## 1. Ouvrir et enregistrer TOUT DE SUITE en .ai
1. **File > Open** → `maquette_A4.svg`.
2. **Avant de modifier quoi que ce soit** : **File > Save As** (Ctrl+Shift+S).
   - Choisis un dossier **local non synchronisé** (Documents ou Bureau, pas OneDrive).
   - Nom : `maquette_A4_v2.ai`.
   - **Save as type : Adobe Illustrator (*.AI)** (surtout pas SVG).
   - Dans la fenêtre suivante, laisse les options par défaut puis **OK**.
3. Ensuite, **Ctrl+S** enregistre en .ai.
   - Si Illustrator dit « This file has been modified outside Illustrator » : clique **No**, puis refais un Save As avec un nouveau nom.
4. Ne renomme **jamais** un fichier de `.svg` en `.ai` à la main : ça ne le convertit pas et il ne s'ouvre plus.

## 2. Régler le document
1. **Edit > Preferences > Units** → General : **Millimeters**.
2. **File > Document Setup** : vérifie 210 × 297 mm.
   - Seulement si tu fais imprimer en imprimerie : Bleed = 3 mm de chaque côté, puis agrandis le rectangle crème du fond jusqu'au bord rouge.
3. Affiche les règles : **Ctrl+R**. Tire des repères depuis les règles à **12 mm** de chaque bord (ce sont les marges de la maquette).

## 3. Réparer les polices en gras
Les titres en gras (titre, titres de panneaux, noms en gras sur les rubans…) peuvent s'afficher en Arial. Pour tous les corriger d'un coup :
1. **Esc**, puis clique dans une zone vide pour tout désélectionner.
2. **Type > Find Font…**
3. Dans « Fonts in Document », clique sur la ligne **Arial** (ou ArialMT / Arial-BoldMT) : les textes concernés se surlignent.
4. En bas, « Replace With Font From » reste sur **System**. Choisis **Barlow Condensed** + **Bold** dans la liste.
5. **Change All**, puis **Done**.

Ne touche pas aux textes déjà en Source Serif (« Big data », chapô, textes d'annotations, sources) : ils sont corrects.

## 4. Ranger le fond
1. **Window > Layers**.
2. Crée un nouveau calque « Fond » (icône ＋), glisse dedans le groupe `fond`, mets ce calque tout en bas et **clique sur le cadenas** : plus de risque de le déplacer.
3. Pour retoucher le contenu d'un groupe : **double-clic** dessus (mode isolation). **Esc** pour en sortir.
4. Si tu veux sélectionner un seul élément d'un groupe : outil flèche blanche (**A**, Direct Selection) puis clic dessus.

## 5. Créer les couleurs en nuances globales
Avantage : tu changes une couleur une fois, elle change partout.

1. **Window > Swatches**. Clique sur l'icône « New Swatch ». Mode RGB, saisis le code (champ Hex), coche **Global**.
2. Crée ces nuances :

   | Nom | Code |
   |---|---|
   | Fond | `#F7EFDF` |
   | Encre | `#1E1B18` |
   | Encre légère | `#6E665A` |
   | Gris clair (rubans de contexte) | `#E3D9C6` |
   | Gris moyen (rubans de la zone) | `#A39A8A` |
   | Pouce | `#4E473E` |
   | Rouge, Fonctions & sens | `#CC3D2A` |
   | Bleu, Bras & mains | `#1A7BB0` |
   | Ocre, Jambes & pieds | `#D99200` |
   | Violet, Visage, dents & intimité | `#7D3FA0` |

3. Applique-les par lots (exemple avec le rouge) :
   - clique sur un ruban rouge avec la flèche blanche (**A**) ;
   - **Select > Same > Stroke Color** : tous les contours rouges sont sélectionnés ;
   - clique sur la nuance « Rouge » dans Swatches.
4. Même chose pour chaque couleur. Pour les **points ronds**, utilise **Select > Same > Fill Color**.
5. ⚠️ **Les liserés** : sous chaque ruban coloré, il y a un ruban un peu plus épais de couleur crème qui le détache des autres. Sélectionne-en un, fais **Select > Same > Stroke Color**, puis applique la nuance **Fond**.

## 6. Refaire les textes longs en vrais paragraphes
Dans le SVG, chaque ligne de texte est un objet séparé : impossible de modifier une phrase proprement. À faire pour le **chapô**, chaque **annotation** et le bloc **sources** :
1. Sélectionne toutes les lignes du bloc, copie (**Ctrl+C**), puis supprime-les.
2. Outil **Type (T)** : **trace un rectangle** de la largeur de l'ancien bloc (c'est une zone de texte).
3. Colle (**Ctrl+V**) et supprime les retours à la ligne en trop.
4. **Window > Type > Character** (Ctrl+T), puis règle :

   | Bloc | Police | Taille / interligne |
   |---|---|---|
   | Chapô | Source Serif 4 | 10 pt / 13 pt |
   | Titre d'annotation | Barlow Condensed Bold | 8 pt |
   | Texte d'annotation | Source Serif 4 | 7 pt / 9 pt |
   | Sources | Source Serif 4 | 7 pt / 9 pt |

5. Si un petit **＋ rouge** apparaît en bas de la zone, le texte déborde : agrandis la zone.
6. « 1re », « 3e » : sélectionne « re » ou « e », puis dans le menu (≡) du panneau Character, choisis **Superscript**.

## 7. Agrandir les noms des petites parties
Ils font 5,8 pt : trop petit à l'impression.
1. Avec la flèche blanche (**A**), clique sur un nom gris (ex. « Bras »).
2. **Select > Same > Font Size**.
3. Dans Character, passe la taille à **6,5 pt**.
4. Corrige les chevauchements à la main avec les **flèches du clavier** (**Shift+flèche** = grand déplacement). Pour les noms très serrés (orteils, doigts), écarte-les et relie chacun à sa ligne par un filet très fin (0,25 pt).

## 8. Ajouter 4 pictogrammes
Un par panneau, à côté du titre :

| Panneau | Picto |
|---|---|
| Fonctions & sens | œil ou cerveau |
| Bras & mains | main |
| Jambes & pieds | pied |
| Visage, dents & intimité | visage |

- **Dessiner** : outils Pen (**P**) et Ellipse (**L**), traits de 1 pt aux extrémités arrondies, environ 14 × 14 pt, dans la couleur de la zone.
- **Ou icônes libres** : **Phosphor Icons** (phosphoricons.com, gratuit). Télécharge en SVG, puis **File > Place** et recolorie avec ta nuance.
- Même taille pour les 4 et aligne-les avec **Window > Align**.

## 9. Finitions et vérifications
- [ ] Remplacer **[TON NOM]** en bas à droite.
- [ ] Aucun texte qui déborde (pas de ＋ rouge).
- [ ] **Test daltonisme** : **View > Proof Setup > Color Blindness – Protanopia-type**, puis **Deuteranopia-type**. Les 4 couleurs doivent rester distinctes. **View > Proof Colors** pour revenir à la normale.
- [ ] **Imprime à 100 %** sur une feuille A4 : les petits noms sont-ils lisibles ? Comprend-on le message en 5 secondes ?
- [ ] Les chiffres sur les rubans colorés n'ont pas bougé (ils viennent des données, ne les retape pas).

## 10. Exporter
- **Version de travail** : le `.ai`.
- **PDF à rendre** : **File > Save a Copy…** → type Adobe PDF (*.PDF) → preset **[High Quality Print]**. Pour une imprimerie, choisis plutôt **[PDF/X-4]** et coche **Trim Marks** + **Use Document Bleed Settings** dans l'onglet « Marks and Bleeds ».
- **Image pour le portfolio** : **File > Export > Export for Screens…** → PNG, échelle 2x.
- **Impression pro seulement** : **File > Document Color Mode > CMYK**. Le bleu et le violet ternissent un peu, réajuste-les si besoin.

---

### Raccourcis utiles (Windows)
| Touche | Action |
|---|---|
| V | Selection (flèche noire) |
| A | Direct Selection (flèche blanche : un seul élément d'un groupe) |
| T | Type (texte) |
| P | Pen |
| Espace maintenu | Main (déplacer la vue) |
| Ctrl+G / Ctrl+Shift+G | Grouper / dégrouper |
| Ctrl+2 | Verrouiller la sélection |
| Ctrl+Alt+2 | Tout déverrouiller |
| Ctrl+R | Règles |
| Ctrl+T | Panneau Character |
| Ctrl+Shift+O | Vectoriser le texte (**Type > Create Outlines**), seulement sur une copie finale : le texte n'est plus modifiable ensuite |
