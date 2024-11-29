"""Everythings that forms a graph"""

from settings import *

class Node:
    """Node of the graph"""

    x = 0
    y = 0

    tag = 0
    title = ""

    data = []

    def __init__(self, x, y, tag):
        self.x = x
        self.y = y

        self.tag = tag

        self.data = []

    def __repr__(self):
        return f"Node(x={self.x},y={self.y},tag={self.tag},data={self.data})"

    def is_inside_node(self, x, y):
        "Return true if the position is inside the node"
        return pow(self.x - x, 2) + pow(self.y - y, 2) <= pow(NODE_RADIUS, 2)

    def is_inside_spacing(self, x, y):
        "Return true if the position is inside the node spacing"
        return pow(self.x - x, 2) + pow(self.y - y, 2) <= pow(NODE_RADIUS_SPACING, 2)

    def add(self, data):
        "Append data to the node data list"
        self.data.append(data)

class Edge:
    """Edge of the graph"""
    node1 = 0
    node2 = 0

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
