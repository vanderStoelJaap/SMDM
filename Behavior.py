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
      print(f"a passing action to peer {action.feature} \n free lines are: ")
      if availableRegions == False: 
        Behavior.delete(action)
        print(f"no free lines found")
      elif availableRegions == None: 
        continue
      elif len(availableRegions) == 0: 
        print(f"region is fully available")
        continue 
      else: 
        for i, region in enumerate(availableRegions):
          if i == 0: 
            action.shape = region
          else:       
            Behavior(
              region, "pass", None, action.feature)  
        print(f"region devided in {i}  accesable regions")  



    '''
      givePass_ex = givePass.shape.exterior.coords   
      givePass_ch = Shape.convexHull(ballPos, list(givePass_ex))       
      #Behavior(givePass_ch, "reach")
   
      for avoid in avoidList:
        if Shape.intersect(givePass_ch, avoid.shape):
          buffer = avoid.shape.buffer(0.05)
          avoid_ch = Shape.convexHull(list(ballPos), list(buffer.exterior.coords))
          avoid_ex = avoid_ch.exterior.coords
          poly = geom.Polygon([avoid_ex[0], avoid_ex[1], avoid_ex[-2], avoid_ex[0]])
          print(f"avoid_ex first point: {avoid_ex[0]}")
          poly = scale(poly, 10, 10, origin=avoid_ex[0])
          Behavior(
            poly, "other", None, givePass.feature)          
          lines = [LineString([avoid_ex[0], avoid_ex[1]]), LineString([avoid_ex[0], avoid_ex[-2]])]
          scaled_lines = []
          #vis_lines = []

          """
          vis_line = Shape.intersection(scaled_line, Features.field)
          balletje = list(ballPos[0])
          vis_line = Shape.difference(vis_line, Shape.circle(balletje, 0.1))
          print(vis_line)
          vis_line = vis_line[1]
          """
          setter = False
          if Shape.contains(poly, givePass.shape):
            print("delete region because pass is not possible ")
            setter = True
          elif Shape.intersect(poly, givePass.shape):
            for line in lines: 
              scaled_line = scale(line, 10,10)
              scaled_lines.append(scaled_line)
            print("I have found an intersection !!!!!!!!!!!!11!!!!!!")
            #vis_lines.append(vis_line)
            #Behavior(vis_line, 'line') 
          else: 
            print(Shape.crosses(poly,givePass.shape))
            print("no intersection between regions")

          if setter == True: 
            Behavior.delete(givePass)
            break

          else: 
            newReg = Shape.reshape(givePass_ch , givePass.shape, scaled_lines, avoid.shape)
            for i, region in enumerate(newReg):
              print("NEW REGION ADJUSTED OR CREATED")
              if i == 0: 
                givePass.shape = region
              else:
                Behavior(
                  region, "pass", None, givePass.feature)
            
          '''
    

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
            otherReg = [Shape.difference(behavior.shape, region)]
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

    avoidRegions = Behavior.getBehavior('avoid')
    for avoid in avoidRegions: 
      shot_ex = shot.shape.exterior.coords
      shot_ch = Shape.convexHull(list(ballPos), list(shot_ex))

      if Shape.intersect(shot_ch, avoid.shape) or Shape.cover(shot_ch, avoid.shape):
        extra_buffer = avoid.shape.buffer(0.001)
        avoid_ch = Shape.convexHull(list(ballPos), list(extra_buffer.exterior.coords)).exterior.coords
        poly = geom.Polygon([shot_ex[0], shot_ex[1], shot_ex[-2], shot_ex[0]])
        poly = scale(poly, 10, 10)
        lines = [LineString([avoid_ch[0], avoid_ch[1]]), LineString([avoid_ch[0], avoid_ch[-2]])]    
        
        scaled_lines = []
        vis_lines = []
        for line in lines:          

          scaled_line = scale(line, 10,10)
          """
          vis_line = Shape.intersection(scaled_line, Features.field)
          balletje = list(ballPos[0])
          vis_line = Shape.difference(vis_line, Shape.circle(balletje, 0.1))
          vis_line = vis_line[1]
          """
          if Shape.intersect(shot.shape, poly):
            scaled_lines.append(scaled_line)
            #vis_lines.append(vis_line)
            #Behavior(vis_line, 'line') 
          elif Shape.cover(poly, shot.shape):
            del shot
        
        newReg = Shape.reshape(shot_ch , shot.shape, scaled_lines, avoid.shape)

        for i, region in enumerate(newReg):
          if i == 0: 
            shot.shape = region
          else:
            Behavior(
              region, "reach", None, shot.feature)
        
        #otherReg = Shape.difference(newReg[0], shot.shape)
        #Behavior(
        #  otherReg, "reach", None, shot.feature)       


        
        