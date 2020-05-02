class Node(object):
    def __init__(self, is_red, key, value, lch=None, rch=None, parent=None):
        self.is_red = is_red
        self.key = key
        self.value = value
        self.lch = lch  # left child
        self.rch = rch  # right child
        self.parent = parent

    @property
    def sibling(self):
        if self.parent is None:
            return None
        if self is self.parent.lch:
            return self.parent.rch
        elif self is self.parent.rch:
            return self.parent.lch
        else:
            raise Exception('Unrecognized Parent-Child Relationship')

    @property
    def aunt(self):
        """
        Get the node which is sibling with the parent of the current node.
        :return: aunt node of the current node
        """
        if self.parent is None:
            return None
        if self.grandparent is None:
            return None

        # Check whether the parent is the left child or right child.
        if self.parent is self.grandparent.lch:
            return self.grandparent.rch
        if self.parent is self.grandparent.rch:
            return self.grandparent.lch
        return None

    @property
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def replace_child_of_parent(self, new_child):
        """
        Replace the current node in its relationship with its parent,
        using a new child node.
        """
        if self.parent is not None:
            if self is self.parent.lch:
                self.parent.lch = new_child
            elif self is self.parent.rch:
                self.parent.rch = new_child
            else:
                raise Exception('Unrecognized Parent-Child Relationship')
            new_child.parent = self.parent

    def replace_node_with_child(self):
        """
        Replace the current node with its only child or None.
        """
        if self.lch is None and self.rch is None:
            self.replace_child_of_parent(None)
        elif self.lch is not None and self.rch is not None:
            raise Exception('Cannot replace node with both children')
        elif self.lch is not None:
            self.replace_child_of_parent(self.lch)
        else:
            self.replace_child_of_parent(self.rch)

    @property
    def only_child(self):
        if self.lch is None and self.rch is None:
            raise Exception('Current node has no child')
        elif self.lch is not None and self.rch is not None:
            raise Exception('Current node has both children')
        elif self.lch is not None:
            return self.lch
        else:
            return self.rch


class RedBlackTree(object):
    """
    Red Black Tree, implemented according to description on Wikipedia.
    """
    def __init__(self, comp=lambda x, y: x < y):
        self.root = None
        self.comp = comp

    def _rotate_left(self, anchor):
        if anchor.rch is None:
            raise Exception('Empty (leaf) node can not become internal')
        new_anchor = anchor.rch
        parent = anchor.parent
        anchor.rch = new_anchor.lch
        new_anchor.lch = anchor

        # Fix the parent references.
        anchor.parent = new_anchor
        if anchor.rch is not None:
            anchor.rch.parent = anchor

        # Fix child references.
        if parent is not None:
            anchor.replace_child_of_parent(new_anchor)
        else:
            self.root = new_anchor

    def _rotate_right(self, anchor):
        if anchor.lch is None:
            raise Exception('Empty (leaf) node can not become internal')
        new_anchor = anchor.lch
        parent = anchor.parent
        anchor.lch = new_anchor.rch
        new_anchor.rch = anchor

        # Fix the parent references.
        anchor.parent = new_anchor
        if anchor.lch is not None:
            anchor.lch.parent = anchor

        # Fix child references.
        if parent is not None:
            anchor.replace_child_of_parent(new_anchor)
        else:
            self.root = new_anchor

    def _rotate_up(self, node):
        """
        Rotate the tree anchored on the parent of the node to make the node
        the new parent.
        """
        if node.parent is None:
            raise Exception('Current node has no parent')
        if node is node.parent.lch:
            self._rotate_left(node.parent)
        elif node is node.parent.rch:
            self._rotate_right(node.parent)
        else:
            raise Exception('Unrecognized Parent-Child Relationship')

    def _find(self, key):
        node = self.root
        while node is not None:
            if self.comp(node.key, key):  # left branch
                if node.lch is None:
                    return node
                node = node.lch
            else:                         # right branch
                if node.rch is None:
                    return node
                node = node.rch
        return node

    def _insert(self, new_node):

        # Construct a new tree if it is currently empty.
        if self.root is None:
            self.root = new_node
            return

        # Insert the new node according to the rule of a BST.
        node = self._find(new_node.key)
        if node.lch is None:
            node.lch = new_node
        elif node.rch is None:
            node.rch = new_node
        else:
            raise Exception('_find returns a non-leaf position for insertion')
        new_node.parent = node
        self._balance_insert(new_node)

    def _balance_insert(self, new_node):

        # The new node is the root.
        if new_node.parent is None:
            new_node.is_red = False
            return

        # The parent node is black.
        if not new_node.parent.is_red:
            return

        # The parent and the aunt are both red.
        if new_node.aunt is not None and new_node.parent.is_red and \
                new_node.aunt.is_red:
            new_node.parent.is_red = False
            new_node.aunt.is_red = False
            new_node.grandparent.is_red = True
            self._balance_insert(new_node.grandparent)
            return

        # The parent is red but the aunt is black (including leaves).
        # Rotate the inside node to the outside of the subtree.
        if new_node is new_node.parent.rch and new_node.parent is \
                new_node.grandparent.lch:
            self._rotate_left(new_node.parent)
            new_node = new_node.lch
        elif new_node is new_node.parent.lch and new_node.parent is \
                new_node.grandparent.rch:
            self._rotate_right(new_node.parent)
            new_node = new_node.rch
        # Rotate the node upwards.
        if new_node is new_node.parent.lch:
            self._rotate_right(new_node.grandparent)
        else:
            self._rotate_left(new_node.grandparent)
        new_node.parent.is_red = False
        new_node.grandparent.is_red = True

    def add(self, key, value):
        new_node = Node(is_red=True, key=key, value=value)
        self._insert(new_node)

    def _balance_delete(self, node):
        """
        Balance the tree for the case where we removed a black node from the
        subtree rooted at the node given.
        """
        # If the node is the root of the whole tree, one black node was removed
        # from every path, so properties will be preserved -> finish.
        if node.parent is None:
            self.root = node
            return

        # Otherwise, we will need to check the color of the sibling.
        if node.sibling.is_red:

            # For a red sibling, we swap the color of the sibling with parent.
            node.sibling.is_red = False
            node.parent.is_red = True

            # Then rotate to make the sibling the new parent.
            self._rotate_up(node.sibling)
        else:
            # For a black sibling, we check the colors of its children.
            if not node.sibling.lch.is_red and not node.sibling.rch.is_red:

                # Both children are black, check the parent.
                if not node.parent.is_red:

                    # Parent is also black, flip the sibling and recurse on
                    # the parent.
                    node.sibling.is_red = True
                    self._balance_delete(node.parent)
                else:
                    # Parent is red, exchange colours of parent and sibling.
                    node.sibling.is_red = True
                    node.parent.is_red = False
            elif node is node.parent.lch and node.sibling.lch.is_red and not \
                    node.sibling.rch.is_red:

                # Swap colours of sibling and its left child and rotate right.
                node.sibling.is_red = True
                node.sibling.lch.is_red = False
                self._rotate_right(node.sibling)
            elif node is node.parent.rch and not node.sibling.lch.is_red and \
                    node.sibling.rch.is_red:

                # Swap colours of sibling and its right child and rotate left.
                node.sibling.is_red = True
                node.sibling.rch.is_red = False
                self._rotate_left(node.sibling)
            else:
                # The red child of the sibling is on the opposite side to our
                # target node.
                node.sibling.is_red = node.parent.is_red
                node.parent.is_red = False
                if node is node.parent.lch:
                    node.sibling.rch.is_red = False
                    self._rotate_left(node.parent)
                else:
                    node.sibling.lch.is_red = False
                    self._rotate_right(node.parent)

    def _delete(self, target_node):

        # In the case where the target node does not have the same key,
        # copy the node to cover the node to delete.
        node = target_node
        while node is not None and node.key != target_node.key:
            node = node.parent
        if node is None:  # the key can not be found in the tree
            return
        node.key, node.value = target_node.key, target_node.value  # copy over

        # Remove the target node.
        # Step 1: replace the target node with its only child
        child = target_node.only_child
        target_node.replace_node_with_child()

        # Step 2: for black target node, we check its child
        if not target_node.is_red:

            # Step 2.1: for red child, we flip its colour
            if child.is_red:
                child.is_red = False

            # Step 2.2: for black child, we balance the tree further
            else:
                self._balance_delete(child)

    def remove(self, key):
        target_node = self._find(key)  # find the target node
        self._delete(target_node)

    def first(self):
        if self.root is None:
            return None
        node = self.root
        while node.lch is not None:
            node = node.lch
        return node.key, node.value

    def pop(self):
        first_node = self.first()
        self.remove(first_node[0])
        return first_node
