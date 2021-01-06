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


class Node:
    def __init__(
        self,
        key: int,
        value: typing.Any,
        left: Node,
        right: Node,
        parent: Node = None,
    ) -> None:

        self.key = key
        self.value = value
        self.left = left
        self.right = right

        self.parent = None

    def __repr__(self):
        return f"<Node key:{self.key}, value:{self.value}, parent:{self.parent}, left:{self.left}, right:{self.right}>"




class BinaryTree:
    def __init__(self, elements: typing.Iterable) -> None:
        self.root = None
        for value, key in enumerate(elements):
            self.root = self.insert(key, value, self.root)

    def search(
        self, key: int, node: Node = None, allow_duplicate: bool = False
    ) -> Node:
        _node = node or self.root
        while _node is not None:
            if not allow_duplicate and key == _node.key:
                return _node

            _node = _node.left if key < _node.key else _node.right
        return _node

    def insert(self, key: int, value: typing.Any, node: Node = None) -> Node:
        if node is None:
            return Node(key, value, None, None, None)

        if key == node.key:
            return Node(key, value, node.left, node.right, node.parent)

        if key < node.key:
            return Node(
                node.key,
                node.value,
                self.insert(key, value, node.left),
                node.right,
                node.parent,
            )

        return Node(
            node.key,
            node.value,
            node.left,
            self.insert(key, value, node.right),
            node.parent,
        )

    def minimum(self, node: Node):
        _node = node
        while _node.left is not None:
            _node = _node.left
        return _node

    def replace(self, node: Node, another: Node):
        if node.parent:
            if node == node.parent.left:
                node.parent.left = another
            else:
                node.parent.right = another
        if another is not None:
            another.parent = node.parent


if __name__ == "__main__":

    from random import shuffle

    el = list(range(150))
    shuffle(el)
    bt = BinaryTree(el)
    print(bt.search(10))
