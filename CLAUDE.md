# Les Nuits de Lamuline — passation

Jeu navigateur de défense jour/nuit dans l'univers du JDR **Amertüme** (Big Budi Games, Valentin Drouet).
Le jour : bâtir, recruter, améliorer. La nuit : la horde de la Charogne arrive par les chemins et marche sur le donjon. Objectif : tenir 10 nuits, puis mode infini.

Développé jusqu'ici dans Claude (artefact), version V9.5. Valentin pilote, génère les planches de sprites avec une autre IA, et Claude les intègre.

## Lancer / tester
- Aucune dépendance, aucun build : tout est dans `index.html` (HTML + CSS + un seul `<script>`).
- Servir en local : `python3 -m http.server 8765` puis `http://localhost:8765` (pas en `file://`, les images ne se chargent pas toutes).
- Vérif syntaxe rapide : extraire le dernier `<script>` et `node -e "new Function(src)"`.
- Tests visuels : Playwright + captures. Hooks dispo : `window.__S()` (état) et `window.__test` (`step`, `tryPlace`, `addUnit`, `startNight`, `dawn`, `openInfo`, `selU`, `setPaused`, `cam`, `centerOn`, `endScreen`, `saveGame`, `loadGame`…). Ex. : forcer la nuit avec `S.t=119.9` puis boucler `T.step(0.05)`.
- **Toujours vérifier à l'écran (capture) avant de livrer** : Valentin juge sur le rendu.

## Arborescence
- `index.html` : le jeu.
- `img/bg.webp` carte 1672×941 (clairière, 4 entrées en coin) ; `img/ebouA|ebouB.webp` éboulis des entrées 3 et 4.
- `img/b/` bâtiments · `img/u/<id>_{idle,w1,w2,atk}.webp` unités/héros · `img/m/<id>_{w1,w2,atk,dead}.webp` + `_rim` monstres · `img/i/` icônes 128² · `img/fx/<nom>.webp` effets (bande de 6 frames 128²).
- `tools/sprites.py` : découpe des planches (voir plus bas).

## Architecture du code (index.html)
- **Monde iso 2:1** : `WW,WH` (taille carte), `TW=64,TH=32,OX,OY`, `MK` (échelle, laissée à 1 : Valentin a refusé ×1,5 et ×2). `iso(i,j)`, `cellOf(x,y)`.
- **Temps** : `DAY=120, NIGHT=110` en secondes de jeu, `TIME=2` (×1 = 2 s de jeu par seconde réelle). Phases `S.phase` = day / night / dawn ; `S.eclipse` = mini-nuit de jour.
- **Données** : `B` bâtiments (lv[], up[], ut[], un[]), `U` gardes, `W` villageois, `ALLU`, `M` monstres, `HEROES`/`HD`, `SK` compétences héros, `REQ` déblocages, `TIERS` arbre, `LISTS` onglets bas, `EQ/EQC` armurerie, `TV` spécialisations de tour, `NIGHTS`, `HTABLES` tables de groupes de la horde (débloquées par nuit `t`, budget `hBudget`, coût `MCOST`), `CHALS`, `SEASONS`, `ELITES`, `ACH` hauts faits, `NOTES` notes de version (à compléter à chaque version).
- **Dés Amertüme (d6)** : `roll(dice,def,mul)`. W blanc compte s'il dépasse la DEF ; R rouge ignore la DEF ; B mystique doit dépasser la DEF, doublé sur double ; double 1 = Échec.
- **Grille** : `S.grid` Map "i,j" → bâtiment ; `CELLSET` cellules constructibles (généré depuis le masque de la clairière) ; la porte occupe 2 cases (`b.cells`, `gateCells`).
- **Entrées** : `ENTRY` (chemins en coordonnées carte), `openEntries(jour)` : 2 au départ, 3 dès la nuit 4, 4 dès la nuit 8. Totem d'entrée dessiné à `entMk(e)`.
- **Navigation** :
  - monstres : champs de flux Dijkstra `navEnsure()`/`ffStep()` (coût des murs selon leurs PV, `navVer` à incrémenter quand la grille change) ; ils s'arrêtent et frappent les barricades ; Fouisseur creuse 4 s.
  - unités : A* + lissage `astar()`/`navTo()`, contournent palissades, passent par les portes ; `rangedSpot()` garde tireurs/mages derrière l'enceinte si elle est fermée.
  - `wallBetween(a,b)` empêche de frapper à travers une barricade ; les monstres ciblent les unités avant les défenses (sauf Brutes et Béliers).
- **Boucle** : `step(dt)` logique · `draw(t)` rendu canvas (tri par profondeur, `outlined()` surbrillance, `ghostLine()` contour des unités cachées derrière un bâtiment, `occBy()`) · `refresh()` HUD · `hud()` plaque jour/nuit.
- **VFX** : `fxAdd(nom,x,y,{f0,f1,dur,sz,rot,flip,add})`, `fxFrame()`, `fire()` (flammes animées).
- **UI** : barre du bas `renderCards()` (onglets b, d, p, u, w, h = Héros), cadre d'unité compact `#info.uf` (3 lignes, à droite des ressources), fenêtres bâtiment `bldModal`, `dialog()/closeDlg()` (clic à côté ferme), rapport de l'aube `showReport()` (auto-fermeture 10 s), accueil `hmRender()`, menu (Progression, Arbre, Hauts faits, Bestiaire, Encyclopédie, Règles, Paramètres, Sauvegarder, Recharger, Recommencer, Accueil).
- **Sauvegarde** : `saveGame(k)/loadGame(o)` en localStorage (`lamuline-save` auto à chaque aube, `lamuline-slot1..3`), méta inter-parties `lamuline-meta` (kills, unité phare, hauts faits, bestiaire vu), scores `lamuline-scores`, réglages `lamuline-cfg`.

## Pipeline sprites
Valentin génère des planches à fond transparent ; on lance `tools/sprites.py` (voir docstring). Repères de taille actuels (sprite dessiné à ½ de sa taille fichier) :
- unités ~60–66 px de haut (héros 76–96), monstres : `charo` 54, brute 96, colosse 176, matriarche ~160 ;
- bâtiments : largeur de dessin dans `bodyBld()` (ferme 168, puits 38, marché 118, taverne 122, chapelle 108, Hall des Charognards 118…). Toujours comparer à la ferme et à la scierie.
- Nouveaux sprites : ajouter le nom dans les listes de préchargement (`UP` pour les unités, `MS` pour les monstres avec la taille de `w1`, liste `img/b/` pour les bâtiments) puis brancher le dessin.

Bloc de style à mettre en tête des prompts de planches :
> Dark-fantasy pixel art, high-detail 16-bit look, muted earthy palette, warm gold accents, crisp dark 1px outline, soft top-left light. 3/4 isometric view (2:1). Fully transparent background, no ground, no shadow, no text, no grid. Every element separated by generous empty space, same scale.

## État et pistes ouvertes
- Fait : 60 améliorations de la V5, carte 4 entrées, barricades étanches, patrouilles, palissade à pieux, Hall des Charognards (traque par espèce), Bestiaire, Porteur d'eau, accueil/sauvegardes/hauts faits, VFX, tous les sprites.
- À surveiller : équilibrage (Valentin trouvait le jeu trop facile avant la V6), lisibilité mobile (< 900 px le cadre d'unité repasse en panneau bas), perfs avec beaucoup de monstres (champs de flux recalculés quand la grille change).
- Idées non faites : sons/musique, carte plus nette en 3344×1882 si Valentin la fournit, découpage de `index.html` en modules si le fichier devient ingérable.

## Façon de travailler avec Valentin
- Réponses en **français**, courtes et concrètes ; il envoie souvent plusieurs retours d'affilée en cours de travail : les traiter tous.
- Il teste et renvoie des captures : corriger, vérifier en capture, puis livrer.
- Ne jamais toucher l'échelle globale sans qu'il le demande.
- **Version** : constante `VERSION` dans `index.html` (affichée sur l'accueil, le menu et le titre de l'onglet). L'augmenter à **chaque push** (0.9 → 0.9.1 → 0.9.2…, palier rond sur demande de Valentin) et ajouter une entrée `NOTES` du même numéro.
