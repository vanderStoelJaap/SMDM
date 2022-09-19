from dataclasses import Field
import Features
from Features import Feature
from Representation import Shape
import Settings
import shapely.geometry as geom
from shapely.geometry import LineString
from shapely.affinity import scale
import shapely.ops as geomops
from Functions import Functions as fun

""" 
This class contains all semantic behaviors and create behavior objects.
A better coupling of data between behavior and features has to be made. 
"""

class Behavior:

  all = []

  def __init__(self, shape, type = None, center = None, feature = None):
    self.shape = shape
    self.center = center
    self.type = type
    self.feature = feature

    Behavior.all.append(self)

  def delete(self):
    print(f"behavior {self} removed")
    Behavior.all.remove(self)
    del self

  def getAllBehavior():
    return Behavior.all

  def getBehavior(type): 
    result = []

    for behavior in Behavior.all:
      if behavior.type == type:
        result.append(behavior)
    
    return result 

  """Put circle (update for eclipse) around opponent which has to be avoided """
  def avoidOpponent():
    type = "avoid"

    opponentList = Feature.getFeature('Opponent')

    for opponent in opponentList:
      shape = Shape.ellipse(opponent.pos, Settings.AvoidOpponent, opponent.vel)
      Behavior(
        shape, type, opponent.pos
      )

  """Put circle around peer to indicate locations for which a pass can be given to that peer """
  def givePass():
    type = "pass"

    peerList = Feature.getFeature('Peer', 'assist')
    for peer in peerList:
      shape = Shape.circle(peer.pos, Settings.Pass)
      Behavior(
        shape, type, peer.pos, peer.lab
      )

  """
  Check if no player (only opponents for now) is blocking a pass line. 
  Covex hull of the pass region around a peer with the ball position is taken. 
  If intersection the pass region is reshaped by taking the tangent lines (by use of convex hull) to the avoid region of the opponent
   """
  def checkPassLine():
    type = "checkPassLine"
   
    ballPos = Feature.getFeature('Ball')[0].pos
    passList = Behavior.getBehavior('pass')
    avoidList =  Behavior.getBehavior('avoid')
    for action in passList:
      availableRegions = fun.freeLine(ballPos, action, avoidList)      
      if availableRegions == False: 
        Behavior.delete(action)
      else: 
        for i, region in enumerate(availableRegions):
          if i == 0: 
            action.shape = region
          else:       
            Behavior(
              region, "pass", None, action.feature)  
    

  """ 
  Check if a possible pass is closer to the receiver than to any opponent by use of a voronoi diagram 
  """
  def checkReachability ():

    type = "Dist"

    points = []

    passList = Behavior.getBehavior('pass')
    for action in passList:
      points.append(action.center)
      avoidList = Behavior.getBehavior('avoid')
      for avoid in avoidList:
        points.append(avoid.center)

      reachableRegion = fun.Reachable(action, points)
    
    """    
    points = geom.MultiPoint(points)
    reachability = Shape.voronoi(points)

    peerList = Feature.getFeature('Peer', 'assist')
    
    for region in reachability: 
      if Shape.intersect(geom.Point(peer.pos), region):
        for behavior in Behavior.all:
          # rewrite !! 
          if behavior.type == "pass" and behavior.feature == peer.lab:
            newReg = Shape.intersection(behavior.shape, region)
            otherReg = [Shape.difference(behavior.shape, region)]
            if newReg:
              behavior.shape = newReg
              #Behavior(otherReg[0], "reach")
              #Behavior(otherReg[1], "reach")
    """


  def dribble (): 
    type = "dribble"
    
    me = Feature.getFeature('Self', None)
    me = me[0]
    Behavior(Shape.circle(me.pos, 3), type, me.pos)
 
  def checkDribble (): 
    
    dribble = Behavior.getBehavior('dribble')[0]
    avoidRegions = Behavior.getBehavior('avoid')
    for avoid in avoidRegions:
      type(avoid)
      if Shape.intersect(dribble.shape, avoid.shape): 
        newReg = Shape.difference(dribble.shape, avoid.shape)
        if newReg:
          dribble.shape = newReg
        

  def shot (): 

    goal = Features.oppGoal
    Behavior(goal, "shot")
    

  def checkShot ():
    ballPos = Feature.getFeature('Ball')[0].pos
    shot = Behavior.getBehavior('shot')[0]
    avoidList = Behavior.getBehavior('avoid')

    availableRegions = fun.freeLine(ballPos, shot, avoidList)      
    if availableRegions == False: 
      Behavior.delete(shot)
    else: 
      for i, region in enumerate(availableRegions):
        if i == 0: 
          shot.shape = region
        else:       
          Behavior(
            region, "pass", None, shot.feature)    