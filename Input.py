import csv

class Feature:

    def __init__(self, pos, vel) :
        self.pos = pos
        self.vel = vel

    @classmethod
    def instantiate_from_csv(cls):
        with open('input.csv', 'r') as f:
            features = list(csv.DictReader(f))
            for feature in features:
                clss = feature.get('class')

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
                    print("Type of feature is not supported, please check the input file")


    @property
    def name(self):
        # Property Decorator = Read-Only Attribute
        return self.__name

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.lab}' with position: {self.pos} \n"


class Peer(Feature):

    all = []

    def __init__(self, pos, vel, lab, role) :
        super().__init__(pos,vel)
        self.lab = lab
        self.role = role

        self.all.append(self)

class Opponent(Feature):

    all = []
    
    def __init__(self, pos, vel, lab) :
        super().__init__(pos,vel)
        self.lab = lab

        self.all.append(self)

class Ball(Feature):
    
    all = []

    def __init__(self, pos, vel) :
        super().__init__(pos,vel)
        self.lab = None
        self.all.append(self)


Feature.instantiate_from_csv()