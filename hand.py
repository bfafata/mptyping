
from numpy.lib.scimath import log10
from calc import lmtoarr
import mediapipe as mp
import cv2
import math
from printlandmarks import pl
from calc import cross

import numpy as np
from confunc import listToNLL,NLLToList
from tup import tupl,tupendNorm,tuplineVert1,tuplineVert2
import json
import os
import path
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands



font                    = cv2.FONT_HERSHEY_SIMPLEX
topLeftCornerOfFrame    = (30,30)
topRightCornerOfFrame   = (300,30)
bottomLeftCornerOfFrame = (10,450)
fontScale               = 1
fontColorWhite          = (255,255,255)
fontColorRed            = (255,0,0)
fontColorBlue           = (0,0,255)
lineType                = 2

frameWithHand=0

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
fps =  int(cap.get(cv2.CAP_PROP_FPS))

bufferlen=5

prev=[]
def avgnll(listofnll):
  global nllprev
  res=[]
  for i in range(21):
    res.append({"x":0,"y":0,"z":0})
  for nll in listofnll:
    index=0
    lml=NLLToList(nll)
    for lm in lml:
      res[index]["x"]+=lm["x"]
      res[index]["y"]+=lm["y"]
      res[index]["z"]+=lm["z"]
      index+=1
  for i in range(21):
    res[i]["x"]= res[i]["x"]/bufferlen
    res[i]["y"]= res[i]["y"]/bufferlen
    res[i]["z"]= res[i]["z"]/bufferlen
  return listToNLL(res)
def addtofixedlist(list,item,listlength):
  global prev
  resultlist=[]
  if len(list)<listlength:
    resultlist=list+[item]
    prev=resultlist
  if len(list)==listlength:
    resultlist=[item]+list[:listlength-1]
    prev=resultlist

class snapshot:
  def __init__(self,logfile:str):
    self.logfile=logfile
    print("snapshot taken")
  def write(self,content:dict):
    with open(f"{self.logfile}.json",'w') as log:
      json.dump(content,log)
    return
  def retrieve(self):
    with open(f"{self.logfile}.json",'r') as log:
      return json.loads(log.read())

class plane:
  def __init__(self,a,b,c,d):
    self.a=a
    self.b=b
    self.c=c
    self.d=d
  def findFromLandmarks(self,landmark1,landmark2,landmark3):
    scalar=1000000

    l1=lmtoarr(landmark1)
    l2=lmtoarr(landmark2)
    l3=lmtoarr(landmark3)

    r=cross(l1,l2,l3)
    self.a=r[0]
    self.b=r[1]
    self.c=r[2]
    self.d=r[0]*l1[0]+r[1]*l1[1]+r[2]*l1[2]
    return
  def __repr__(self):
    return(f"{self.a},{self.b},{self.c},{self.d}")

newsurface=plane(0,0,0,0)
def establishSurface(lm1,lm2,lm3):
  newsurface.findFromLandmarks(lm1,lm2,lm3)
  print("surface established")
  return


with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if not results.multi_hand_landmarks:
      prev=[]
    if results.multi_hand_landmarks:
      frameWithHand+=1
      addtofixedlist(prev,results.multi_hand_landmarks[0],bufferlen)
      buffedlist=avgnll(prev)
      if len(prev)==bufferlen:
        for hand_landmarks in results.multi_hand_landmarks: #hand_landmarks is a list of hands, and the list of actual points is of type NormalizedLandmarkList 
          mp_drawing.draw_landmarks(
              image, buffedlist)
      landmarks=NLLToList(buffedlist)
      wrist=landmarks[0]
      thumbtip=landmarks[4]
      pinkytip=landmarks[20]
      #print(tup(thumbtip),tup(pinkytip))
      #cv2.rectangle(image,tup(thumbtip),tup(pinkytip), fontColorBlue)
      base=tupl(wrist)
      tip=tupendNorm(wrist,thumbtip,pinkytip)
      #print(f"base {base}, tip {tip}")
      cv2.line(image,base,tip, fontColorBlue)
  
    cv2.putText(image,str(frameWithHand),topRightCornerOfFrame, font, fontScale,fontColorWhite,lineType)
    cv2.putText(image,str(fps),topLeftCornerOfFrame, font, fontScale,fontColorRed,lineType)
    cv2.imshow('MediaPipe Hands', image)
    
    if cv2.waitKey(5) & 0xFF == ord("e"):
      establishSurface(wrist,thumbtip,pinkytip)

    if cv2.waitKey(5) & 0xFF == ord("w"):
      snaptest= snapshot("test")
      snaptest.write(NLLToList(buffedlist)[1])

    if cv2.waitKey(5) & 0xFF == ord("q"):
      break
cap.release()
#cv2.destroyAllWindows()

#z values
#relitive to wrist
#pos = further away from camera
#neg = closer to camera