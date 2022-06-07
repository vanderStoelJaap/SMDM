from re import S
import shapely.geometry as shape
import matplotlib.pyplot as plt
from Settings import Settings
from Behavior import Behavior
from Representation import Shape
from Input import Feature, Opponent, Peer, Ball


field = Shape.rectangle([0,0], Settings.Field[1], Settings.Field[0], True)
x, y = field.exterior.xy
plt.plot(x,y, 'g')

for opponent in Opponent.all:
    opp = Shape.circle(opponent.pos,Settings.TurtleDiameter)
    x,y = opp.exterior.xy
    plt.plot(x,y, 'm')

for peer in Peer.all:
    pr = Shape.circle(peer.pos,Settings.TurtleDiameter)
    x,y = pr.exterior.xy
    plt.plot(x,y, 'b')    
    
    
for behavior in Behavior.all:
    x,y = behavior.shape.exterior.xy
    if behavior.label == "checkPassLine":
        plt.plot(x,y, 'k')
        print("label is checkPassLine")
    if behavior.label == "avoidOpponent":
        plt.plot(x,y, 'r')
    else:
        plt.plot(x,y, 'k')
        print(behavior.label)

print(Peer.all)
print(Opponent.all)
plt.show()