"""Découpe d'une planche d'animation en grille (une ligne = une animation) pour Les Nuits de Lamuline.

Usage :
  python3 tools/anim.py planche.png nom hauteur [lignes colonnes]
    -> img/a/<nom>/<r><c>.webp  (r = ligne, c = colonne, à partir de 0)

Format de planche attendu (prompt dans docs/prompts-sprites.md) : 4 lignes x 4 colonnes, cases égales,
fond transparent (un fond blanc uni est retiré automatiquement), perso tourné vers la droite.
  ligne 0 : repos · ligne 1 : marche · ligne 2 : attaque · ligne 3 : touché puis mort (3 images)
Chaque case est découpée telle quelle puis toutes sont recadrées sur le MÊME rectangle,
ce qui garde le perso immobile d'une image à l'autre (pas de tremblement).
hauteur = hauteur de la silhouette au repos en pixels "écran x2" (le jeu dessine à la moitié).
Affiche la ligne à coller dans ANIM (index.html).
"""
import sys, os
from PIL import Image
import numpy as np
from scipy import ndimage as nd

def load(path):
  a = np.array(Image.open(path).convert('RGBA'))
  if (a[..., 3] < 40).mean() < .2:  # fond opaque : on retire le blanc relié aux bords
    wh = a[..., :3].min(-1) > 235
    lab, _ = nd.label(wh)
    b = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    a[np.isin(lab, list(b)), 3] = 0
  a[..., 3] = np.where(a[..., 3] < 40, 0, a[..., 3])
  return a

if __name__ == '__main__':
  path, name, H = sys.argv[1], sys.argv[2], int(sys.argv[3])
  R, C = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (4, 4)
  a = load(path); h, w = a.shape[:2]; ch, cw = h / R, w / C
  cells = [[a[round(r * ch):round((r + 1) * ch), round(c * cw):round((c + 1) * cw)] for c in range(C)] for r in range(R)]
  # rectangle commun à toutes les cases
  y0 = x0 = 10 ** 9; y1 = x1 = 0
  for row in cells:
    for c in row:
      ys, xs = np.nonzero(c[..., 3] > 0)
      if len(ys): y0, y1, x0, x1 = min(y0, ys.min()), max(y1, ys.max()), min(x0, xs.min()), max(x1, xs.max())
  # échelle d'après la silhouette au repos (case 0,0)
  ys, xs = np.nonzero(cells[0][0][..., 3] > 0); idleH = ys.max() - ys.min() + 1
  s = H / idleH
  # point d'ancrage = milieu des pieds au repos
  foot = xs[ys >= ys.max() - idleH * .12]; ax = (foot.mean() - x0) / (x1 - x0 + 1); ay = (ys.max() - y0 + 1) / (y1 - y0 + 1)
  os.makedirs(f'img/a/{name}', exist_ok=True)
  W2, H2 = round((x1 - x0 + 1) * s), round((y1 - y0 + 1) * s)
  for r, row in enumerate(cells):
    for c, cell in enumerate(row):
      im = Image.fromarray(cell[y0:y1 + 1, x0:x1 + 1]).resize((W2, H2), Image.LANCZOS)
      im.save(f'img/a/{name}/{r}{c}.webp', quality=92)
  print(f"  {name}:{{w:{W2},h:{H2},ax:{ax:.3f},ay:{ay:.3f}}},")
