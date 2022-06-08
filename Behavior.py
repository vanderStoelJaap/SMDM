from typing_extensions import Self
from Input import Feature, Opponent, Peer, Ball
from Representation import Shape
from Settings import Settings
import numpy as np

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

  #Put circle (update for eclipse) around opponent which has to be avoided
  def avoidOpponent():
    label = "avoidOpponent"
    for opponent in Opponent.all:
        shape = Shape.circle(opponent.pos, Settings.AvoidOpponent)
        Behavior(
          shape, label, opponent.pos
        )

  #Put circle around peer to indicate locations for which a pass can be given to that peer
  def givePass():
    label = "pass"

    for peer in Peer.all:
      if peer.lab != "Main":
        shape = Shape.circle(peer.pos, Settings.Pass)
        Behavior(
          shape, label, peer.pos
        )

  #Put a convex hull around "givePass" area and ball pos to check wether a pass can be given 
  def checkPassLine():
    label = "checkPassLine"
   
    ballPos = Ball.all[0].pos

    for behavior in Behavior.all:
      if behavior.label == "pass":
        shape = Shape.convexHull(list(ballPos), list(behavior.shape.exterior.coords))
        Behavior(
          shape, label, None
        ) 

    #for behavior in Behavior.all: 
    #  if behavior.label == "avoidOpponent":
    #    if Shape.intersect(shape, behavior.shape):
          


Behavior.avoidOpponent()
Behavior.givePass()
Behavior.checkPassLine()