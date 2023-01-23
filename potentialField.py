# NOT USED!

"""
Constructing potential field inside polygon 
Inpunt:     Region of interest, Type of potential field, Settings (esolution)
Output:     Gridpoint coordinates and potential (value)
"""

from sqlite3 import register_converter
from Representation import Shape
import Settings
import numpy as np
import matplotlib.pyplot as plt

class Potfield:
    # Settings
    n = 0 
    res = 0.25

    #Initialize griddpoints
    gridpoints = []

    def __init__(self, pos, mu, value):
        self.pos = pos
        self.mu = mu
        self.val = value

        Potfield.gridpoints.append(self)

    # calculate potential field 
    def potentialfield(region, type): 
        n = Potfield.n
        res = Potfield.res
    # get midpoint of region
        bounds = list(Shape.bounds(region))
        print(f"calculating potential field for behavior having region of type with bounds {bounds}")
        xmin = bounds[0]
        ymin = bounds[1]
        xmax = bounds[2]
        ymax = bounds[3]
        xw = int(round((xmax - xmin)/ res))
        yw = int(round((ymax - ymin)/ res))
        print(xw)
        print(yw)
        x = xmin
        y = ymin

        pmap = [[0.0 for i in range(yw)] for i in range(xw)]
        X = [[0.0 for i in range(yw + 1)] for i in range(xw + 1)]
        Y = [[0.0 for i in range(yw + 1)] for i in range(xw + 1)]

        for i in range(xw): 
            x = xmin + i * res
            for j in range(yw): 
                y = ymin + j * res  
                pos = [x,y] 
                posp = Shape.point(pos)
                if Shape.intersect(region, posp): 
                    mu = Potfield.calculateMuValue(pos, type)
                    value = Potfield.calculateValue(mu)
                    pmap[i][j] = value
                    X[i][j] = x - 1/2*res
                    Y[i][j] = y - 1/2*res

                    Potfield(pos, mu, value) 
                    print(f"i'm not done yet calculate gridpoint number {n}, coords {x}, {y} having value {value}")
                    n = n + 1
    
        return pmap, X, Y
    

    def calculateMuValue(pos, type): 
        mu = [] 

        x = pos[0]
        y = pos[1]

        # GENERAL FUNCTIONS (for every type)

        # 1. Reward depth 
        Fieldlength = Settings.Field[1] 
        muVal = (y + Fieldlength/2) /Fieldlength
        mu.append(muVal)



        # SKILL:    SHOOTING

        # 2. Reward big relative angle of goal 


        return mu

    def calculateValue(mu): 
        value = 0
        for i in mu: 
            value = value + i
        return value 