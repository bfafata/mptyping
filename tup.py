
from calc import lmtoarr,cross
import numpy as np
width=640
height=480

def tupl(landmarkdict):
  return (int(landmarkdict["x"]*width),int(landmarkdict["y"]*height))

def tupendNorm(landmark1,landmark2,landmark3):
  scalar=1000000
  l1=lmtoarr(landmark1)
  l2=lmtoarr(landmark2)
  l3=lmtoarr(landmark3)
  r=cross(l1,l2,l3)
  s=np.sum(r)
  # r[0]*(x-landmark1["x"])-(4)
  #print(r)
  return (int(landmark1["x"]*r[0]*scalar/-s),int(landmark1["y"]*r[1]*scalar/-s))
  


def tuplineVert1(landmarkdict):
  return (int(landmarkdict["x"]*width),0)
def tuplineVert2(landmarkdict):
  return (int(landmarkdict["x"]*width),int(height))