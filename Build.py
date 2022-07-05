from Features import Feature
from Behavior import Behavior
import time
import Visualization

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
    Visualization.run(behaviors)

Feature.instantiate_from_csv()
run()

print("--- %s seconds ---" % (time.time() - start_time))