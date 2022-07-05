import shapely.geometry as shape
import matplotlib.pyplot as plt
import Settings
from Features import Feature
from Behavior import Behavior
from Representation import Shape
import Features

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

    Peers = Feature.getFeature('Peer')
    for peer in Peers: 
        pr = Shape.circle(peer.pos,Settings.TurtleDiameter)
        x,y = pr.exterior.xy
        peer, = plt.plot(x,y, 'cyan')   

    Me = Feature.getFeature('Self')
    for me in Me: 
        me = Shape. circle(me.pos, Settings.TurtleDiameter)
        x,y = me.exterior.xy
        me, = plt.plot(x,y, 'darkcyan')
        
    for behavior in behaviors:
        if behavior.type == "line":
            x,y = behavior.shape.coords.xy
            line, = plt.plot(x,y, 'black')
        else:
            x,y = behavior.shape.exterior.xy
            if behavior.type == "pass":
                givePass, = plt.plot(x,y, 'gray')
            if behavior.type == "dribble":
                dribble, = plt.plot(x,y, 'blue')
            if behavior.type == "shot": 
                shot, = plt.plot(x,y, 'darkred')
            if behavior.type == "avoid":
                avoid, = plt.plot(x,y, 'orange')
            if behavior.type == "reach": 
                debug, = plt.plot(x,y, 'red')


    plt.legend([field, opp, peer, givePass, dribble, shot, avoid], ["field", "opponent", "peer", "pass region", "dribble region", "shot region", "avoid region"])

    plt.show()