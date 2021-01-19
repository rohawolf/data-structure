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

        def _in_order(tree, visit):
            if tree is None:
                pass

            else:
                visit(tree.root)
                _pre_order(tree.left, visit)
                _pre_order(tree.right, visit)
        
        _pre_order(self, visit)
        

    def in_order(self, visit=lambda _node: print(_node.value)):
        """ L - N - R """

        def _in_order(tree, visit):
            if tree is None:
                pass

            else:
                _in_order(tree.left, visit)
                visit(tree.root)
                _in_order(tree.right, visit)
        
        _in_order(self, visit)
        

    def post_order(self, visit=lambda _node: print(_node.value)):
        """ L - R - N """

        def _post_order(tree, visit):
            if tree is None:
                pass

            else:
                _post_order(tree.left, visit)
                _post_order(tree.right, visit)
                visit(tree.root)
        
        _post_order(self, visit)


class BFSMixin:
    """add-on Mix-in class including BFS (Breath-First Search) methods
    
    Trees can also be traversed in level-order, where we visit every node on a level before going to a lower level. 
    This search is referred to as breadth-first search (BFS), as the search tree is broadened as much as possible 
    on each depth before going to the next depth.
    """

    def level_order(self, visit=lambda _node: print(_node.value)):

        def _level_order(tree, visit):
            q = Queue()
            q.enqueue(tree)
            while not q.is_empty:
                tree = q.dequeue()
                if tree is not None:
                    visit(tree.root)
                    if tree.left is not None:
                        q.enqueue(tree.left)

                    if tree.right is not None:
                        q.enqueue(tree.right)
        
        _level_order(self, visit)


class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f'{self.key}'


class Tree(object):
    def __init__(self, node=None, left=None, right=None, parent=None):
        self.root = node
        self.left = left
        self.right = right
        self.parent = parent
        self.balance_factor = 0

    def __repr__(self):
        left_subtree = self.left or ''
        right_subtree = self.right or ''
        root = '' if self.parent else 'root:'
        return f'({left_subtree}<-{root}{self.root}->{right_subtree})'


class BinarySearchTree(DFSMixin, BFSMixin):
    

    def __init__(self, node=None, left=None, right=None, parent=None):
        self.tree = Tree(node=None, left=None, right=None, parent=None)


    def __repr__(self):
        return str(self.tree)


    def find_min(self, tree):
        current = tree
        while current.left is not None:
            current = current.left
        return current


    def swap(self, tree, another):
        if tree is not None:
            if tree.parent is not None:
                if tree == tree.parent.left:
                    tree.parent.left = another
                else:
                    tree.parent.right = another
            
            if another:
                another.parent = tree.parent


    def _find_value(self, key):
        current = self.tree
        while current is not None:
            node = current.root
            if node is not None and key == node.key:
                return current

            current = current.left if key < node.key else current.right
        return None


    def _insert_value(self, tree, key, value, parent=None):
        node = Node(key, value)
        inserted = False

        if tree is None:
            tree = Tree(node, parent=parent)
            inserted = True

        elif tree.root is None:
            tree.root = node
            inserted = True

        else:
            node = tree.root
            if key == node.key:
                return None, inserted

            elif key < node.key:
                tree.left, inserted = self._insert_value(tree.left, key, value, tree)
            else:
                tree.right, inserted = self._insert_value(tree.right, key, value, tree)

        return tree, inserted
        
        
    def _delete_value(self, tree, key):
        deleted = False
        if tree is None:
            return tree, deleted
        
        _parent = tree.parent
        node = tree.root

        if key == node.key:
            deleted = True
            if tree.left and tree.right:
                # replace the node to the leftmost of node.right
                parent, child = tree, tree.right
                while child.left is not None:
                    parent, child = child, child.left
                child.left = tree.left
                if parent != tree:
                    parent.left = child.right
                    child.right = tree.right
                tree = child
            elif tree.left or tree.right:
                tree = tree.left or tree.right
            else:
                tree = None

        elif key < node.key:
            tree.left, deleted = self._delete_value(tree.left, key)
        else:
            tree.right, deleted = self._delete_value(tree.right, key)
        return tree, deleted
    

    def find(self, key):
        return self._find_value(key)


    def insert(self, key, value):
        self.tree, inserted = self._insert_value(self.tree, key, value)
        return inserted


    def delete(self, key):
        self.tree, deleted = self._delete_value(self.tree, key)
        return deleted


class AVLBinarySearchTree(BinarySearchTree):

    def rotate_left(self, sub_tree, heavy_tree, with_updating=True):
        sub_tree.right = heavy_tree.left
        if heavy_tree.left is not None:
            heavy_tree.left.parent = sub_tree
        heavy_tree.left = sub_tree
        sub_tree.parent = heavy_tree

        if with_updating:
            if heavy_tree.balance_factor == 0:
                sub_tree.balance_factor += 1
                heavy_tree.balance_factor -= 1
            else:
                sub_tree.balance_factor = 0
                heavy_tree.balance_factor = 0

        return heavy_tree


    def rotate_right(self, sub_tree, heavy_tree, with_updating=True):
        sub_tree.left = heavy_tree.right
        if heavy_tree.right is not None:
            heavy_tree.right.parent = sub_tree
        heavy_tree.right = sub_tree
        sub_tree.parent = heavy_tree

        if with_updating:
            if heavy_tree.balance_factor == 0:
                sub_tree.balance_factor -= 1
                heavy_tree.balance_factor += 1
            else:
                sub_tree.balance_factor = 0
                heavy_tree.balance_factor = 0

        return heavy_tree


    def rotate_right_left(self, sub_tree, heavy_tree):
        new_tree = self.rotate_left(
            sub_tree, 
            self.rotate_right(heavy_tree, heavy_tree.left, with_updating=False), 
            with_updating=False
        )

        if new_tree.balance_factor == 0:
            sub_tree.balance_factor = 0
            heavy_tree.balance_factor = 0
        elif new_tree.balance_factor > 0:
            sub_tree.balance_factor -= 1
            heavy_tree.balance_factor = 0
        else:
            sub_tree.balance_factor = 0
            heavy_tree.balance_factor += 1

        new_tree.balance_factor = 0
        return new_tree


    def rotate_left_right(self, sub_tree, heavy_tree):
        new_tree = self.rotate_right(
            sub_tree, 
            self.rotate_left(heavy_tree, heavy_tree.right, with_updating=False), 
            with_updating=False
        )
        
        if new_tree.balance_factor == 0:
            sub_tree.balance_factor = 0
            heavy_tree.balance_factor = 0
        elif new_tree.balance_factor > 0:
            sub_tree.balance_factor += 1
            heavy_tree.balance_factor = 0
        else:
            sub_tree.balance_factor = 0
            heavy_tree.balance_factor -= 1

        new_tree.balance_factor = 0
        return new_tree

    
    def _insert_rebalancing(self, inserted):
        _parent = inserted.parent
        _current = inserted
        
        while _parent is not None:
            _grandparent = _parent.parent
            _new_tree = None
            if _current == _parent.right:
                if _parent.balance_factor > 0:
                    if _current.balance_factor < 0:
                        _new_tree = self.rotate_right_left(_parent, _current)
                    else:
                        _new_tree = self.rotate_left(_parent, _current)
                else:
                    _parent.balance_factor += 1
                    if _parent.balance_factor == 0:
                        break
                    _parent, _current = _grandparent, _parent
                    continue
            else:
                if _parent.balance_factor < 0:
                    if _current.balance_factor > 0:
                        _new_tree = self.rotate_left_right(_parent, _current)
                    else:
                        _new_tree = self.rotate_right(_parent, _current)

                else:
                    _parent.balance_factor -= 1
                    if _parent.balance_factor == 0:
                        break
                    _parent, _current = _grandparent, _parent
                    continue
            
            _new_tree.parent = _grandparent
            if _grandparent is not None:
                if _parent == _grandparent.left:
                    _grandparent.left = _new_tree
                else:
                    _grandparent.right = _new_tree
            else:
                self.tree = _new_tree
            break
        

    def _delete_rebalancing(self, child_deleted):
        pass


    def insert(self, key, value):
        self.tree, is_inserted = self._insert_value(self.tree, key, value)
        if is_inserted:
            inserted = self.find(key)
            self._insert_rebalancing(inserted)
        return is_inserted


    def delete(self, key):
        self.tree, deleted = self._delete_value(self.tree, key)
        return deleted

if __name__ == '__main__':
    array = [40, 4, 34, 45, 14, 55, 48, 13, 15, 49, 47]

    # bst = BinarySearchTree()
    bst = AVLBinarySearchTree()
    for x in array:
        bst.insert(x, x)
        print(x, bst)
    # print(bst)
    bst.find(14) # True
    bst.find(17) # False

    # # depth first
    # bst.pre_order()   # 40 4 34 14 13 15 45 55 48 47 49
    # bst.in_order()    # 4 13 14 15 34 40 45 47 48 49 55
    # bst.post_order()  # 13 15 14 34 4 47 49 48 55 45 40
    # # breadth first
    # bst.level_order() # 40 4 45 34 55 14 48 13 15 47 49

    print(bst.delete(55)) # True
    print(bst)

    # # depth first
    # bst.pre_order()   # 40 4 34 14 13 15 45 48 47 49
    # bst.in_order()    # 4 13 14 15 34 40 45 47 48 49
    # bst.post_order()  # 13 15 14 34 4 47 49 48 45 40
    # # breadth first
    # bst.level_order() # 40 4 45 34 48 14 47 49 13 15

    # bst.delete(14) # True

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