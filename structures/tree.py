from queue import Queue


class NodeAlreadyExist(Exception):
    pass


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

        def _pre_order(node, visit):
            if node is None:
                pass

            else:
                visit(node)
                _pre_order(node.left, visit)
                _pre_order(node.right, visit)
        
        _pre_order(self.root, visit)
        

    def in_order(self, visit=lambda _node: print(_node.value)):
        """ L - N - R """

        def _in_order(node, visit):
            if node is None:
                pass

            else:
                _in_order(node.left, visit)
                visit(node)
                _in_order(node.right, visit)
        
        _in_order(self.root, visit)


    def post_order(self, visit=lambda _node: print(_node.value)):
        """ L - R - N """

        def _post_order(node, visit):
            if node is None:
                pass

            else:
                _post_order(node.left, visit)
                _post_order(node.right, visit)
                visit(node)

        _post_order(self.root, visit)


class BFSMixin:
    """add-on Mix-in class including BFS (Breath-First Search) methods
    
    Trees can also be traversed in level-order, where we visit every node on a level before going to a lower level. 
    This search is referred to as breadth-first search (BFS), as the search tree is broadened as much as possible 
    on each depth before going to the next depth.
    """

    def level_order(self, visit=lambda _node: print(_node.value)):

        def _level_order(node, visit):
            q = Queue()
            q.enqueue(node)
            while not q.is_empty:
                node = q.dequeue()
                if node is not None:
                    visit(node)
                    if node.left is not None:
                        q.enqueue(node.left)

                    if node.right is not None:
                        q.enqueue(node.right)
        
        _level_order(self.root, visit)


class Node(object):
    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.balance_factor = 0

    def __repr__(self):
        return f'<{self.left or "*"} <-{self.key}-> {self.right or "*"}>'


class BinarySearchTree(DFSMixin, BFSMixin):
    def __init__(self):
        self.root = None


    def find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current


    def swap(self, node, another):
        if node.parent is not None:
            if node == node.parent.left:
                node.parent.left = another
            else:
                node.parent.right = another
        
        if another:
            another.parent = node.parent


    def _find_value(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return current

            current = current.left if key < current.key else current.right
        return None


    def _insert_value(self, node, key, value, parent=None):
        inserted = False

        if node is None:
            node = Node(key, value, parent=parent)
            inserted = True

        else:
            if key == node.key:
                return None, inserted

            elif key < node.key:
                node.left, inserted = self._insert_value(node.left, key, value, node)
            else:
                node.right, inserted = self._insert_value(node.right, key, value, node)

        return node, inserted
        
        
    def _delete_value(self, node, key):
        if node is None:
            return node, False

        deleted = False
        if key == node.key:
            deleted = True
            if node.left and node.right:
                # replace the node to the leftmost of node.right
                parent, child = node, node.right
                while child.left is not None:
                    parent, child = child, child.left
                child.left = node.left
                if parent != node:
                    parent.left = child.right
                    child.right = node.right
                node = child
            elif node.left or node.right:
                node = node.left or node.right
            else:
                node = None
        elif key < node.key:
            node.left, deleted = self._delete_value(node.left, key)
        else:
            node.right, deleted = self._delete_value(node.right, key)
        return node, deleted
    

    def find(self, key):
        return self._find_value(key)


    def insert(self, key, value):
        self.root, inserted = self._insert_value(self.root, key, value)
        return inserted


    def delete(self, key):
        self.root, deleted = self._delete_value(self.root, key)
        return deleted


class AVLBinarySearchTree(BinarySearchTree):
    def rotate_left(self, subroot, node):
        self.swap(subroot.right, node.left)
        self.swap(node.left, subroot)

        if node.balance_factor == 0:
            subroot.balance_factor += 1
            node.balance_factor -= 1
        else:
            subroot.balance_factor = 0
            node.balance_factor = 0

        return node


    def rotate_right(self, subroot, node):
        self.swap(subroot.left, node.right)
        self.swap(node.right, subroot)

        if node.balance_factor == 0:
            subroot.balance_factor -= 1
            node.balance_factor += 1
        else:
            subroot.balance_factor = 0
            node.balance_factor = 0

        return node


    def rotate_right_left(self, subroot, node):
        self.swap(node.left.left, node.right)
        self.swap(node.right, node.left)

        self.swap(subroot.right, node.left.left)
        self.swap(node.left.left, subroot)

        if node.left.balance_factor == 0:
            subroot.balance_factor = 0
            node.balance_factor = 0
        elif node.left.balance_factor > 0:
            subroot.balance_factor -= 1
            node.balance_factor = 0
        else:
            subroot.balance_factor = 0
            node.balance_factor += 1

        node.left.balance_factor = 0
        return node.left


    def rotate_left_right(self, subroot, node):
        self.swap(node.right.right, node.left)
        self.swap(node.left, node.right)

        self.swap(subroot.left, node.right.right)
        self.swap(node.right.right, subroot)

        if node.right.balance_factor == 0:
            subroot.balance_factor = 0
            node.balance_factor = 0
        elif node.right.balance_factor > 0:
            subroot.balance_factor += 1
            node.balance_factor = 0
        else:
            subroot.balance_factor = 0
            node.balance_factor -= 1

        node.right.balance_factor = 0
        return node.right


    def _insert_rebalancing(self, child_inserted):
        pass

    def _delete_rebalancing(self, child_deleted):
        pass


if __name__ == '__main__':
    array = [40, 4, 34, 45, 14, 55, 48, 13, 15, 49, 47]

    bst = BinarySearchTree()
    for x in array:
        bst.insert(x, x)

    print(bst.root)
    print(bst.find(15)) # True
    print(bst.find(17)) # False

    # # depth first
    # bst.pre_order()   # 40 4 34 14 13 15 45 55 48 47 49
    # bst.in_order()    # 4 13 14 15 34 40 45 47 48 49 55
    # bst.post_order()  # 13 15 14 34 4 47 49 48 55 45 40
    # # breadth first
    # bst.level_order() # 40 4 45 34 55 14 48 13 15 47 49

    # print(bst.delete(55)) # True
    

    # # depth first
    # bst.pre_order()   # 40 4 34 14 13 15 45 48 47 49
    # bst.in_order()    # 4 13 14 15 34 40 45 47 48 49
    # bst.post_order()  # 13 15 14 34 4 47 49 48 45 40
    # # breadth first
    # bst.level_order() # 40 4 45 34 48 14 47 49 13 15

    # print(bst.delete(14)) # True
    # print(bst.root)

    # # depth first
    # bst.pre_order()   # 40 4 34 15 13 45 48 47 49
    # bst.in_order()    # 4 13 15 34 40 45 47 48 49
    # bst.post_order()  # 13 15 34 4 47 49 48 45 40
    # # breadth first
    # bst.level_order() # 40 4 45 34 48 15 47 49 13

    # print(bst.delete(11)) # False

    # # depth first
    # bst.pre_order()   # 40 4 34 15 13 45 48 47 49
    # bst.in_order()    # 4 13 15 34 40 45 47 48 49
    # bst.post_order()  # 13 15 34 4 47 49 48 45 40
    # # breadth first
    # bst.level_order() # 40 4 45 34 48 15 47 49 13