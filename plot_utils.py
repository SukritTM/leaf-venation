import matplotlib.pyplot as plt
import numpy as np

from ven_types import Point, SuperellipseLeafBlade, Node

def plot_contour(leaf_contour: SuperellipseLeafBlade, color='black'):
    t = np.linspace(0, 2*np.pi)
    x, y = leaf_contour.get_range_as_numpy(t)
    plt.plot(x, y, c=color)

def plot_edges(root: Node, color='black'):

    if root.children is None: return

    for child in root.children:
        plt.plot([root.position.x, child.position.x], [root.position.y, child.position.y], c=color)
        plot_edges(child)