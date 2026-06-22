import matplotlib.pyplot as plt
import numpy as np

from ven_types import Point, SuperellipseLeafBlade, Node

def plot_contour(leaf_contour: SuperellipseLeafBlade, color='black'):
    t = np.linspace(0, 2*np.pi)
    x, y = leaf_contour.get_range_as_numpy(t)
    plt.plot(x, y, c=color)


def calculate_thicknesses(nodes):

    thicknesses = [None] * len(nodes)

    min_thick = 0.1
    root = None
    for i, node in enumerate(nodes):
        if thicknesses[i] is not None: continue
        
        if node.children is None:
            thicknesses[i] = min_thick
            continue

        if node.parent is None:
            root = node
                
    
    def _recurse(root, thicknesses):
        my_index = nodes.index(root)
        try:
            if thicknesses[my_index] is not None: return
        except IndexError as e:
            print(my_index, len(thicknesses))
            exit(1)
        

        for child in root.children:
            _recurse(child, thicknesses)
        
        child_thicknesses = [thicknesses[nodes.index(child)] for child in root.children]
        
        try:
            thicknesses[my_index] = sum(child_thicknesses)
        except IndexError as e:
            print('over here')
            print(my_index, len(thicknesses))
            exit(1)
        
    _recurse(root, thicknesses)
    
    return thicknesses


def plot_edges(root: Node, color='black', nodes = None, thicknesses = None):

    if root.children is None: return

    if thicknesses == None:
        for child in root.children:
            plt.plot([root.position.x, child.position.x], [root.position.y, child.position.y], c=color)
            plot_edges(child)
    else:
        thickness = thicknesses[nodes.index(root)]
        for child in root.children:
            plt.plot([root.position.x, child.position.x], [root.position.y, child.position.y], c=color, linewidth=thickness)
            plot_edges(child)