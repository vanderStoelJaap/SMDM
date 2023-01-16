from Representation import Shape
from shapely.geometry import Point, MultiPoint
from shapely.affinity import scale
from shapely.ops import voronoi_diagram
from numpy import sqrt, arctan2
#DEBUG
import matplotlib.pyplot as plt
DEBUG = True

"""
This class contains geometric operations used to constraint the actions
"""

class Functions:

    def avoid(action, objects : list):
        blocked = []
        actionRegion = action.shape
        actionRegions = [actionRegion]

        for avoid in objects:
            avoidRegion = avoid.shape
            if actionRegion.intersect(avoidRegion):
                blocked.append(Shape.buffer(avoidRegion, 0.01))
            
        for region in blocked:
            actionRegions = Shape.differenceMultiPolygon(actionRegions, region)

        return actionRegions
    
    def freeLine(startPos : float, actionRegion, objects : list):
        blocked = []
        startPos_tup = [tuple(startPos)]
        EX_action = actionRegion.exterior.coords[:]
        CH_points = MultiPoint(startPos_tup + EX_action)
        CH_action = CH_points.convex_hull
        for avoid in objects: 
            avoidRegion = avoid.shape
            if CH_action.intersects(avoidRegion):
                EX_avoid = avoidRegion.exterior.coords[:]
                CH_points = MultiPoint(startPos_tup + EX_avoid)
                CH_avoid = CH_points.convex_hull
                SC_CH_avoid = scale(CH_avoid, 10, 10, origin= startPos_tup[0])
                if SC_CH_avoid.contains(actionRegion): 
                    return None
                else:
                    blockedRegion = Shape.buffer(SC_CH_avoid.difference(Shape.buffer(CH_avoid.difference(avoidRegion),0.01)), 0.02)
                    blocked.append(blockedRegion)

                    #DEBUG
                    if DEBUG:
                        print("------------ DEBUG DEBUG DEBUG -----------------")
                        constraint = actionRegion.intersection(blockedRegion)
                        Functions.plotconstraint(constraint, 'red')

        actionRegions = [actionRegion]
        for region in blocked:
            if actionRegions == None:
                break
            actionRegions = Shape.differenceMultiPolygon(actionRegions, region)
        return actionRegions
   
    def voronoi(multipoint: MultiPoint): 
        points = MultiPoint(multipoint)
        return voronoi_diagram(points)

    def passPoint(action):
         target = Functions.caculate_stop_point(action.peer.pos, action.peer.vel)
         region = action.shape
         if region.intersects(Point(target)):
            return target
         else: 
            return Shape.representativePoint(region)

    def caculate_stop_point(pos, vel_vec):
        MAX_ACCELERATION = 4.5
        REACTIONTIME = 1/20
        dx = (0.5 * vel_vec[0]) * (vel_vec[0]/MAX_ACCELERATION + REACTIONTIME)
        dy = (0.5 * vel_vec[1]) * (vel_vec[1]/MAX_ACCELERATION + REACTIONTIME)
        return [pos[0] + dx, pos[1] + dy] 



    def reachable(action, voronoi):
        #print(f"ININTPOS : {action.peerpos}, POS {action.pos}, SHAPE : {action.shape}, type : {action}")
        actionPos = Point(action.peer.pos)
        actionRegion = action.shape
        for region in voronoi:
            if actionPos.intersects(region):
                action.shape = region.intersection(actionRegion)
                action.pos = Functions.passPoint(action)

            #DEBUG
            elif DEBUG & actionRegion.intersects(region):
                constraint = region.intersection(actionRegion)
                Functions.plotconstraint(constraint, 'red')

    def freeSpace(startPos : float, action, objects : list, INFLUNECEDIST):
        blocked = []
        actionRegion = action.shape
        startPos_tup = [tuple(startPos)]
        for avoid in objects: 
            dist = Shape.distance(startPos, avoid.pos)
            if dist < INFLUNECEDIST:
                avoidRegion = avoid.shape
                EX_avoid = avoidRegion.exterior.coords[:]
                CH_points = MultiPoint(startPos_tup + EX_avoid)
                CH_avoid = CH_points.convex_hull
                SC_CH_avoid = scale(CH_avoid, 10, 10, origin= startPos_tup[0])
                blocked.append(SC_CH_avoid)
                
                #DEBUG
                if DEBUG:
                    constraint = actionRegion.intersection(SC_CH_avoid)
                    Functions.plotconstraint(constraint, 'red')                 

        actionRegions = [actionRegion]
        for region in blocked:
            if actionRegions == None:
                break
            actionRegions = Shape.differenceMultiPolygon(actionRegions, region)

            #DEBUG
            #print(f"actionregions: {actionRegions}")
        return actionRegions
    
    def opponentsToGoal(skill, field, objects: list):
        startPos = [tuple(skill.pos)] 
        goal = field.oppGoal
        EX_action = goal.exterior.coords
        CH_action = Shape.convexHull(startPos, EX_action) 
        i = 0
        for object in objects: 
            if Shape.intersect(Point(object.pos), CH_action):
                i = i + 1
        skill.opponentsToGoal = i

    def calculatePassRadius(me, peer, fv):
        rmin = 2 # minimal pass region radius in case of low/no velocity
        vp = 5 # pass velocity, estimated average
        vt = 4 # turtle velocity, max
        d = Shape.distance(me.pos, peer.pos)
        t = d/vp
        r = fv * vt * t #reachable distance in half a second, iteratively chosen 
        if r < rmin: 
            r = rmin
        return r

    def listRegions(regions): 
        result = []
        try: 
            for region in regions:
                result.append(region)
        except:
            result = regions
        return result


    def plotconstraint(constraint, colortype, filled = True):
        try:    
            x,y = constraint.exterior.xy
            plt.plot(x,y, color = colortype , linestyle = 'dashed', linewidth = 2.5)
            if filled:
                plt.fill(x,y, color = colortype, fill = False, hatch = '//')
        except:
            return