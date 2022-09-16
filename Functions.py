from Representation import Shape as geom
from shapely import affinity as aff

import matplotlib.pyplot as plt
"""
This class contains geometric operations used to constraint the actions
"""

class Functions:
    
    def freeLine(startPos : float, action, objects : list):
        splitLines = [] 
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
                tangentLines= [geom.line(EX_CH_avoid[0], EX_CH_avoid[1]), geom.line(EX_CH_avoid[0], EX_CH_avoid[-2])]
                print(f"we have an intersection of pass region peer {action.feature} and and avoid opponent {avoid.feature}")
                if geom.contains(SC_CH_avoid, actionRegion): 
                    return False
                elif geom.intersect(CH_action, avoidRegion): 
                    blockedRegion = geom.difference(SC_CH_avoid, geom.buffer(geom.difference(CH_avoid, avoidRegion),0.05))
                    x,y = blockedRegion.exterior.xy
                    other, = plt.plot(x,y, 'magenta', linestyle = 'dashed')
                    blocked.append(geom.intersection(actionRegion, blockedRegion))
                    for line in tangentLines: 
                        print("tangentline")
                        line = aff.scale(line,10,10)
                        if geom.intersect(actionRegion, line):
                            splitLines.append(line)
                            print(f"splitLines found: {line}")
                
                """
                if len(splitLines) != 0: 
                    for line in splitLines: 
                        splitRegions = geom.split(actionRegion, line)
                        for region in splitRegions:
                            print("hello")   
                            if geom.intersect(region, CH_avoid): 
                                print("available")
                                blocked.append(region)
                """
            
        print(blocked)
        actionRegions = [actionRegion]
        print(f"acactionRegion: {actionRegions} with length {len(actionRegions)}")
        for region in blocked:
            actionRegions = geom.differenceMultiPolygon(actionRegions, region)
            print(f"actionregions: {actionRegions}")

        return actionRegions
