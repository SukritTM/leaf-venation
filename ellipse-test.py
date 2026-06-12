import matplotlib.pyplot as plt
import numpy as np

from ven_types import Point

t = np.linspace(0, 2*3.1415)
# x = np.cos(t)*(1 + 0.5*np.sin(t)**2)
# y = np.sin(t) * np.cos(t)**2

x = 3*np.sign(np.cos(t))*np.abs(np.cos(t))**0.8
y = 5*np.sign(np.sin(t))*np.abs(np.sin(t))**0.8



plt.plot(x, y)
plt.scatter([0], [-5])
plt.axis('equal')
plt.show()

def draw_linesegment(p1: Point, p2: Point, thickness=1):
    plt.plot([p1.x, p2.x], [p1.y, p2.y], linewidth=thickness)

draw_linesegment(Point(0, 0), Point(1, 1), thickness=3)
plt.show()