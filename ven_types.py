from __future__ import annotations
from typing import Optional

import math
import numpy as np
from dataclasses import dataclass

PI = 3.1415

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Node:
    position: Point 
    parent: Optional[Node] 
    children: Optional[list[Node]]


class SuperellipseLeafBlade:
    
    def __init__(self, a, b, r):
        self.a = a
        self.b = b
        self.r = r
        self.scale = 1

    def __call__(self, t):

        if t < 0 or t > 2*PI:
            raise ValueError("'t' parameter should be between 0 and 2π")

        return Point(
            x = self.scale*self.a*np.sign(np.cos(t))*np.abs(np.cos(t))**self.r,
            y = self.scale*self.b*np.sign(np.sin(t))*np.abs(np.sin(t))**self.r
        )
    
    def get_range_as_numpy(self, t: np.ndarray):
        x = self.scale*self.a*np.sign(np.cos(t))*np.abs(np.cos(t))**self.r
        y = self.scale*self.b*np.sign(np.sin(t))*np.abs(np.sin(t))**self.r

        return (x, y)

    def point_in_shape(self, p: Point):
        return (abs(p.x / (self.scale * self.a)))**(2 / self.r) + \
               (abs(p.y / (self.scale * self.b)))**(2 / self.r) < 1

    def compute_area(self):
        return 4 * self.scale**2 * self.a * self.b * (math.gamma(1 + self.r/2)**2 / math.gamma(1 + self.r)**2)


    @property
    def petiole(self):
        return Point(0, -self.b*self.scale)
