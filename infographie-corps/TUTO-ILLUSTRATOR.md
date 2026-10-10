# Tuto Illustrator : finir la maquette « Ce que vaut notre corps »

Fichier de départ : `maquette/maquette_A4.svg`. Il a déjà le format A4 et les bons chiffres. Toi, tu fais les finitions.

> ⚠️ **Règle d'or** : si tu veux encore changer les données (filtre, parties en couleur…), fais-le **avant** de travailler dans Illustrator.
> Relancer les scripts recrée un SVG neuf : tout ce que tu as retouché à la main serait perdu.

Raccourcis cités : **Cmd** sur Mac = **Ctrl** sur Windows.

---

## 0. Avant d'ouvrir Illustrator : installer les polices
1. Télécharge **Barlow Condensed** : fonts.google.com/specimen/Barlow+Condensed (bouton « Get font » puis « Download »).
2. Télécharge **Source Serif 4** : fonts.google.com/specimen/Source+Serif+4
3. Installe les fichiers `.ttf`. Sur Mac : double-clic puis « Installer ». Sur Windows : clic droit puis « Installer pour tous les utilisateurs ».
   Il faut au minimum : Barlow Condensed Regular + Bold, et Source Serif 4 Regular + Bold + Italic.
4. Si Illustrator était ouvert, ferme-le et relance-le.

## 1. Ouvrir et régler le document
1. **Fichier > Ouvrir** → `maquette_A4.svg`.
2. **Enregistre tout de suite en .ai** : **Fichier > Enregistrer sous** → format Adobe Illustrator. Garde le SVG intact comme sauvegarde.
3. Unités en millimètres : **Illustrator > Réglages > Unités** sur Mac, **Édition > Préférences > Unités** sur Windows → Général : Millimètres.
4. Vérifie le format : **Fichier > Format du document** → 210 × 297 mm.
   Seulement si tu fais imprimer en imprimerie : fond perdu 3 mm de chaque côté. Agrandis alors le rectangle crème du fond jusqu'au trait rouge du fond perdu.
5. Affiche les règles (**Cmd+R**). Tire des repères depuis les règles à **12 mm** de chaque bord : ce sont les marges de la maquette.

## 2. Vérifier les polices
- Si une fenêtre « polices manquantes » s'ouvre : **Texte > Rechercher la police**, puis remplace chaque police manquante par la bonne.
- À contrôler :

  | Élément | Police |
  |---|---|
  | Titre, titres de panneaux, noms de parties | Barlow Condensed (**Bold** pour les titres) |
  | Chapô, annotations, sources | Source Serif 4 |

- Si un titre apparaît en maigre : sélectionne-le, ouvre **Fenêtre > Caractère** (**Cmd+T**), puis choisis le style **Bold**.

## 3. Ranger le fond
1. **Fenêtre > Calques**. Tout arrive dans un seul calque, découpé en **groupes nommés** : `fond`, `entete`, `comment-lire`, `panneau-fonctions`, `panneau-bras`, `panneau-jambes`, `panneau-visage`, `hommes-femmes`, `sources`.
2. Crée un nouveau calque « Fond » (icône ＋), glisse le groupe `fond` dedans, mets ce calque **tout en bas** et **verrouille-le** (clic sur le cadenas). Tu ne déplaceras plus le fond par erreur.
3. Pour retoucher l'intérieur d'un groupe : **double-clic** dessus (mode isolation). **Échap** pour en sortir.

## 4. Créer les couleurs en « nuances globales »
Avantage : si tu changes une couleur plus tard, elle change partout d'un coup.

1. **Fenêtre > Nuancier** → icône « Nouvelle nuance ». Mode RVB, saisis le code, coche **Couleur globale**.
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

3. Applique les nuances par lots. Exemple avec le rouge :
   - clique sur le ruban rouge ;
   - **Sélection > Même > Couleur de contour** : tous les contours rouges sont sélectionnés ;
   - clique sur la nuance « Rouge ».
4. Fais pareil pour chaque couleur. Pour les **points ronds**, utilise **Sélection > Même > Couleur de fond**.
5. ⚠️ **Les liserés** : sous chaque ruban coloré se trouve un ruban un peu plus épais, couleur crème, qui le détache des autres.
   Sélectionne-les (**Sélection > Même > Couleur de contour** sur l'un d'eux) et donne-leur la nuance **Fond**. Si tu changes le fond, ils suivront.

## 5. Refaire les textes longs en vrais paragraphes
Dans le SVG, chaque ligne de texte est un objet séparé : impossible de modifier une phrase proprement. Pour le **chapô**, chaque **annotation** et le bloc **sources** :

1. Sélectionne toutes les lignes du bloc, copie-les (**Cmd+C**), puis supprime-les.
2. Prends l'outil **Texte (T)** et **trace un rectangle** de la même largeur que l'ancien bloc : c'est une zone de texte.
3. Colle le texte (**Cmd+V**) et supprime les retours à la ligne en trop.
4. Règle la police dans **Fenêtre > Caractère** :

   | Bloc | Police | Taille / interligne |
   |---|---|---|
   | Chapô | Source Serif 4 | 10 pt / 13 pt |
   | Titre d'annotation | Barlow Condensed Bold | 8 pt |
   | Texte d'annotation | Source Serif 4 | 7 pt / 9 pt |
   | Sources | Source Serif 4 | 7 pt / 9 pt |

5. Si un petit **＋ rouge** apparaît en bas de la zone, le texte déborde : agrandis la zone.
6. Finition typographique : dans « 1re » ou « 3e », sélectionne « re » / « e », puis menu du panneau Caractère > **Exposant**.

## 6. Agrandir les noms des petites parties
Les noms à côté des rubans font 5,8 pt : c'est trop petit à l'impression.

1. Clique sur un nom gris (ex. « Bras »), puis **Sélection > Même > Taille de police**.
2. Passe-les à **6,5 pt**.
3. Corrige les chevauchements à la main : **flèches du clavier** (1 cran) ou **Maj+flèche** (gros cran).
   Pour les noms très serrés (orteils, doigts), écarte-les un peu et relie chacun à sa ligne par un filet très fin (0,25 pt, gris).

## 7. Ajouter les 4 pictogrammes
Un picto par panneau, à côté du titre (à la place du petit carré de couleur ou juste après) :

| Panneau | Picto |
|---|---|
| Fonctions & sens | œil ou cerveau |
| Bras & mains | main |
| Jambes & pieds | pied |
| Visage, dents & intimité | visage |

- **Option A, dessiner** : outils Plume (**P**) et Ellipse (**L**), traits de 1 pt aux extrémités arrondies, environ 14 × 14 pt, dans la couleur de la zone.
- **Option B, icônes libres** : par exemple **Phosphor Icons** (phosphoricons.com, licence MIT, gratuit). Télécharge en SVG, puis **Fichier > Importer** et recolorie avec ta nuance.
- Mets-les tous à la même taille et aligne-les sur les titres : **Fenêtre > Alignement**.

## 8. Finitions et vérifications
- [ ] Remplacer **[TON NOM]** en bas à droite.
- [ ] Aucun texte qui déborde (pas de ＋ rouge).
- [ ] **Test daltonisme** : **Affichage > Format d'épreuve > Daltonisme – type protanopie**, puis **deutéranopie**. Les 4 couleurs doivent rester distinctes. **Affichage > Couleurs d'épreuve** pour revenir à la normale.
- [ ] **Imprime la page à 100 %** sur une feuille A4 : les petits noms sont-ils lisibles ? Comprend-on le message en 5 secondes ?
- [ ] Les chiffres sur les rubans colorés n'ont pas bougé (ne les retape pas, ils viennent des données).

## 9. Exporter
- **Version de travail** : le `.ai`, que tu gardes éditable.
- **PDF à rendre** : **Fichier > Enregistrer une copie** → Adobe PDF → paramètre **[Qualité supérieure]**.
  Pour une imprimerie, choisis plutôt **[PDF/X-4]** et coche **Traits de coupe** + **Fond perdu** dans l'onglet « Repères et fonds perdus ».
- **Image pour le portfolio** : **Fichier > Exporter > Exporter pour les écrans** → PNG, échelle 2x.
- **Impression pro seulement** : passe avant en CMJN (**Fichier > Mode colorimétrique du document > CMJN**). Le bleu et le violet ternissent un peu : réajuste-les si besoin.

---

### Raccourcis utiles
| Touche | Action |
|---|---|
| V | Sélection |
| A | Sélection directe (un point, un morceau de courbe) |
| T | Texte |
| P | Plume |
| Espace (maintenu) | Main, pour se déplacer |
| Cmd+G / Cmd+Maj+G | Grouper / dégrouper |
| Cmd+2 | Verrouiller la sélection |
| Cmd+Alt+2 | Tout déverrouiller |
| Cmd+R | Règles |
| Cmd+Maj+O | Vectoriser le texte (seulement sur une copie finale : le texte n'est plus modifiable ensuite) |
