import Features
from Features import Feature
from Representation import Shape
import Settings
import shapely.geometry as geom
from shapely.geometry import LineString
from shapely.affinity import scale

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
      shape = Shape.circle(opponent.pos, Settings.AvoidOpponent)
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
    givePassList = Behavior.getBehavior('pass')
    avoidList =  Behavior.getBehavior('avoid')
    for givePass in givePassList:
      givePass_ex = givePass.shape.exterior.coords   
      givePass_ch = Shape.convexHull(list(ballPos), list(givePass_ex))       
   
      for avoid in avoidList:
        if Shape.intersect(givePass_ch, avoid.shape) or Shape.cover(givePass_ch, avoid.shape):
          buffer = avoid.shape.buffer(0.05)
          avoid_ch = Shape.convexHull(list(ballPos), list(buffer.exterior.coords))
          avoid_ex = avoid_ch.exterior.coords
          lines = [LineString([avoid_ex[0], avoid_ex[1]]), LineString([avoid_ex[0], avoid_ex[-2]])]

          scaled_lines = []

          for line in lines: 
            scaled_line = scale(line, 10,10)
            if Shape.intersect(givePass.shape, scaled_line):
              scaled_lines.append(scaled_line)
              #Behavior(line, 'line') 

          newReg = Shape.reshape(givePass_ch , givePass.shape, scaled_lines, avoid.shape)
          for i, region in enumerate(newReg):
            if i == 0: 
              givePass.shape = region
            else:
              Behavior(
                region, "pass", None, givePass.feature)
  

  """ 
  Check if a possible pass is closer to the receiver than to any opponent by use of a voronoi diagram 
  """
  def checkReachability ():

    type = "Dist"

    points = []

    peerList = Feature.getFeature('Peer', 'assist')
    for peer in peerList:
      points.append(peer.pos)
      avoidList = Behavior.getBehavior('avoid')

    for avoid in avoidList:
      points.append(avoid.center)
    points = geom.MultiPoint(points)
    reachability = Shape.voronoi(points)
    
    for region in reachability: 
      if Shape.intersect(geom.Point(peer.pos), region):
        for behavior in Behavior.all:
          # rewrite !! 
          if behavior.type == "pass" and behavior.feature == peer.lab:
            newReg = Shape.intersection(behavior.shape, region)
            #otherReg = list(Shape.difference(behavior.shape, region))
            if newReg:
              behavior.shape = newReg
              #Behavior(otherReg[0], "reach")
              #Behavior(otherReg[1], "reach")

  def dribble (): 
    type = "dribble"
    
    me = Feature.getFeature('Self', None)
    me = me[0]
    Behavior(Shape.circle(me.pos, 3), type, me.pos)
 
  def checkDribble (): 
    
    dribble = Behavior.getBehavior('dribble')[0]
    avoidRegions = Behavior.getBehavior('avoid')
    for avoid in avoidRegions:
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

    avoidRegions = Behavior.getBehavior('avoid')
    for avoid in avoidRegions: 
      shot_ch = Shape.convexHull(list(ballPos), list(shot.shape.exterior.coords))

      if Shape.intersect(shot_ch, avoid.shape) or Shape.cover(shot_ch, avoid.shape):
        extra_buffer = avoid.shape.buffer(0.001)
        avoid_ch = Shape.convexHull(list(ballPos), list(extra_buffer.exterior.coords)).exterior.coords

        lines = [LineString([avoid_ch[0], avoid_ch[1]]), LineString([avoid_ch[0], avoid_ch[-2]])]    
        
        scaled_lines = []
        for line in lines:          
          scaled_line = scale(line, 10,10)               
          if Shape.intersect(shot.shape, scaled_line):
            scaled_lines.append(scaled_line)
            #Behavior(line, 'line') 
        
        newReg = Shape.reshape(shot_ch , shot.shape, scaled_lines, avoid.shape)
 
        for i, region in enumerate(newReg):
          if i == 0: 
            shot.shape = region
          else:
            Behavior(
              region, "pass", None, shot.feature)