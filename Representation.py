import shapely.geometry as geom
import shapely.ops as ops
import shapely.affinity as aff
from shapely.affinity import scale 
from shapely.geometry import Point, MultiPoint, asMultiPoint, LineString
import numpy as np

""" This class calculates and creates spatial representations"""

class Shape: 

    #SHAPES 
    def point(pos): 
        p = geom.Point(pos[0],pos[1])
        return p 

    def line(xy1, xy2): 
        l = geom.LineString([xy1,xy2])
        return l

    def circle(pos, radius):
        p = geom.Point(pos[0],pos[1])
        circ = p.buffer(radius) 
        return circ

    def ellipse(pos, radius, vel_vec): 
        phi = np.arctan2(vel_vec[1],vel_vec[0])
        velocity = 0.25 * np.sqrt(vel_vec[0] ** 2 + vel_vec[1] ** 2 )
        major = velocity + radius
        minor = np.sqrt( major ** 2 - velocity ** 2 )
        midpoint = [pos[0] + velocity, pos[1]]
        p = geom.Point(midpoint)
        ellipse = p.buffer(1)
        ellipse = aff.scale(ellipse, major, minor)
        ellipse = aff.rotate(ellipse, phi, use_radians=True, origin=(pos[0],pos[1]))
        return ellipse

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

    def buffer(obj, val): 
        return obj.buffer(val)

    def exterior(obj):
        return obj.exterior.coords

    def convexHull(obj1, obj2):
        merge = list(obj1) + list(obj2)
        convexHull = geom.MultiPoint(merge).convex_hull
        return convexHull

    def envelope(obj):
        return obj.envelope

    def bounds(obj): 
        return obj.bounds

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
    
    def contains(obj1, obj2):
        return obj1.contains(obj2)

    def split(obj, line):
        return ops.split(obj, line)

    def intersection(obj1, obj2):
        return obj1.intersection(obj2)

    def difference(obj1, obj2):
        return obj1.difference(obj2)

    def differenceMultiPolygon(polylist: list, obj): 
        result = []
        if polylist and len(polylist) > 1: 
            for polygon in polylist: 
                result.append(Shape.difference(polygon, obj))
        elif polylist: 
            result.append(Shape.difference(polylist[0], obj))
        return result

    def voronoi(multipoint):
        voronoi = ops.voronoi_diagram(multipoint)
        return voronoi

    def area(shape):
        return shape.area

    def reshape(region, passRegion, lines, avoid_region): 
        """Used in checkpassline, has to be rewritten """
        reshape = []
        new_region = []
        number = 1
        for line in lines:
            regions = Shape.split(region, line)
            for n in regions:
                new_region.append(n) 
        for new_reg in new_region:
            if not Shape.intersect(new_reg, avoid_region):
                new_reg = new_reg.intersection(passRegion)
                reshape.append(new_reg)

        return reshape   


