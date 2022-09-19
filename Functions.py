from Representation import Shape as geom
from shapely import affinity as aff

# DEBUG
import matplotlib.pyplot as plt

"""
This class contains geometric operations used to constraint the actions
"""

class Functions:
    
    def freeLine(startPos : float, action, objects : list):
        blocked = []
        actionRegion = action.shape
        
        EX_action = geom.exterior(actionRegion)
        CH_action = geom.convexHull(startPos, EX_action) 
        for avoid in objects: 
            avoidRegion = avoid.shape
            EX_avoid = geom.exterior(avoidRegion)
            if geom.intersect(CH_action, avoidRegion): 
                CH_avoid = geom.convexHull(startPos, EX_avoid)
                EX_CH_avoid = geom.exterior(CH_avoid)
                SC_CH_avoid = aff.scale(CH_avoid, 10, 10, origin= EX_CH_avoid[0])
                if geom.contains(SC_CH_avoid, actionRegion): 
                    return False
                elif geom.intersect(CH_action, avoidRegion): 
                    blockedRegion = geom.difference(SC_CH_avoid, geom.buffer(geom.difference(CH_avoid, avoidRegion),0.05))
                    blocked.append(geom.intersection(actionRegion, blockedRegion))

                    #DEBUG
                    x,y = blockedRegion.exterior.xy
                    other, = plt.plot(x,y, 'magenta', linestyle = 'dashed')                    

        print(blocked)
        actionRegions = [actionRegion]
        for region in blocked:
            actionRegions = geom.differenceMultiPolygon(actionRegions, region)
            
            #DEBUG
            print(f"actionregions: {actionRegions}")

        return actionRegions

    def Reachable(action, objects: list):

        points = geom.MultiPoint(objects)
        reachability = geom.voronoi(points)
        
        for region in reachability: 
            if geom.intersect(geom.point(action.center), region):
                action.shape = geom.intersection(region, action.shape)
