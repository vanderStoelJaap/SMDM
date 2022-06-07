import shapely.geometry as geom
from shapely.geometry import Point, MultiPoint, asMultiPoint
import numpy as np
import math

class Shape: 

    #SHAPES 
    def circle(pos, radius):
        p = geom.Point(pos[0],pos[1])
        circ = p.buffer(radius)
        return circ

    def rectangle(pos, length , width , centred: bool):
        
        if centred == True: 
            a = [pos[0] - 0.5*width, pos[1] - 0.5*length] 
            b = [pos[0] + 0.5*width, pos[1] - 0.5*length] 
            c = [pos[0] + 0.5*width, pos[1] + 0.5*length] 
            d = [pos[0] - 0.5*width, pos[1] + 0.5*length] 
        elif centred == False:
            a = pos; 
            b = [pos[0] + width, pos[1]]
            c = [pos[0] + width, pos[1] + length]
            d = [pos[0], pos[1] + length]

        rect = geom.Polygon([a, b, c, d, a])
        return rect

    def convexHull(obj1: list, obj2: list):

        merge = obj1 + obj2
        convexHull = geom.MultiPoint(merge).convex_hull
        return convexHull

    def intersect(obj1, obj2):

        return obj1.intersects(obj2)
