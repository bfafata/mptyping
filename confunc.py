import mediapipe as mp
def listToNLL(list):
  c= mp.framework.formats.landmark_pb2.NormalizedLandmarkList()
  for landmark in list:
    d=mp.framework.formats.landmark_pb2.NormalizedLandmark()
    d.x=landmark["x"]
    d.y=landmark["y"]
    d.z=landmark["z"]
    c.landmark.append(d)
  return c

def NLLToList(nll):
  locnll=nll.__deepcopy__()
  landmarkTypeList=[]
  resultList=[]
  while len(locnll.landmark)!=0:
    lm=locnll.landmark.pop()
    landmarkTypeList.append(lm)
  for lm in landmarkTypeList:
    d={}
    d["x"]=lm.x
    d["y"]=lm.y
    d["z"]=lm.z
    resultList.append(d)
  return resultList[::-1]