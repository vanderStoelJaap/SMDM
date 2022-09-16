from Features import Feature
from Behavior import Behavior
from potentialField import Potfield
import time
import Visualization
from matplotlib import pyplot as plt
start_time = time.time()

role = 'main'

def run(): 

    if role == 'main':
        Behavior.avoidOpponent()
        Behavior.givePass()
        Behavior.checkReachability()
        Behavior.checkPassLine()
        Behavior.dribble()
        Behavior.checkDribble()
        Behavior.shot()
        Behavior.checkShot()
    
    if role == 'walkFree': 
        Behavior.avoidOpponent()
        Behavior.receivePass()
        Behavior.dribble()
    
    behaviors = Behavior.getAllBehavior()

    k = 1

    """
    for behavior in behaviors: 
        if behavior.shape: 
            if k < 3: 
                reg = behavior.shape
                x , y = reg.exterior.xy
                plt.plot(x,y) 
                print(reg)
                pmap, X, Y = Potfield.potentialfield(behavior.shape, "type")
                print(pmap)
                Visualization.vizPotField(pmap, X, Y)
                k = k+1
            else:  
                print("Empty behavior")
    """
    
    Visualization.nGridPoint(behaviors)
    Visualization.run(behaviors)
    plt.show()

Feature.instantiate_from_csv()
run()

print("--- %s seconds ---" % (time.time() - start_time))