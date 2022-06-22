import shapely.geometry as geom
import shapely.ops as ops
from shapely.affinity import scale 
from shapely.geometry import Point, MultiPoint, asMultiPoint, linestring
import numpy as np
import matplotlib.pyplot as plt


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

    def cover(obj1, obj2): 
        return obj1.covers(obj2)

    def crosses(obj1, obj2):
        return obj1.crosses(obj2)

    def overlaps(obj1, obj2):
        return obj1.overlaps(obj2)

    def touches(obj1, obj2):
        return obj1.touches(obj2)

    def split(obj, line):
        #print(f"intersection ? answer: {Shape.intersect(obj,line)}")
        return ops.split(obj, line)

    def intersection(obj1, obj2):
        return obj1.intersection(obj2)

    def voronoi(multipoint):

        voronoi = ops.voronoi_diagram(multipoint)
        return voronoi

    def reshape(region, passRegion, line, avoid_region): 

        reshape = []

        new_region = list(Shape.split(region, line))
        #print(f"now I have found a region without intersections with avoid behavior")
        for new_reg in new_region:
            #print("hello")
            if not Shape.intersect(new_reg, avoid_region):
                new_reg = new_reg.intersection(passRegion)
                reshape.append(new_reg)
                #print(f"reshape behavior created with shape")
            #else: 
                #print(f"intersection check: {Shape.intersect(region, avoid_region)}")

        return reshape   


