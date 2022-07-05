import csv
from Representation import Shape
import Settings as Set
import time

start_time = time.time()


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

class Feature:
    all = []
    """ assign position and velocity to feature"""

    def __init__(self, pos, vel=0) :
        self.pos = pos
        self.vel = vel
        self.all.append(self)
            
    """ Import data form csv file """
    @classmethod
    def instantiate_from_csv(cls):
        with open('Input.csv', 'r') as f:
            features = list(csv.DictReader(f))
            for feature in features:
                clss = feature.get('class')

                if clss == "Self":
                    Self(
                        pos = list((float(feature.get('x')),float(feature.get('y')))) ,
                        vel = list((float(feature.get('dx')),float(feature.get('dy')))) ,
                        lab = int(feature.get('label')),
                        role = feature.get('role')
                    )
                if clss == "Peer":
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
                        pos = [(float(feature.get('x')),float(feature.get('y')))] ,
                        vel = list((float(feature.get('dx')),float(feature.get('dy')))) ,
                    )
                else:
                    print(f"Type of feature is not supported, please check the input file, you entered {clss}")

    @property
    def name(self):
        # Property Decorator = Read-Only Attribute
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.__class__.__name__} \n"

    def getFeature(type, role = None): 
        result = []
        for feature in Feature.all:
            if feature.name == type: 
                if role:
                    if feature.role == role: 
                        result.append(feature)
                else:
                    result.append(feature)

        return result

    def getRole(instance, role): 
        return instance.role == role

class Self(Feature):

    def __init__(self, pos, vel, lab, role) :
        super().__init__(pos,vel)
        self.lab = lab
        self.role = role

class Peer(Feature):

    def __init__(self, pos, vel, lab, role) :
        super().__init__(pos,vel)
        self.lab = lab
        self.role = role

class Opponent(Feature):
    
    def __init__(self, pos, vel, lab) :
        super().__init__(pos,vel)
        self.lab = lab

class Ball(Feature):

    def __init__(self, pos, vel) :
        super().__init__(pos,vel)

"""Static features """
field = Shape.rectangle([0,0], Set.Field[1], Set.Field[0], True)
ownGoal = Shape.rectangle([0, -Set.Field[1]/2 - 0.5] , 1, Set.Goal,  True)
oppGoal = Shape.rectangle([0, Set.Field[1]/2 + 0.5] , 1, Set.Goal,  True)