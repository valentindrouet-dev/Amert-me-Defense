"""Découpe des planches de sprites (fond transparent) pour Les Nuits de Lamuline.

Usage :
  python3 tools/sprites.py units  planche.png nom1:hauteur nom2:hauteur ...   -> img/u/<nom>_{idle,w1,w2,atk}.webp (1 ligne par unité)
  python3 tools/sprites.py mons   planche.png nom1:hauteur ...                -> img/m/<nom>_{w1,w2,atk,dead}.webp + _rim (1 ligne par monstre)
  python3 tools/sprites.py bld    planche.png nom1:largeur ...                -> img/b/<nom>.webp (ordre de lecture gauche->droite, haut->bas)
  python3 tools/sprites.py icons  planche.png cols rows nom1 nom2 ...          -> img/i/<nom>.webp 128x128 avec halo
  python3 tools/sprites.py fx     planche.png nom1 nom2 ...                    -> img/fx/<nom>.webp bandes de 6 frames 128x128 (grille 6 colonnes)
Hauteur/largeur en pixels "écran x2" (les sprites sont dessinés à la moitié de leur taille).
"""
import sys
from PIL import Image
import numpy as np
from scipy import ndimage as nd

def frames(path):
  a=np.array(Image.open(path).convert('RGBA'));m=a[...,3]>40
  lab,_=nd.label(nd.binary_dilation(m,iterations=6))
  bx=[(s[0].start,s[1].start,s[0].stop,s[1].stop) for s in nd.find_objects(lab) if (s[0].stop-s[0].start)*(s[1].stop-s[1].start)>2000]
  bx.sort(key=lambda b:(b[0]+b[2])/2);rows=[]
  for b in bx:
    c=(b[0]+b[2])/2
    if rows and abs(c-rows[-1][0])<120:rows[-1][1].append(b)
    else:rows.append([c,[b]])
  out=[]
  for _,r in rows:
    r.sort(key=lambda b:b[1]);fr=[]
    for (y0,x0,y1,x1) in r:
      sub=a[y0:y1,x0:x1].copy();lb=lab[y0:y1,x0:x1];ids,cnt=np.unique(lb[lb>0],return_counts=True)
      sub[lb!=ids[np.argmax(cnt)]]=0;sub[...,3]=np.where(sub[...,3]<40,0,sub[...,3]);im=Image.fromarray(sub);fr.append(im.crop(im.getbbox()))
    out.append(fr)
  return out

def rim(img,col=(244,211,131),dark=(24,8,0),pad=3):
  w,h=img.size;c=Image.new('RGBA',(w+2*pad,h+2*pad),(0,0,0,0));c.paste(img,(pad,pad))
  a=np.array(c);m=a[...,3]>90;d1=nd.binary_dilation(m,iterations=1);d2=nd.binary_dilation(m,iterations=2);o=a.copy()
  o[d1&~m]=[*dark,255];o[d2&~d1]=[*col,240];return Image.fromarray(o)

def scale(f,s):return f.resize((max(1,round(f.size[0]*s)),max(1,round(f.size[1]*s))),Image.LANCZOS)

if __name__=='__main__':
  mode,path=sys.argv[1],sys.argv[2];args=sys.argv[3:]
  if mode in('units','mons'):
    poses=['idle','w1','w2','atk'] if mode=='units' else ['w1','w2','atk','dead']
    for fr,spec in zip(frames(path),args):
      n,t=spec.split(':');s=int(t)/fr[0].size[1]
      for p,f in zip(poses,fr):
        f=scale(f,s)
        if mode=='units':rim(f).save(f'img/u/{n}_{p}.webp',quality=92)
        else:
          f.save(f'img/m/{n}_{p}.webp',quality=92)
          if p!='dead':rim(f,(179,78,58),(58,0,0),4).save(f'img/m/{n}_{p}_rim.webp',quality=92)
  elif mode=='bld':
    fs=[f for r in frames(path) for f in r]
    for f,spec in zip(fs,args):n,w=spec.split(':');scale(f,int(w)/f.size[0]).save(f'img/b/{n}.webp',quality=92)
  elif mode=='icons':
    ic=Image.open(path).convert('RGBA');W,H=ic.size;cols,rows=int(args[0]),int(args[1])
    for k,n in enumerate(args[2:]):
      r,c0=divmod(k,cols);c=ic.crop((int(c0*W/cols),int(r*H/rows),int((c0+1)*W/cols),int((r+1)*H/rows)));c=c.crop(c.getbbox());c=scale(c,112/max(c.size))
      cv=Image.new('RGBA',(128,128),(0,0,0,0));cv.paste(c,((128-c.size[0])//2,(128-c.size[1])//2),c)
      al=np.array(cv)[...,3].astype(float);hl=np.zeros((128,128,4),np.uint8);hl[...,:3]=(255,226,170);hl[...,3]=np.clip(nd.gaussian_filter(al,4)*.45,0,255).astype(np.uint8)
      Image.alpha_composite(Image.fromarray(hl),cv).save(f'img/i/{n}.webp',quality=92)
  elif mode=='fx':
    im=Image.open(path).convert('RGBA');W,H=im.size;rh=H/len(args);cw=W/6
    for r,n in enumerate(args):
      st=Image.new('RGBA',(768,128),(0,0,0,0))
      for c in range(6):
        cell=np.array(im.crop((int(c*cw),int(r*rh),int((c+1)*cw),int((r+1)*rh))).resize((128,128),Image.LANCZOS)).astype(float)
        cell[...,3]=np.clip((cell[...,3]-20)*255/235,0,255);st.paste(Image.fromarray(cell.astype(np.uint8)),(c*128,0))
      st.save(f'img/fx/{n}.webp',quality=90)
