import time
start_time = time.time()

from re import S
import shapely.geometry as shape
import matplotlib.pyplot as plt
from Settings import Settings
from Behavior import Behavior
from Representation import Shape
from Input import Feature, Opponent, Peer, Ball

fig = plt.plot()
plt.axis('equal')


field = Shape.rectangle([0,0], Settings.Field[1], Settings.Field[0], True)
x, y = field.exterior.xy
field, = plt.plot(x,y, 'g')

goals = [Shape.rectangle([0,i], 1, Settings.Goal, True) for i in [-11.5, 11.5]] 
for goal in goals: 
    x,y = goal.exterior.xy
    field, = plt.plot(x,y, 'g')


for opponent in Opponent.all:
    opp = Shape.circle(opponent.pos,Settings.TurtleDiameter)
    x,y = opp.exterior.xy
    opp, = plt.plot(x,y, 'm')

for peer in Peer.all:
    pr = Shape.circle(peer.pos,Settings.TurtleDiameter)
    x,y = pr.exterior.xy
    peer, = plt.plot(x,y, 'b')   
    
for behavior in Behavior.all:
    if behavior.label == "line":
        x,y = behavior.shape.coords.xy
        line, = plt.plot(x,y, 'b')
    else:
        #print(behavior.all)
        #print(f"behavior {behavior.label} with shape {behavior.shape}")
        x,y = behavior.shape.exterior.xy
        if behavior.label == "pass":
            givePass, = plt.plot(x,y, 'k')
        if behavior.label == "avoid":
            avoid, = plt.plot(x,y, 'r')
            pass
       # else:
        #    plt.plot(x,y, 'k')


plt.legend([field, opp, peer, avoid, givePass], ["field", "opponent", "peer", "avoid region", "pass region"])

plt.show()