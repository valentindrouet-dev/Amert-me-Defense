"""Découpe d'une planche d'animation en grille (une ligne = une animation) pour Les Nuits de Lamuline.

Usage :
  python3 tools/anim.py planche.png nom hauteur [lignes colonnes [planche]]
    -> img/a/<nom>/<planche><r><c>.webp  (r = ligne, c = colonne, à partir de 0 ; planche = préfixe, vide par défaut)

Format de planche attendu (prompt dans docs/prompts-sprites.md) : 4 lignes x 4 colonnes, cases égales,
fond transparent (un fond blanc uni est retiré automatiquement), perso tourné vers la droite.
  ligne 0 : repos · ligne 1 : marche · ligne 2 : attaque · ligne 3 : touché puis mort (3 images)
Les cases sont coupées au milieu des espaces vides, puis chaque image est calée sur ses pieds
dans un rectangle commun : le perso ne tremble pas d'une image à l'autre.
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

def cuts(m, axis, n):
  """Coupe au milieu de la bande vide la plus proche de chaque limite régulière (grilles un peu irrégulières)."""
  prof = m.any(axis=axis); L = len(prof); out = [0]
  for k in range(1, n):
    b = round(k * L / n); best = None
    for x in range(max(1, b - L // n // 2), min(L - 1, b + L // n // 2)):
      if prof[x]: continue
      x0 = x
      while x0 > 0 and not prof[x0 - 1]: x0 -= 1
      x1 = x
      while x1 < L - 1 and not prof[x1 + 1]: x1 += 1
      c = (x0 + x1) // 2
      if best is None or abs(c - b) < abs(best - b): best = c
    out.append(best if best is not None else b)
  out.append(L); return out

if __name__ == '__main__':
  path, name, H = sys.argv[1], sys.argv[2], int(sys.argv[3])
  R, C = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (4, 4)
  P = sys.argv[6] if len(sys.argv) > 6 else ''
  a = load(path); h, w = a.shape[:2]
  ys_, xs_ = cuts(a[..., 3] > 0, 1, R), cuts(a[..., 3] > 0, 0, C)
  cells = [[a[ys_[r]:ys_[r + 1], xs_[c]:xs_[c + 1]] for c in range(C)] for r in range(R)]
  # chaque image est calée sur ses pieds (bas de la silhouette, milieu des appuis) : pas de tremblement
  info = []
  for row in cells:
    for cell in row:
      ys, xs = np.nonzero(cell[..., 3] > 0)
      if not len(ys): info.append(None); continue
      hh = ys.max() - ys.min() + 1; foot = xs[ys >= ys.max() - hh * .12]
      info.append((cell, foot.mean(), ys.max(), xs.min(), xs.max(), ys.min()))
  i0 = info[0]; idleH = i0[2] - i0[5] + 1; s = H / idleH
  L_ = max(x[1] - x[3] for x in info if x); Rr = max(x[4] - x[1] for x in info if x); U_ = max(x[2] - x[5] for x in info if x)
  CW, CH = int(L_ + Rr + 3), int(U_ + 3)
  os.makedirs(f'img/a/{name}', exist_ok=True)
  W2, H2 = round(CW * s), round(CH * s); ax = (L_ + 1) / CW; ay = (U_ + 1) / CH
  k = 0
  for r, row in enumerate(cells):
    for c, cell in enumerate(row):
      x = info[k]; k += 1; cv = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
      if x: cv.paste(Image.fromarray(cell), (int(round(L_ + 1 - x[1])), int(U_ + 1 - x[2])), Image.fromarray(cell))
      cv.resize((W2, H2), Image.LANCZOS).save(f'img/a/{name}/{P}{r}{c}.webp', quality=92)
  print(f"  planche '{P}' : {{w:{W2},h:{H2},ax:{ax:.3f},ay:{ay:.3f}}}")
