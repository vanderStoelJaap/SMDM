from shapely.geometry import Point, MultiPoint, LineString, Polygon
from shapely.ops import voronoi_diagram, split
from shapely.affinity import scale, rotate

from numpy import sqrt, arctan2
import matplotlib.pyplot as plt

""" This class calculates and creates spatial representations"""

RESOLUTION = 4

class Shape: 

    #SHAPES 
    def point(pos): 
        return Point(pos[0],pos[1])

    def MultiPoint(points):
        return MultiPoint(points)

    def representativePoint(shape):
        p = shape.representative_point()
        return [p.x, p.y]

    def line(xy1, xy2): 
        l = LineString([xy1,xy2])
        return l

    def circle(pos, radius):
        p = Point(pos[0],pos[1])
        circ = p.buffer(radius, RESOLUTION) 
        return circ

    def buffer(obj, dist): 
        return obj.buffer(dist, RESOLUTION)

    def ellipse(pos, radius, vel_vec, fv): 
        phi = arctan2(vel_vec[1],vel_vec[0]) #orientation of velocity
        velocity = sqrt(vel_vec[0] ** 2 + vel_vec[1] ** 2 ) #magnitude of velocity
        major = radius + fv*velocity #fv iteratively chosen
        minor = radius
        c = sqrt( (0.5*major) ** 2  - (0.5*minor) ** 2)
        focal = (pos[0] + c, pos[1])
        ellipse = Shape.circle(focal, 1)
        ellipse = scale(ellipse, major, minor) #, origin=(pos[0],pos[1]))
        ellipse = rotate(ellipse, phi, use_radians=True, origin=(pos[0],pos[1]))
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

        rect = Polygon([a, b, c, d, a])
        return rect

    def buffer(obj, val): 
        return obj.buffer(val)

    def exterior(obj):
        return obj.exterior.coords

    def convexHull(obj1: list, obj2: list): 
        merge = [*obj1, *obj2]
        return MultiPoint(merge).convex_hull

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
        return split(obj, line)

    def intersection(obj1, obj2):
        return obj1.intersection(obj2)

    def difference(obj1, obj2):
        return obj1.difference(obj2)

    def differenceMultiPolygon(polylist: list, obj): 
        result = []
        for polygon in polylist: 
            regions = polygon.difference(obj)
            if regions.is_empty:
                return None
            try:
                for region in regions:
                    result.append(region)
            except:
                result.append(regions)
        return result

    def voronoi(multipoint):
        return voronoi_diagram(multipoint)

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

    def distance(pos1, pos2):
        pos1 = Point(pos1) 
        pos2 = Point(pos2) 
        return pos1.distance(pos2)

    def empty(region):
        return region.is_empty

    def linscale(object, xfact, yfact):
        return scale(object, xfact, yfact)

    def perpLine(begin, end):
        dx = end[0] - begin[0]
        dy = end[1] - begin[1]

        yb = begin[1] - 10*dx
        ye = begin[1] + 10*dx
        xb = begin[0] + 10*dy
        xe = begin[0] - 10*dy

        return Shape.line((xb, yb), (xe, ye))
