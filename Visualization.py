import shapely.geometry as shape
import shapely.ops
import matplotlib.pyplot as plt
import Settings
from Features import Feature
from Behavior import Behavior
from Representation import Shape
import Features
from matplotlib.pyplot import draw
from potentialField import Potfield
import numpy as np


fig = plt.plot()
plt.axis('equal')

def run(behaviors):

    field = Features.field
    x, y = field.exterior.xy
    field, = plt.plot(x,y, 'green')

    goals = [Features.ownGoal, Features.oppGoal]
    for goal in goals:
        x,y = goal.exterior.xy
        field, = plt.plot(x,y, 'green')

    Opponents = Feature.getFeature('Opponent')
    
    for opponent in Opponents: 
        opp = Shape.circle(opponent.pos,Settings.TurtleDiameter)
        x,y = opp.exterior.xy
        opp, = plt.plot(x,y, 'magenta')

    """      
        DTpoints = []  
        DTpoints.append(opponent.pos)


    DTpoints = DTpoints + list(Features.field.exterior.coords)
    #veld = [ -7 -11, 7 -11, 7 11, 7 11, -7 -11 ]
    #DTpoints.append(veld)
    print("****************************************************************************************************")
    print(Features.field.exterior.wkt)
    print("****************************************************************************************************")
    DTpoints = shape.MultiPoint(DTpoints)

    print(DTpoints.wkt)

    DT = shapely.ops.triangulate(DTpoints)
    for triangle in DT:
        x,y = triangle.exterior.xy
        DT, = plt.plot(x,y, 'black', linestyle = 'dashed')
    """


    Peers = Feature.getFeature('Peer')
    for peer in Peers: 
        pr = Shape.circle(peer.pos,Settings.TurtleDiameter)
        x,y = pr.exterior.xy
        peer, = plt.plot(x,y, 'cyan')   

    Me = Feature.getFeature('Self')
    for me in Me: 
        me = Shape. circle(me.pos, Settings.TurtleDiameter)
        x,y = me.exterior.xy
        me, = plt.plot(x,y, 'cyan')
        
    for behavior in behaviors:
        if behavior.type == "line":
            x,y = behavior.shape.coords.xy
            line, = plt.plot(x,y, 'red', linestyle = 'dotted')
        else:
            x,y = behavior.shape.exterior.xy
            if behavior.type == "pass":
                givePass, = plt.plot(x,y, 'gray', linewidth = 2.5 )
            if behavior.type == "dribble":
                dribble, = plt.plot(x,y, 'blue', linewidth = 2.5 )
            if behavior.type == "shot": 
                shot, = plt.plot(x,y, 'darkred', linewidth = 2.5 )
            if behavior.type == "avoid":
                avoid, = plt.plot(x,y, 'orange', linewidth = 2.5 )
            if behavior.type == "reach": 
                debug, = plt.plot(x,y, 'red', linestyle = 'dashed')
            #if behavior.type == "other": 
                #other, = plt.plot(x,y, 'red', linestyle = 'dashed')

    plt.legend([field, opp, peer, givePass, dribble, shot, avoid], ["field", "opponent", "peer", "pass region", "dribble region", "shot region", "avoid region"])

    plt.show()

def vizPotField(pmap, X, Y):
    pmap = np.array(pmap).T
    plt.pcolormesh(X, Y, pmap, cmap='jet')


def nGridPoint(behaviors):

    area = 0
    spacing = 0.25

    for behavior in behaviors: 
        if behavior.type != "avoid": 
            region = behavior.shape
            regionArea = Shape.area(region)
            area = area + regionArea


    field = Features.field
    fieldArea = Shape.area(field)

    n = area / (spacing * spacing)
    nField = fieldArea / (spacing * spacing)
    
    reduction = 100 - (area/fieldArea*100)

    print (f"The area of all possible actions is: {area}, thats a reduchtion of {reduction} percent")
    print (f"The number of gridpoints of all possible actions is: {n}, compared to the {nField} of the total field")
