from re import S
import shapely.geometry as shape
import matplotlib.pyplot as plt


p = shape.Point(0,0)
circ = p.buffer(2)
x, y = circ.exterior.xy
square = shape.Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
x2, y2, = square.exterior.xy

plt.plot(x,y)
plt.plot(x2,y2) 
plt.show()