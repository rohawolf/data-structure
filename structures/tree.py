import typing

from stack import Stack
from queue import Queue

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

class DFSMixin:
    """add-on Mix-in class including DFS (Depth-First Search) methods
    
    the general DFS recursive patten for traversing a binary tree

    Go down on level to the recursive argument N.
    If N exits (is non-empty) execute the following three operations in a certain order
    (L) Recursively traverse N's left subtree.
    (R) Recursively traverse N's right subtree.
    (N) Process the current node N itself.

    Return by going up one level and arriving at the parent node of N.
    
    """

    def pre_order(self, visit=lambda _node: print(_node.value)):
        """ N - L - R """
        s = Stack()
        s.push(self)
        while not s.is_empty:
            node = s.pop()
            visit(node)

            if node.right is not None:
                s.push(node.right)

            if node.left is not None:
                s.push(node.left)
        
    def in_order(self, visit=lambda _node: print(_node.value)):
        """ L - N - R """
        s = Stack()
        node = self
        while (not s.is_empty or node is not None):
            if node is not None:
                s.push(node)
                node = node.left
            else:
                node = s.pop()
                visit(node)
                node = node.right

    def post_order(self, visit=lambda _node: print(_node.value)):
        """ L - R - N """
        s = Stack()
        node = self
        last_visited = None
        while (not s.is_empty or node is not None):
            if node is not None:
                s.push(node)
                node = node.left
            else:
                peek_node = s.peek()
                if peek_node.right is not None and last_visited != peek_node.right:
                    node = peek_node.right
                else:
                    visit(peek_node)
                    last_visited = s.pop()


class BFSMixin:
    """add-on Mix-in class including BFS (Breath-First Search) methods
    
    Trees can also be traversed in level-order, where we visit every node on a level before going to a lower level. 
    This search is referred to as breadth-first search (BFS), as the search tree is broadened as much as possible 
    on each depth before going to the next depth.
    """

    def level_order(self, visit=lambda _node: print(_node.value)):
        q = Queue()
        q.enqueue(self)
        while not q.is_empty:
            node = q.dequeue()
            visit(node)

            if node.left is not None:
                q.enqueue(node.left)

            if node.right is not None:
                q.enqueue(node.right)


class AVLMixin:
    BALANCE_FACTOR_RANGE = [-1, 0, 1]

    @property
    def balance_factor(self):
        _right_subtree_height = self.right.height() if self.right else 0
        _left_subtree_height = self.left.height() if self.left else 0
        _balance_factor = _right_subtree_height - _left_subtree_height
        return _balance_factor


    @property
    def is_unbalanced(self):
        return self.balance_factor not in self.BALANCE_FACTOR_RANGE


    def rotate_left(self, sub_root, node):
        tmp = node.left
        sub_root.right = tmp
        if tmp is not None:
            tmp.parent = sub_root
        node.left = sub_root
        sub_root.parent = node

        return node


    def rotate_right(self, sub_root, node):
        tmp = node.right
        sub_root.left = tmp
        if tmp is not None:
            tmp.parent = sub_root
        node.right = sub_root
        sub_root.parent = node

        return node


    def rotate_left_right(self, sub_root, node):
        _node = node.right
        _node = self.rotate_left(node, _node)
        _node = self.rotate_right(sub_root, _node)

        return _node


    def rotate_right_left(self, sub_root, node):
        _node = node.left
        _node = self.rotate_right(node, _node)
        _node = self.rotate_left(sub_root, _node)

        return _node


    def _insert(self, key, value):
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


    def _insert_rebalancing(self):
        pass


    def _delete(self, key):
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


    def _delete_rebalancing(self):
        pass

    
    def insert(self, key, value):
        self._insert(key, value)
        self._insert_rebalancing()


    def delete(self, key):
        self._delete(key)
        self._delete_rebalancing()


class TreeNode(DFSMixin, BFSMixin, AVLMixin):
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
    

    def search(self, key=None):
        _current = self
        while _current is not None:
            if key is None:
                return None
            if key == _current.key:
                break
            _current = _current.left if key < _current.key else _current.right
        return _current


    def is_parent(self, _node):
        return _node is not None and _node.parent == self


    def is_left(self, _parent):
        return self.parent and self.parent.left == self


    def is_right(self, _parent):
        return self.parent and self.parent.right == self


    def height(self):
        _height = 1
        _right_subtree_height = self.right.height() if self.right else 0
        _left_subtree_height = self.left.height() if self.left else 0

        _extra = _right_subtree_height if _right_subtree_height > _left_subtree_height else _left_subtree_height
        
        return _height + _extra


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

if __name__ == '__main__':
    from random import shuffle
    keys = list(range(11))
    values = list(range(2, 12))
    shuffle(keys)

    elements = dict(zip(keys, values))

    bt = BinaryTree(elements)
    print(bt, bt.root.height())
    print('in-order: '); bt.root.in_order()
    print('pre-order: '); bt.root.pre_order()
    print('post-order: '); bt.root.post_order()
    print('level-order: '); bt.root.level_order()