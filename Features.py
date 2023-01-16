import csv
from Representation import Shape

"""
This class creates feature objects 
for now: 
    1. Peer
    2. Opponent
    3. Ball 
    4. Field
    5. Goal

Field and goals defined in settings, later maybe also here 
 
"""

#INITIATE
peers = []
opponents = []
#ball
#me
#field

class Feature:

    #SETTINGS
    turtleDiameter = 0.5
    oppDiameter = 0.5
    ballDiameter = 0.25

    fieldLength = 22.401
    fieldWidth = 13.890
    goalWidth = 2.402
    penaltySpot = [0, fieldLength/2 - 3.560]


    """ assign position and velocity to feature"""
    
    def __init__(self, pos, vel) :
        self.pos = pos
        self.vel = vel
            
    def delete(self, list = None) : 
        if list: 
            list.remove(self)
        del self

    """ Import data form csv file """
    @classmethod
    def instantiate_from_csv(cls):

        name = "Input.csv"
        Field()

        features = cls.open_file(name)
                
        for feature in features:
            
            clss = feature.get('class')

            if clss == "Self":
                Self(
                    pos = list((float(feature.get('x')),float(feature.get('y')))) ,
                    vel = list((float(feature.get('dx')),float(feature.get('dy')))) ,
                    lab = int(feature.get('label')),
                    role = feature.get('role')
                )
            elif clss == "Peer":
                Peer(
                pos = list((float(feature.get('x')),float(feature.get('y')))) ,
                vel = list((float(feature.get('dx')),float(feature.get('dy')))) ,
                lab = int(feature.get('label')),
                role = feature.get('role')
                )                    
            elif clss == "Opponent":
                Opponent(
                    pos = list((float(feature.get('x')),float(feature.get('y')))) ,
                    vel = list((float(feature.get('dx')),float(feature.get('dy')))) ,
                    lab = int(feature.get('label')),
                )
            elif clss == "Ball":
                Ball(
                    pos = list((float(feature.get('x')),float(feature.get('y')))) ,
                    vel = list((float(feature.get('dx')),float(feature.get('dy')))) ,
                )
            else:
                 (f"Type of feature is not supported, please check the input file, you entered {clss}")
    
    def open_file(name):
        try:
            with open(name, 'r') as f:
                features = list(csv.DictReader(f))
        except:
            with open(f'/home/robocup/SMDM/{name}', 'r') as f:
                features = list(csv.DictReader(f))
        return features


    @property
    def name(self):
        # Property Decorator = Read-Only Attribute
        return self.__class__.__name__

    def __repr__(self):
        return f"Feature: {self.__class__.__name__} with position: {self.pos} \n"

    def getRole(instance, role): 
        return instance.role == role

    
    def instantiate(inputstruct): 

        Field()
        ballpos, ballvel, mepos, mevel, peerpos, peervel, peerlab, opponentpos, opponentvel = Feature.convertInputs(inputstruct)
        Ball(ballpos, ballvel)
        Self(mepos, mevel)
        for i in range(int(len(peerlab))):
            Peer(peerpos[i], peervel[i], peerlab[i])
        for i in range(int(len(opponentpos))):
            Opponent(opponentpos[i], opponentvel[i])

    def update(inputstruct): 
        ballpos, ballvel, mepos, mevel, peerpos, peervel, peerlab, opponentpos, opponentvel = Feature.convertInputs(inputstruct)

        ball.pos = ballpos
        ball.vel = ballvel

        me.pos = mepos
        me.vel = mevel

        for i, peer in enumerate(peers):
            try:
                peer.pos = peerpos[i]
                peer.vel = peervel[i]
                peer.lab = peerlab[i]
            except IndexError:
                Feature.delete(peer, peers)
            except:
                print("Not able to update peer")

        nNewpeers = len(peerlab) - len(peers)
        if nNewpeers > 0:
            for i in range(nNewpeers):
                Peer(peerpos[-i-1], peervel[-i-1] , peerlab[-i-1])     
        
        for i, opponent in enumerate(opponents):
            try:
                opponent.pos = opponentpos[i]
                opponent.vel = opponentvel[i]
            except IndexError:
                Feature.delete(opponent, opponents)
            except:
                print("Not able to update opponent")

        nNewOpp = len(opponentpos) - len(opponents)
        if nNewOpp > 0: 
            for i in range(nNewOpp):
                Opponent(opponentpos[-i-1], opponentvel[-i-1]) 
                    
    def convertInputs(inputstruct):
        key = inputstruct['ball']
        ballpos = [key[0],key[1]]
        ballvel = [key[2],key[3]]
        
        key = inputstruct['me']
        mepos = [key[0],key[1]]
        mevel = [key[2],key[3]]
        
        key = inputstruct['peers']
        np = inputstruct['np']
        peerpos = []
        peervel = []
        peerlab = []
        for i in range(int(len(key)/np)):
            peerpos.append([key[i*np],key[i*np+1]])
            peervel.append([key[i*np+2],key[i*np+3]])
            peerlab.append(key[i*np+4])
        
        key = inputstruct['opponents']
        no = inputstruct['no']
        opponentpos = []
        opponentvel = []
        for i in range(int(len(key)/no)):
            opponentpos.append([key[i*no],key[i*no+1]])
            opponentvel.append([key[i*no+2],key[i*no+3]])

        return ballpos, ballvel, mepos, mevel, peerpos, peervel, peerlab, opponentpos, opponentvel

class Self(Feature):

    def __init__(self, pos, vel, lab = None, role = None) :
        super().__init__(pos,vel)
        self.lab = lab
        self.role = role
        global me
        me = self

class Peer(Feature):

    def __init__(self, pos, vel, lab = None, role = None) :
        super().__init__(pos,vel)
        self.lab = lab
        self.role = role
        peers.append(self)

class Opponent(Feature):
    
    def __init__(self, pos, vel, lab = None) :
        super().__init__(pos,vel)
        self.lab = lab
        opponents.append(self)

class Ball(Feature):

    def __init__(self, pos, vel) :
        super().__init__(pos,vel)
        global ball 
        ball = self

"""Static features """

class Field(Feature): 

    def __init__(self):
        global field
        field = self
        self.length = self.fieldLength
        self.width = self.fieldWidth
        self.goalwidth = self.goalWidth
        self.penspot = self.penaltySpot
        self.goalpos = [0, self.length/2]
        self.shape = Shape.rectangle([0,0], self.length, self.width, True)
        self.ownGoal = Shape.rectangle([0, -1/2*self.length - 0.5], 1, self.goalWidth, True)
        self.oppGoal = Shape.rectangle([0, 1/2*self.length + 0.5], 1, self.goalWidth, True)