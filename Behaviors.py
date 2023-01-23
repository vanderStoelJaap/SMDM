import Features
from Representation import Shape
from shapely.affinity import scale
from Functions import Functions as fun
import time as t
""" 
This class contains all semantic behaviors and create behavior objects.
A better coupling of data between behavior and features has to be made.
"""

#SETTINGS
Woppvel = 0.8
avoidOppDiameter = 1.2
avoidOppForShotDiameter = 0.5
avoidPeerDiameter = 0.8
fv = 0.5

DRIBBLEDIAM = 3
MINPASSDIST= 3

DRIBBLEREGION = None
INFLUENCEDIST = 15.0

class Behavior:
  all = {}

  def __init__(self, shape, pos, peer = None, shape2 = None):
    self.pos = pos
    self.peer = peer
    self.type = self.__class__.__name__
    self.ntype = -1
    self.shape = shape
    self.opponentsToGoal = 0
    self.shape2 = shape2
    if self.type in Behavior.all:
      Behavior.all[self.type].append(self)
    else:
      Behavior.all[self.type] = [self]

  def __repr__(self) -> str:
    return self.type

  def delete(self):
    Behavior.all[self.type].remove(self)
    del self

  def clear(): 
    Behavior.all.clear()

  @classmethod
  def get(cls):
    name = cls.__name__
    if name in Behavior.all:
      return Behavior.all[name]
    else:
      return []

class avoidopp(Behavior): 
  def __init__(self, shape, pos = None, avoidForShot = None):
    super().__init__(shape, pos, None, avoidForShot) 

class avoidpeer(Behavior): 
  def __init__(self, shape, pos = None, peerlab = None):
    super().__init__(shape, pos, peerlab) 

class shot(Behavior): 
  def __init__(self, shape, pos = None):
    super().__init__(shape, pos)
    self.ntype = 0

class Pass(Behavior): 
  def __init__(self, shape, pos = None, peer = None):
    super().__init__(shape, pos, peer)
    self.ntype = 1

class dribble(Behavior):
  def __init__(self, shape, pos = None):
    super().__init__(shape, pos)
    self.ntype = 2
    self.infuenceregion = None

class move(Behavior):
  def __init__(self, shape, pos = None):
    super().__init__(shape, pos)
    self.ntype = 3

def inField(shape): 
  return Shape.intersection(Features.field.shape, shape)

"""Put circle (update for eclipse) around opponent which has to be avoided """
def avoidOpponent(opponentList):
  for opponent in opponentList:
    vel = [i*Woppvel for i in opponent.vel]
    shape = Shape.ellipse(opponent.pos, avoidOppDiameter, vel, fv)
    shapeForShot = Shape.circle(opponent.pos, avoidOppForShotDiameter)
    avoidopp(
      shape, opponent.pos, shapeForShot
    )

def avoidPeer(peerList): 
  for peer in peerList:
    vel = [i*fv for i in peer.vel]
    shape = Shape.ellipse(peer.pos, avoidPeerDiameter, vel, fv)
    avoidpeer(
      shape, peer.pos
    )

"""Put circle around peer to indicate locations for which a pass can be given to that peer """
def givePass(me, peers):
  time = t.time()
  peerList = peers
  for peer in peerList:
    if Shape.distance(me.pos, peer.pos) > MINPASSDIST:
      radius = fun.calculatePassRadius(me, peer, fv)
      shape = Shape.ellipse(peer.pos, radius, peer.vel, fv)
      shape = inField(shape)
      action = Pass(
        shape, None, peer
      )
      pos = fun.passPoint(action)
      action.pos = pos

    checkReachability()
    checkPassLine(me)

def makeDribble(me): 
  global DRIBBLEREGION
  if (DRIBBLEREGION == None) or (not Shape.intersect(Shape.point(me.pos), DRIBBLEREGION)):
    shape = Shape.circle(me.pos, DRIBBLEDIAM)
    DRIBBLEREGION = inField(shape)
  
  dribble(DRIBBLEREGION, me.pos)

  divideForwardBackward(me)
  dodgeOpponent(me)

def makeShot(me, field): 
  oppGoal = field.oppGoal
  if Shape.distance(me.pos, field.goalpos) < 1/2 * field.fieldLength:
    shot(oppGoal, [0, field.fieldLength/2])
    checkShot(me)
  
"""
Check if no player (only opponents for now) is blocking a pass line. 
Covex hull of the pass region around a peer with the ball position is taken. 
If intersection the pass region is reshaped by taking the tangent lines (by use of convex hull) to the avoid region of the opponent
"""
def checkPassLine(me):
  passList = Pass.get()
  avoidList = avoidopp.get()
  for action in passList:
    availableRegions = fun.freeLine(me.pos, action.shape, avoidList)
    if availableRegions == None: 
      Behavior.delete(action)
    else: 
      for i, region in enumerate(availableRegions):
        if i == 0: 
          action.shape = region
          action.pos = fun.passPoint(action)
        else:      
          action = Pass(region, None, action.peer) 
          action.pos = fun.passPoint(action)

""" 
Check if a possible pass is closer to the receiver than to any opponent by use of a voronoi diagram 
"""
def checkReachability():
  points = []
  passList = Pass.get()
  for action in passList:
    points.append(action.peer.pos)
  avoidList = avoidopp.get()
  for avoidOpp in avoidList:
    points.append(avoidOpp.pos)
  
  voronoi = fun.voronoi(points)
  for action in passList:
    fun.reachable(action, voronoi)

def checkDribble ():   
  actionList = dribble.get()
  avoidList = [*avoidopp.get(), *avoidpeer.get()]
  
  for action in actionList:
    dribbleRegions = fun.avoid(action, avoidList)
    for i, region in enumerate(dribbleRegions):
      if i == 0: 
        action.shape = region
        action.pos = Shape.representativePoint(action.shape)

      else:       
        action =  dribble(region, None) 
        action.pos = Shape.representativePoint(action.shape)
  
def checkShot(me):
  action = shot.get()[0]
  avoidList = [*avoidopp.get(), *avoidpeer.get()]
  availableRegions = fun.freeLine(me.pos, action.shape, avoidList)    
  if availableRegions == None: 
    Behavior.delete(action)
  else: 
    for i, region in enumerate(availableRegions):
      if i == 0: 
        action.shape = region
        action.pos = Shape.representativePoint(action.shape)
      else:       
        action = shot( region, None)    
        action.pos = Shape.representativePoint(action.shape)

def dodgeOpponent(me):
  actionList = dribble.get()
  avoidList = avoidopp.get()
  for action in actionList:
      availableRegions = fun.freeSpace(me.pos, action, avoidList, INFLUENCEDIST)
      if availableRegions == None:
        Behavior.delete(action)
      else:
        for i, region in enumerate(availableRegions):
          if i == 0: 
            action.shape = region
            action.pos = Shape.representativePoint(action.shape)
          else:      
            action = dribble(region, None) 
            action.pos = Shape.representativePoint(action.shape)

def divideForwardBackward(me):
  actionList = dribble.get()

  #create line perpendicular from me to score pos
  line = Shape.perpLine(me.pos, Features.field.penaltySpot)
  bufline = Shape.buffer(line, 0.05)
  #if intersect then split region 
  for action in actionList: 
    actionRegion = action.shape
    try:
      if actionRegion.intersects(line):
        regions =actionRegion.difference(bufline)
        for i, region in enumerate(regions):
          if i == 0:
            action.shape = region
            action.pos = Shape.representativePoint(action.shape)
          else:
            action = dribble(region, None)
            action.pos = Shape.representativePoint(action.shape)
    except: 
      print(f"The dribble region is not defined properly -> type: {type(action)} region: {actionRegion}")