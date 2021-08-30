import numpy as np

def lmtoarr(lmdict):
    return np.array(list(lmdict.values()))

# W= point of wrist
# I= point of indextip
# P= point of pinky tip

def createVector(V1,V2):
    return np.array([V1[0]-V2[0],V1[1]-V2[1],V1[2]-V2[2]])

def cross(W,I,P):
    WI= createVector(W,I)
    WP= createVector(W,P)
    #print(WI,WP)
    return np.cross(WI,WP)

