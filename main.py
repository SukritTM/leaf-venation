from  ven_types import Node, Point, SuperellipseLeafBlade, PI
from numpy.random import default_rng

import numpy as np

from plot_utils import plot_contour, plot_edges, calculate_thicknesses
import matplotlib.pyplot as plt


gen  = default_rng(38572736218376+3)

def sample_uniform(xsmall, xlarge, ysmall, ylarge):
    global gen
    return Point(
        x = gen.uniform(xsmall, xlarge),
        y = gen.uniform(ysmall, ylarge)
    )

def walk_and_get_all_nodes(root: Node, nodes):
    nodes.append(root)

    if root.children is None: return None

    for child in root.children:
        walk_and_get_all_nodes(child, nodes)


def compute_distance(p1: Point, p2: Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**(1/2)

def generate_auxin(
        auxin_sources: set[Point], 
        source_birth_distance: float,
        nodes: list[Node],
        vein_birth_distance: float, 
        dart_number: int, 
        leaf_contour: SuperellipseLeafBlade
    ):
    global gen
    
    new_auxin_sources: list[Point] = list()

    for _ in range(dart_number):
        potential_source = sample_uniform(-leaf_contour.a, leaf_contour.a, -leaf_contour.b, leaf_contour.b)

        while not leaf_contour.point_in_shape(potential_source):
            potential_source = sample_uniform(-leaf_contour.a, leaf_contour.a, -leaf_contour.b, leaf_contour.b)
        
        auxin_dists = [compute_distance(potential_source, auxin_source) for auxin_source in auxin_sources] 
        if len(auxin_dists) == 0: auxin_dists = [9999999] 
        if min(auxin_dists) < source_birth_distance:
            continue
        
        vein_dists = [compute_distance(potential_source, node.position) for node in nodes]
        if len(vein_dists) == 0: vein_dists = [9999999] 
        if min(vein_dists) < vein_birth_distance:
            continue

        new_auxin_sources.append(potential_source)

    return new_auxin_sources

def generate_auxin_marginonly(
        auxin_sources: set[Point], 
        source_birth_distance: float,
        nodes: list[Node],
        vein_birth_distance: float, 
        dart_number: int, 
        leaf_contour: SuperellipseLeafBlade
):
    global gen

    new_auxin_sources: list[Point] = list()

    for _ in range(dart_number):
        t = gen.uniform(0, 2*PI)
        potential_source = leaf_contour(t)
        
        auxin_dists = [compute_distance(potential_source, auxin_source) for auxin_source in auxin_sources] 
        if len(auxin_dists) == 0: auxin_dists = [9999999] 
        if min(auxin_dists) < source_birth_distance:
            continue
        
        vein_dists = [compute_distance(potential_source, node.position) for node in nodes]
        if len(vein_dists) == 0: vein_dists = [9999999] 
        if min(vein_dists) < vein_birth_distance:
            continue

        new_auxin_sources.append(potential_source)

    return new_auxin_sources


def check_and_kill_auxin(auxin_sources, nodes, kill_distance):

    for auxin in auxin_sources:
        if min([compute_distance(auxin, node.position) for node in nodes]) < kill_distance:
            auxin_sources.remove(auxin)


def expand_leaf(leaf_contour, nodes, auxin_sources, factor_increase):
    old_petiole = leaf_contour.petiole
    leaf_contour.scale += factor_increase
    new_petiole = leaf_contour.petiole
    diff_x = new_petiole.x - old_petiole.x
    diff_y = new_petiole.y - old_petiole.y

    for node in nodes:
        node.position.x += diff_x
        node.position.y += diff_y

    for auxin in auxin_sources:
        auxin.x += diff_x
        auxin.y += diff_y


def place_new_nodes(nodes, auxin_sources):

    closest = {i: [] for i, node in enumerate(nodes)}
    for source in auxin_sources:
        distances = np.array([compute_distance(source, node.position) for node in nodes])
        min_arg = np.argmin(distances)
        # node = nodes[min_arg]
        closest[min_arg].append(source)
    
    for nodeidx, sources in closest.items():
        if len(sources) == 0: continue
        
        node = nodes[nodeidx]
        vectors = np.array([[source.x - node.position.x for source in sources],
                            [source.y - node.position.y for source in sources]]).T
        
        normed_vectors = vectors / np.linalg.norm(vectors, axis=1)[:, np.newaxis]
        summed_vectors = np.sum(normed_vectors, axis=0)
        normed_final_pos = summed_vectors / np.linalg.norm(summed_vectors)

        newnode = Node(position=Point(node.position.x + normed_final_pos[0], node.position.y + normed_final_pos[1]), parent=node, children=None)
        node.children = [newnode] if node.children is None else node.children + [newnode]






def main():
    auxin_sources: list[Point] = list()
    leaf_contour = SuperellipseLeafBlade(a = 2, b = 5, r = 0.8)
    root_node = Node(position=leaf_contour.petiole, parent=None, children=None)

    B_DIST_S = 10
    B_DIST_V = 3
    K_DIST = 2
    NUM_NEW_SRC_PER_AREA = 1
    GROWTH_DELTA = 0.09

    NUM_ITER = 55

    nodes = [root_node]

    for _ in range(NUM_ITER):
        new_auxin_sources = generate_auxin_marginonly(
            auxin_sources = auxin_sources, 
            source_birth_distance = B_DIST_S,
            nodes = nodes,
            vein_birth_distance = B_DIST_V, 
            dart_number = int(NUM_NEW_SRC_PER_AREA * leaf_contour.compute_area()),
            leaf_contour = leaf_contour
        )

        auxin_sources.extend(new_auxin_sources)
        place_new_nodes(nodes, auxin_sources)
        check_and_kill_auxin(auxin_sources, nodes, K_DIST)
        expand_leaf(leaf_contour, nodes, auxin_sources, GROWTH_DELTA)

        nodes = []
        walk_and_get_all_nodes(root_node, nodes)

    plt.axis('equal')
    plot_contour(leaf_contour)
    plot_edges(root_node, nodes=nodes)
    plt.show()





if __name__ == '__main__':
    main()