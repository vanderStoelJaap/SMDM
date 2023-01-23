import Features
from Features import Feature as ft
from Behaviors import Behavior as bv
import Behaviors
import time as t
import DecisionEngine as DE
import Features
import Visualization as vz
#import cProfile

INITFLAG = True         #for initializing features 
N = 0                   #counter for the vizualisation 
INPUTLENPEER = 5        #number of peer properties (x,y,vx,vy,n)
INPUTLENOPPONENT = 4    #number of opponet properties (x,y,vx,vy)

""" 
Runs the module
input: dictionary with keys: ball, me, peers, opponents
output: skill type (0,1,2), skill target, assisting peer
"""

def run(ball = None, me = None, peers = None, opponents = None):
    # DEBUG: start timer
    start_time = t.time()   

    inputstruct = {
        'ball': ball, 
        'me': me,
        'np' : INPUTLENPEER,        
        'peers': peers,
        'no' : INPUTLENOPPONENT, 
        'opponents': opponents
        }
    
    #Create or update features
    global INITFLAG
    if INITFLAG == True: 
        #from imput csv (static situation)
        ft.instantiate_from_csv()
        
        #from inputstruct
        #ft.instantiate(inputstruct)
        INITFLAG = False
    else: 
        ft.update(inputstruct)

    #Run the decision engine
    me = Features.me
    ball = Features.ball
    peers = Features.peers
    opponents = Features.opponents
    field = Features.field
    skill = DE.onBall(me, ball, peers, opponents, field)
    if skill == None:
        print("ERROR: no skill and target have been selected")
    else:
        target_x = skill.pos[0]
        target_y = skill.pos[1]
        type = skill.ntype
        peer = None
        if skill.peer is not None:
            peer = skill.peer.lab
        if skill.ntype != 2: #Not dribbling anymore
            Behaviors.DRIBBLEREGION == None

        print("--- decision time: %s seconds ---" % (t.time() - start_time))

        #DEGUB: Print result
        print("############################################################################")
        print(f"A {type} to position {target_x, target_y} is selected with peer {peer}")
        print("############################################################################")

    #Plot semantic map
    global N
    if N >= 0:
        vz.run(me, ball, peers, opponents, field)
        N = 0
    N = N+1

    # DEBUG: print 
    print(f"behavior.all: {bv.all}")
    print("--- computing time: %s seconds ---" % (t.time() - start_time))
    bv.clear()
    
    #return skill, target, and peer in case of pass
    return (type, target_x, target_y, peer)

if __name__ == "__main__":
    run()
    #cProfile.run("run(ball, me, peers, opponents)")