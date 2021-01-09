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


class TreeNode:
    def __init__(self, key, value, left = None, right = None, parent = None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent


    def __repr__(self):
        return f'< {self.left or "*"} <-- {self.key}:{self.value} --> {self.right or "*"} >'


    def min(self):
        _current = self
        while _current.left:
            _current = _current.left
        return _current

    
    def replace(self, other):
        if self.parent:
            if self == self.parent.left:
                self.parent.left = other
            else:
                self.parent.right = other

        if other:
            other.parent = self.parent


    def insert(self, key, value):
        _current = self
        while True:
            if key == self.key:
                return
            
            if key < _current.key:
                if _current.left is None:
                    _current.left = TreeNode(key, value, parent=_current)
                    return
                _current = _current.left
            else:
                if _current.right is None:
                    _current.right = TreeNode(key, value, parent=_current)
                    return
                _current = _current.right
        

    def search(self, key=None):
        _current = self
        while _current is not None:
            if key is None:
                return None
            if key == _current.key:
                break
            _current = _current.left if key < _current.key else _current.right
        return _current


    def delete(self, key):
        if key < self.key:
            self.left.delete(key)
            return

        if key > self.key:
            self.right.delete(key)
            return

        if self.left and self.right:
            successor = self.right.min()
            self.key = successor.key
            successor.delete(successor.key)

        elif self.left:
            self.replace(self.left)

        elif self.right:
            self.replace(self.right)

        else:
            self.replace(None)


    def is_parent(self, _node):
        return _node is not None and _node.parent == self


    def is_left(self, _parent):
        return self.parent and self.parent.left == self


    def is_right(self, _parent):
        return self.parent and self.parent.right == self


    def traverse(self, key_from=0, callback=lambda v: print(v), _type='in-order'):
        if _type not in ['in-order', 'pre-order', 'post-order']:
            return

        _node = self.search(key_from)
        if _node is None:
            return

        if _type == 'in-order':
            if _node.left:
                self.traverse(_node.left.key, callback)
            callback(_node.value)
            if _node.right:
                self.traverse(_node.right.key, callback)

        elif _type == 'pre-order':
            callback(_node.value)
            if _node.left:
                self.traverse(_node.left.key, callback)
            if _node.right:
                self.traverse(_node.right.key, callback)

        else:
            if _node.left:
                self.traverse(_node.left.key, callback)
            if _node.right:
                self.traverse(_node.right.key, callback)                
            callback(_node.value)



class BinaryTree:
    def __init__(self, values):
        self.root = None

        if any([isinstance(values, _type) for _type in [list, set, frozenset]]):
            _iter = enumerate(values)
        elif isinstance(values, dict):
            _iter = values.items()

        for key, value in _iter:
            if self.root is None:
                self.root = TreeNode(key, value)
            else:
                self.root.insert(key, value)


    def __repr__(self):
        return str(self.root)

    def traverse(self, callback=lambda v: print(v), _type='in-order'):
        self.root.traverse(key_from=self.root.key, callback=callback, _type=_type)


if __name__ == '__main__':
    from random import shuffle
    keys = list(range(11))
    values = list(range(2, 12))
    shuffle(keys)

    elements = dict(zip(keys, values))

    bt = BinaryTree(elements)
    print('in-order: '); bt.traverse()
    print('pre-order: '); bt.traverse(_type='pre-order')
    print('post-order: '); bt.traverse(_type='post-order')