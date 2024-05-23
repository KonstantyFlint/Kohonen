from functools import cached_property
from typing import List, Set, Callable

import numpy as np


class Node:

    def __init__(self):
        self.position = np.random.uniform(-1, 1, 3)
        self.neighbours: List[Node] = []

    def __hash__(self):  # unsafe
        return hash(tuple(self.position))

    def move(self, target: np.ndarray, scale: float):
        self.position += (target - self.position) * scale

    @cached_property
    def neighbour_waves(self) -> List[Set["Node"]]:
        current_wave = {self}
        visited = set()
        waves = []
        while current_wave:
            waves.append(current_wave)
            visited |= current_wave
            new_wave = set()
            for node in current_wave:
                new_wave |= set(node.neighbours)
            current_wave = new_wave - visited

        return waves


class Grid:

    def __init__(
            self,
            width: int,
            height: int
    ):
        self.nodes = make_grid_nodes(width, height)

    def iter_nodes(self):
        for row in self.nodes:
            yield from row

    def plot(self, plot):
        for node in self.iter_nodes():
            plot.scatter(*node.position, color='r')
            x, y, z = node.position
            for neighbour in node.neighbours:
                x2, y2, z2 = neighbour.position
                plot.plot([x, x2], [y, y2], [z, z2], color='r')

    def get_closest(self, target: np.ndarray) -> Node:
        return min(self.iter_nodes(), key=lambda node: np.sum(np.square(node.position - target)))

    def move(
            self,
            sample_getter: Callable[[], np.ndarray],
            neighbour_scale_getter: Callable[[int], float],
            time_scale: float,
    ):
        target = sample_getter()
        closest = self.get_closest(target)
        node_waves = closest.neighbour_waves
        for taxi_distance, wave in enumerate(node_waves):
            for node in wave:
                scale = neighbour_scale_getter(taxi_distance) * time_scale
                node.move(target, scale)


def connect_nodes(a: Node, b: Node):
    a.neighbours.append(b)
    b.neighbours.append(a)


def connect_rows(row_a: List[Node], row_b: List[Node]):
    for (a, b) in zip(row_a, row_b):
        connect_nodes(a, b)


def make_row_nodes(width: int):
    nodes = [Node()]
    for _ in range(width - 1):
        nodes.append(Node())
        connect_nodes(nodes[-1], nodes[-2])
    return nodes


def make_grid_nodes(width, height) -> List[List[Node]]:
    rows = [make_row_nodes(width)]
    for _ in range(height - 1):
        rows.append(make_row_nodes(width))
        connect_rows(rows[-1], rows[-2])
    return rows
