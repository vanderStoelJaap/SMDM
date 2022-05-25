import shapely.geometry as shape
import matplotlib.pyplot as plt


p = shape.Point(0,0)
circ = p.buffer(2)

x, y = circ.exterior.xy
plt.plot(x,y) 
plt.show()