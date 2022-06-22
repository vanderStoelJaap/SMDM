from typing_extensions import Self
import Input
from Input import Feature, Opponent, Peer, Ball
from Representation import Shape
from Settings import Settings
import shapely.geometry as geom
from shapely.geometry import Point, MultiPoint, asMultiPoint, LineString
import numpy as np
from shapely.affinity import scale
import time

  #ELEMENTARY BEHAVIORS
avoid = {"id" : "avoid"}
noEnter = {"id" : "noEnter"} # Necessary? 
avoidPass = {"id" : "avoidPass"} #Necessary? 
move = {"id" : "Move"}
dribble = {"id" : "Dribble"}
humanDribble = {"id" : "HumanDribble"}
shoot = {"id" : "Shoot"}
givePass = {"id" : "Pass"}
target = {"id" : "Target"} # Necessary? 

class Behavior:

  all = []

  def __init__(self, shape, label = None, center = None):
    self.shape = shape
    self.center = center
    self.label = label 

    Behavior.all.append(self)
    
  def delete(self): 
      print("Hello i'm a behavior to be deleted")
      Behavior.all.remove(self)
      for behavior in Behavior.all: 
        if behavior.label == "pass":
          print("I'm a pass behavior")
      del self

  #Put circle (update for eclipse) around opponent which has to be avoided
  def avoidOpponent():
    label = "avoid"
    for opponent in Opponent.all:
        shape = Shape.circle(opponent.pos, Settings.AvoidOpponent)
        Behavior(
          shape, label, opponent.pos
        )

  #Put circle around peer to indicate locations for which a pass can be given to that peer
  def givePass():
    label = "pass"

    for peer in Peer.all:
      if peer.role != "Main":
        #print(f"Pass region for peer with label: {peer.lab}")
        shape = Shape.circle(peer.pos, Settings.Pass)
        Behavior(
          shape, label, peer.pos
        )

  #Put a convex hull around "givePass" area and ball pos to check wether a pass can be given 
  def checkPassLine():
    label = "checkPassLine"
   
    ballPos = Ball.all[0].pos
    
    for givePass in Behavior.all:
      if givePass.label == "pass":
        for avoid in Behavior.all: 
          if avoid.label == "avoid":
            region = givePass.shape
            #print(f"------------------------ i'm type {type(region)} wiht label {givePass.label}")
            region = region.exterior
            region = region.coords
            checkPass = Shape.convexHull(list(ballPos), list(region))
            #print(f"checkPass of type {type(checkPass)}")
            #print(f"avoid.shape of type {type(avoid.shape)}")
            if Shape.intersect(checkPass, avoid.shape) or Shape.cover(checkPass, avoid.shape):
              extra_buffer = avoid.shape.buffer(0.001)
              avoid_ch = Shape.convexHull(list(ballPos), list(extra_buffer.exterior.coords))
              avoid_ch = list(avoid_ch.exterior.coords)
              leftline = LineString([avoid_ch[0], avoid_ch[1]])
              rightline = LineString([avoid_ch[0], avoid_ch[-2]])
              lines = [leftline, rightline]
              #print(f"AVOID INTERSECTS REGION having lines {lines[0]} and {lines[1]}") 
              for line in lines: 
                if Shape.cover(checkPass, line):
                  scaled_line = scale(line, 10,10)
                  #Behavior(
                  #  scaled_line, "line", None
                  #)
                  #print(f"line with shape {line} created")
                  newReg = Shape.reshape(checkPass , givePass.shape, scaled_line, avoid.shape)
                  #print(f"this is a newRegion of type {type(newReg[0])} shape {print(newReg[0])} and length {len(newReg)}")
                  if len(newReg) > 1:
                    #print("-------------------------------------HELLO --------------------------------")
                    givePass.shape = newReg[0]
                    #print(f"--------------------------TYPE TYPE TYPE OF THE NEWREGION IS : {type(givePass.shape)}")
                    Behavior(
                      newReg[1], "pass", None
                    )
                  elif len(newReg) == 1:
                    givePass.shape = newReg[0]
                    #print(f"--------------------------TYPE TYPE TYPE OF THE NEWREGION IS : {type(givePass.shape)}")

                  #print(f"intersection found with {avoid.label} having centerpoint {avoid.center}")
                  
            #else: 
              #print("pass is valid")

 

   #  SEMANTIC REGIONS SHOULD BE COUPLED TO A PEER !!!!!! 
  def checkReachability ():

    label = "Dist"

    for peer in Peer.all:
      points = []
      if peer.role != "Main":
        points.append(peer.pos)

        for avoid in Behavior.all:
          if avoid.label == "avoid":
            points.append(avoid.center)
        #print(f"---------- wE HAVE NOW THE FOLLOWING POINTS !!! ------------- {points}")
        points = geom.MultiPoint(points)
        reachability = Shape.voronoi(points)
        #print(reachability)
        for region in reachability: 
          #print(region)
          if Shape.intersect(geom.Point(peer.pos), region):
            for behavior in Behavior.all:
              if behavior.label == "pass" and Shape.intersect(behavior.shape, region):
                newReg = Shape.intersection(behavior.shape, region)
                if newReg:
                  behavior.shape = newReg

Behavior.avoidOpponent()
Behavior.givePass()
Behavior.checkPassLine()
Behavior.checkReachability()

print("--- %s seconds ---" % (time.time() - Input.start_time))