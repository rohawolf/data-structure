import typing

""" Tree

    - Definition

    node: the basic element consisting of tree
    edge: the connection such like branch of tree
    parent node: the node which has child node
    child node: the node which has parent node
    root (node): the starting node, which has no parent node
    siblings node: the node from same parent node
    leaf (node)/(terminal node): the node which has no child node
    path: the sequence of nodes from one to another
    length: the count of nodes from start node to end node
    depth: the path length from root
    level: the edge count from root
    height: the max value of depth
    degree: the count of child node
    degree of tree: the max value of degree of node in tree
    size: total count of node including root
    width: the value of level which has maximum node count
"""

class Node(Object):
        parent = None
        siblings = []
        children = []

        def __init__(self, value: typing.Any, parent: typing.Optional[Node], siblings: typing.List[Node], children: typing.List[Node]) -> None:
            if isinstance(value, int):
                self.value = value
            else:
                self.value = id(value)
            self.parent = parent
            self.siblings = siblings
            self.children = children

        @property
        def has_parent(self) -> bool:
            return self.parent is not None

        @property
        def has_child(self) -> bool:
            return len(self.children) != 0


class Tree(Object):

    def __init__(self, elements: typing.Iterable) -> None:
        self.elements = elements
        self.build()

    def build(self):
        pass

    
