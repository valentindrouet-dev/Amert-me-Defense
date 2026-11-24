# Prompts des planches manquantes (v0.9.8)

Chaque planche : **fond transparent**, éléments bien séparés, même échelle à l'intérieur d'une planche.
Coller le **bloc de style** en tête de chaque prompt, puis le texte de la planche.

> Dark-fantasy pixel art, high-detail 16-bit look, muted earthy palette, warm gold accents, crisp dark 1px outline, soft top-left light. 3/4 isometric view (2:1). Fully transparent background, no ground, no shadow, no text, no grid. Every element separated by generous empty space, same scale.

Règles de pose communes :
- **Unités** (une ligne par personnage, 4 images de gauche à droite) : *idle*, *walk 1*, *walk 2*, *attack*. Tournées vers la **droite** (vers le bas-droite en 3/4).
- **Monstres** (une ligne par créature, 4 images) : *walk 1*, *walk 2*, *attack*, *dead* (couché au sol). Tournés vers la **droite**, comme les monstres actuels (le jeu les retourne).
- Bâtiments : une image par élément, vue 3/4 iso, base en losange 2:1 visible.

---

## 1. Unités de soutien (3 lignes × 4 poses)

```
Sprite sheet of 3 medieval militia support units for a village defense game, one character per row, 4 frames per row from left to right: idle, walk step 1, walk step 2, action. All facing right.
Row 1 — War dog: a lean, scarred mastiff in a riveted leather harness with an iron spiked collar, muzzle with old wounds, alert ears. Frames: standing alert, trotting, trotting other leg, lunging bite with open jaws.
Row 2 — Standard bearer: sturdy villager-soldier in a padded gambeson and open iron helm, holding high a tall wooden pole with a tattered crimson banner bearing a gold tower emblem. Frames: banner upright, marching, marching, banner raised and waved overhead.
Row 3 — War drummer: young soldier in a brown tabard with a large hide drum strapped at the hip, two wooden mallets. Frames: standing, marching while drumming, marching other step, both mallets raised striking hard.
Same scale for all, human figures about 120 px tall, the dog about 70 px tall.
```
Découpe : `python3 tools/sprites.py units planche.png chien:96 etendard:128 tambour:124`

---

## 2. Nouvelles créatures de la Charogne (5 lignes × 4 poses)

```
Sprite sheet of 5 carrion-plague monsters ("the Charogne": rotting, fungal, bone and sinew, sickly green-yellow ichor), one creature per row, 4 frames per row from left to right: walk step 1, walk step 2, attack, dead lying on the ground. All facing right.
Row 1 — Carrion vulture: huge bald vulture with mangy grey-brown feathers, exposed ribs, bone beak, wings spread in flight. Frames: wings up, wings down, diving claws forward, crashed on the ground wings splayed.
Row 2 — Bone slinger: hunched gaunt ghoul with too-long arms, a sling made of sinew, a pouch of sharpened bones on its belt. Frames: walking, walking, whirling the sling overhead, collapsed.
Row 3 — Carrion shaman: tall emaciated ghoul wrapped in rags and antlers, a staff topped with a skull and glowing sickly-green fungus, bone fetishes. Frames: walking with staff, walking, staff raised casting a green glow, fallen with broken staff.
Row 4 — Swarming mass: a blob of fused carrion bodies, many small limbs and mouths, pulsing fungal growths, about knee-high to waist-high. Frames: crawling, crawling, rearing up to slam, burst apart into puddle.
Row 5 — Spawnling: tiny skittering fragment of the mass, rat-sized, three legs and a mouth. Frames: scuttling, scuttling, leaping bite, splattered.
Scale: vulture 90 px tall in flight, slinger and shaman 110 px tall, mass 120 px tall, spawnling 40 px tall.
```
Découpe : `python3 tools/sprites.py mons planche.png vautour:96 frondeur:112 chaman:124 amas:128 grouillon:40`

---

## 3. Boss des nuits 10, 15 et 20 (3 lignes × 4 poses)

```
Sprite sheet of 3 giant carrion-plague boss monsters, one per row, 4 frames per row from left to right: walk step 1, walk step 2, attack, dead lying on the ground. All facing right. Very large, imposing silhouettes.
Row 1 — The Canker: an enormous bloated plague-ogre, skin covered in pustules and yellow-green fungal chancres leaking toxic mist, tiny head, massive belly, dragging knuckles. Attack: both fists slamming the ground with a burst of spores. Dead: deflated, collapsed in a puddle.
Row 2 — The Crow-Mother: a gigantic black carrion crow with three eyes, ragged wings full of smaller crows nesting in its feathers, a bone crown on its head, in flight. Attack: diving with talons spread, shrieking. Dead: fallen on its back, wings broken.
Row 3 — The Ram-King: a colossal armored ram-beast standing on four legs, huge curled horns banded with iron, rusted armor plates nailed into its hide, a ragged crown wedged between the horns. Attack: head lowered charging, horns forward. Dead: collapsed on its side.
Scale: each boss about 300 px tall (3 times a normal soldier).
```
Découpe : `python3 tools/sprites.py mons planche.png chancre:190 merec:160 roib:150`

---

## 4. Boss final : la Charogne-Mère (2 lignes × 4 poses)

```
Sprite sheet of the final boss "The Carrion Mother", 2 rows, 4 frames per row from left to right: walk step 1, walk step 2, attack, dead lying on the ground. Facing right.
Row 1 — The Carrion Mother, armored form: a towering matriarch monster made of fused corpses and bone, a huge plated carapace of rib-bones on her back, many arms, a crown of antlers and fungus, dark red ichor, birthing sacs on her belly. Attack: rearing up with arms spread, roaring.
Row 2 — The same creature after shedding her carapace (phase 3, frenzy): thinner, raw red flesh and sinew exposed, glowing ember-red eyes and cracks, faster and more savage pose. Attack: leaping strike with claws.
Scale: about 500 px tall, the largest creature in the game.
```
Découpe : `python3 tools/sprites.py mons planche.png charmere:255 charmere3:240`
(la ligne 2 demandera un petit branchement dans le code pour la phase 3)

---

## 5. Chenil, porte fortifiée, armes de rempart (bâtiments)

```
Sprite sheet of 7 medieval village defense structures, isometric 3/4 view, each a separate object with its diamond 2:1 base visible, reading order left to right then top to bottom:
1 — War kennel: small timber and stone kennel with a thatched roof, wooden fence pen, a bone pile and a chain stake, a carved dog-head sign.
2 — Fortified stone gate, intact: a stone gatehouse two tiles wide with a heavy oak door reinforced with iron bands, small crenellated parapet, torches either side.
3 — The same fortified gate, damaged: cracked stones, splintered door, one torch out, scorch marks.
4 — The same fortified gate, destroyed: rubble heap, broken door planks, fallen stones.
5 — Rampart crossbow: a heavy ballista-like crossbow on a wooden swivel mount, sized to sit on top of a stone wall segment.
6 — Pitch cauldron: a large iron cauldron on a tilting wooden frame with a fire under it, bubbling black pitch, a long pouring spout, sized to sit on a wall.
7 — Same pitch cauldron, tipped over pouring a stream of burning pitch.
Scale: kennel about 1 tile (comparable to a small hut), gate as wide as 2 wall segments, rampart weapons about one third of a wall segment.
```
Découpe : `python3 tools/sprites.py bld planche.png kennel:240 sgate:260 sgateD:260 sgateX:260 sv_arb:110 sv_poix:110 sv_poix2:110`

---

## 6. Mur de pierre raccordable

Le mur actuel n'a que deux orientations et un poteau. Pour qu'il se raccorde proprement, il faut les pièces d'angle, de T et de croisement, chacune en 3 états.

```
Sprite sheet of modular stone castle wall pieces for an isometric 2:1 tile grid, grey fieldstone with mortar, small crenellations on top, same height for all pieces. Arrange in 3 rows: row 1 intact, row 2 cracked and chipped, row 3 ruined (half collapsed, rubble at base). Each row contains, left to right, these 7 pieces:
1 — straight segment running toward the bottom-left / top-right diagonal,
2 — straight segment running toward the bottom-right / top-left diagonal,
3 — square pillar (end post),
4 — corner joining the two diagonals (L-shape, opening downward),
5 — corner joining the two diagonals (L-shape, opening upward),
6 — T junction,
7 — cross junction.
All pieces sit on the same tile footprint and line up seamlessly when placed side by side.
```
Découpe : `python3 tools/sprites.py bld planche.png` puis je nomme les 21 pièces à l'intégration (le code doit être adapté pour choisir la bonne pièce selon les voisins).

---

## 7. Carte en haute définition (3344×1882)

**Important** : la zone constructible et les 4 chemins d'entrée sont calculés à partir de la carte actuelle. La nouvelle doit avoir **exactement la même composition** (même clairière, mêmes chemins, mêmes éboulis). Le mieux : donner `img/bg.webp` à l'IA comme image de référence et lui demander de la redessiner à ×2.

```
Redraw this exact map at twice the resolution (3344×1882 pixels), keeping the composition pixel-for-pixel identical: same clearing shape and position, same four dirt paths entering from the four corners, same tree line, same rocks and rubble spots. Only add detail and sharpness: individual grass blades and wildflowers in the clearing, packed earth and wheel ruts on the paths, dense dark pine and twisted oak forest around the edges with layered canopy, moss on rocks, a few fallen logs and mushrooms at the forest edge. Dark-fantasy pixel art, high-detail 16-bit look, muted earthy palette, soft top-left light, top-down 3/4 isometric view (2:1). No buildings, no characters, no text, no UI.
```
Si l'IA ne garde pas la composition, un **agrandissement ×2** (upscale) de l'image actuelle sans changement de cadrage fera l'affaire.

---

## 8. Persos animés (format 4×4, 16 images)

Une planche par perso, image carrée 1024×1024, avec une image du perso actuel en référence (*keep this exact character design*). Découpe : `python3 tools/anim.py planche.png nom 84` puis ajouter la ligne affichée dans `ANIM`.

```
Pixel art sprite sheet of ONE character for a dark-fantasy isometric tower defense game.
Character: <description du perso>.

Layout: a strict grid of 4 rows x 4 columns, 16 frames total, each frame centered in its own equal square cell, generous empty space between frames, no frame touching another. Fully transparent background, no ground, no shadow under the feet, no text, no grid lines, no labels.
Row 1 – IDLE (4 frames): breathing loop, chest and shoulders rise and fall.
Row 2 – WALK (4 frames): clear walk cycle — 1 left foot forward wide stride, 2 passing pose body high, 3 right foot forward wide stride, 4 passing pose body high. Legs and arms must visibly swing, no sliding.
Row 3 – ATTACK (4 frames): 1 anticipation (body coiled back, weapon raised far behind), 2 lunge forward, 3 impact (arm fully extended, motion smear), 4 recovery.
Row 4 – HURT and DEATH (4 frames): 1 hurt recoil, 2 collapsing to knees, 3 falling sideways, 4 lying dead flat on the ground.

Every frame faces RIGHT in a 3/4 isometric view (2:1). Same character, identical proportions, colors and equipment in every frame, same scale, same pixel size, feet on the same baseline in each cell.

Readability at small size (the sprite will be shown about 50 px tall):
- strong silhouette with exaggerated, dynamic poses and clear negative space between limbs and body;
- thick dark 2px outline around the whole figure;
- high value contrast: bright warm rim light from the top-left, deep shadow on the right side, three clear tones per material;
- limited palette, no noisy texture;
- strong accents (eyes, weapon highlight), skin clearly separated in value from clothing.
Dark-fantasy pixel art, high-detail 16-bit look, muted earthy palette with warm gold accents.
```
Attaque à distance : *1 draws, 2 aims, 3 releases with recoil, 4 lowers*. Magie : *1 gathers energy, 2 raises hands, 3 casts with a glow burst, 4 recovers*. Volant : remplacer WALK par *FLY: wing up, wing mid, wing down, wing mid*.
