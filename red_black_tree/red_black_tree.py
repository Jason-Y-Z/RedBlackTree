from collections import deque


class Node(object):
    def __init__(self, is_red, key, value, lch=None, rch=None, parent=None):
        self.is_red = is_red
        self.key = key
        self.value = value
        self.lch = lch  # left child
        self.rch = rch  # right child
        self.parent = parent

    def __str__(self):
        return f'[{"R" if self.is_red else "B"}, {self.key}, {self.value}, ' \
               f'{None if self.lch is None else self.lch.key}, ' \
               f'{None if self.rch is None else self.rch.key}, ' \
               f'{None if self.parent is None else self.parent.key}]'

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

    @property
    def only_child(self):
        if self.lch is None and self.rch is None:

            # If it has no non-leaf child, return a leaf node.
            return Node(is_red=False, key=None, value=None, parent=self)
        if self.lch is not None and self.rch is not None:
            raise Exception('Current node has both children')
        return self.lch if self.lch else self.rch


class RedBlackTree(object):
    """
    Red Black Tree, implemented according to description on Wikipedia.
    """

    def __init__(self, comp=lambda x, y: x < y):
        """
        Initialise a red black tree with given comparator.
        :param comp: comparator to compare the keys of the nodes in the tree
        """
        self.root = None
        self.comp = comp

    def __str__(self):
        if self.root is None:
            return ''

        # Initialise the search queue.
        level = 0  # level of the current node
        level_str = ''
        node_queue = deque()
        node_queue.append((self.root, level))
        tree_str = ''

        # Since we add None strings in place of empty nodes, we need this
        # flag to keep track of whether next level has non-empty nodes.
        next_level_flag = True
        EMPTY_NODE = Node(False, None, None)

        # BFS
        while len(node_queue) > 0:
            node, node_level = node_queue.popleft()

            # Create a newline in the string when reaching the next level.
            if node_level > level:
                if not next_level_flag:  # no non-empty node on this level
                    break
                tree_str += level_str + '\n'
                level = node_level
                level_str = ''
                next_level_flag = False

            # Add the current node to the current layer.
            level_str += str(node)
            if node.lch is None:
                node_queue.append((EMPTY_NODE, level + 1))
            else:
                next_level_flag = True
                node_queue.append((node.lch, level + 1))
            if node.rch is None:
                node_queue.append((EMPTY_NODE, level + 1))
            else:
                next_level_flag = True
                node_queue.append((node.rch, level + 1))
        return tree_str

    def add(self, key, value):
        """
        Add a new node to the tree, with given key and value.
        """
        new_node = Node(is_red=True, key=key, value=value)
        self._insert(new_node)

    def remove(self, key):
        """
        Remove an existing node from the tree, with given key.
        """
        # Find the target node, which is the largest node smaller than or
        # equal to the node to delete.
        target_node = self._find(key)

        # In the case where the target node found does not have the same key,
        # copy the target node to cover the node to delete.
        node = target_node
        while node is not None and node.key != key:
            node = node.parent
        if node is None:  # the key can not be found in the tree
            return
        node.key, node.value = target_node.key, target_node.value  # copy over
        self._delete(target_node)

    def first(self):
        """
        Find the first node with 'smallest' key according to the given
        comparator of the tree.
        :return: key and value of the first node as a tuple, None if tree empty
        """
        if self.root is None:
            return None
        node = self.root
        while node.lch is not None:
            node = node.lch
        return node.key, node.value

    def pop(self):
        """
        Find the first node and remove it from the tree.
        :return: key and value of the first node as a tuple, None if tree empty
        """
        first_node = self.first()
        if first_node is None:
            return None
        self.remove(first_node[0])
        return first_node

    def _replace_child_of_parent(self, node, new_child):
        """
        Replace the current node with a new child node (in its relationship
        with its parent).
        """
        parent = node.parent
        if parent:

            # Replace the left/right child reference accordingly.
            if parent.lch and node.key == parent.lch.key:
                parent.lch = new_child
            elif parent.rch and node.key == parent.rch.key:
                parent.rch = new_child
            else:
                raise Exception('Unrecognized Parent-Child Relationship')
        else:

            # Parent is None means the current node is the root.
            self.root = new_child
        if new_child is not None:

            # Update the new child's parent reference.
            new_child.parent = parent

    def _rotate_left(self, anchor):
        """
        Rotate the subtree, rooted at the anchor, leftwards.
        """
        if anchor.rch is None:
            raise Exception(
                'Root of the left-rotating subtree has an empty right child')
        new_anchor = anchor.rch
        anchor.rch = new_anchor.lch
        new_anchor.lch = anchor

        # Update the parent/child references.
        self._replace_child_of_parent(anchor, new_anchor)
        anchor.parent = new_anchor
        if anchor.rch:
            anchor.rch.parent = anchor

    def _rotate_right(self, anchor):
        """
        Rotate the subtree, rooted at the anchor, rightwards.
        """
        if anchor.lch is None:
            raise Exception(
                'Root of the right-rotating subtree has an empty left child')
        new_anchor = anchor.lch
        anchor.lch = new_anchor.rch
        new_anchor.rch = anchor

        # Update the parent/child references.
        self._replace_child_of_parent(anchor, new_anchor)
        anchor.parent = new_anchor
        if anchor.lch:
            anchor.lch.parent = anchor

    def _rotate_up(self, node):
        """
        Rotate the tree anchored on the parent of the node to make the node
        the new parent.
        """
        if node.parent is None:
            raise Exception('Current node has no parent')
        if node is node.parent.lch:
            self._rotate_right(node.parent)
        elif node is node.parent.rch:
            self._rotate_left(node.parent)
        else:
            raise Exception('Unrecognized Parent-Child Relationship')

    def _find(self, key):
        """
        Find the largest node with key smaller than or equal to target key.
        """
        node = self.root
        while node is not None:
            if self.comp(key, node.key):  # left branch
                if node.lch is None:
                    return node
                node = node.lch
            else:                         # right branch
                if node.rch is None:
                    return node
                node = node.rch
        return node

    def _insert(self, new_node):
        """
        Insert a new node into the red black tree.
        """

        # Construct a new tree if it is currently empty.
        if self.root is None:
            new_node.is_red = False
            self.root = new_node
            return

        # Insert the new node according to the rule of a Binary Search Tree.
        node = self._find(new_node.key)
        if self.comp(new_node.key, node.key) and node.lch is None:
            node.lch = new_node
        elif not self.comp(new_node.key, node.key) and node.rch is None:
            node.rch = new_node
        else:
            raise Exception('_find returns a non-leaf position for insertion')
        new_node.parent = node

        # Balance the tree after the insertion.
        self._balance_insert(new_node)

    def _balance_insert(self, new_node):
        """
        Balance the tree after insertion.
        """

        # The current node is root.
        if new_node.parent is None:
            new_node.is_red = False  # root must be black
            self.root = new_node
            return

        # The parent node is black, adding a red child is fine.
        if not new_node.parent.is_red:
            return

        # The parent and the aunt are both red.
        if new_node.aunt and new_node.aunt.is_red:

            # Swap colours of aunt and parent with grandparent.
            new_node.parent.is_red = False
            new_node.aunt.is_red = False
            new_node.grandparent.is_red = True

            # Recurse on grandparent.
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

        # Rotate the parent node upwards.
        grandparent = new_node.grandparent
        self._rotate_up(new_node.parent)

        # The parent has now become parent of grandparent and current node.
        # Swap its color with the grandparent node.
        new_node.parent.is_red = False
        grandparent.is_red = True

    def _delete(self, target_node):
        """
        Delete a node from the tree.
        """

        # Replace the target node with its only child.
        child = target_node.only_child
        self._replace_child_of_parent(target_node, child)

        # For black target node, we check its child.
        if not target_node.is_red:

            # For red child, we flip its colour.
            if child.is_red:
                child.is_red = False

            # For black child, we balance the tree further.
            else:
                self._balance_delete(child)

        # Remove the empty (leaf) node from our representation.
        if child.key is None:
            self._replace_child_of_parent(child, None)

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
        if node.sibling and node.sibling.is_red:

            # For a red sibling, we swap the color of the sibling with parent.
            node.sibling.is_red = False
            node.parent.is_red = True

            # Then rotate to make the sibling the new parent.
            self._rotate_up(node.sibling)

        # For black parent, sibling and sibling's children.
        if not node.parent.is_red and not node.sibling.is_red \
                and (node.sibling.lch is None or not node.sibling.lch.is_red) \
                and (node.sibling.rch is None or not node.sibling.rch.is_red):

            # Flip the sibling and recurse on the parent.
            node.sibling.is_red = True
            self._balance_delete(node.parent)

        # For red parent, black sibling (implied) and sibling's children.
        elif node.parent.is_red \
                and (node.sibling.lch is None or not node.sibling.lch.is_red) \
                and (node.sibling.rch is None or not node.sibling.rch.is_red):

            # Exchange colours of parent and sibling.
            node.sibling.is_red = True
            node.parent.is_red = False
        else:
            # For black sibling (implied) and sibling right child, red sibling
            # left child (implied), node being the left child of parent.
            if node is node.parent.lch and \
                    (node.sibling.rch is None or not node.sibling.rch.is_red):

                # Swap colours of sibling and its left child.
                node.sibling.is_red = True
                node.sibling.lch.is_red = False
                self._rotate_right(node.sibling)
            # For black sibling (implied) and sibling left child, red sibling
            # right child (implied), node being the right child of parent.
            elif node is node.parent.rch and \
                    (node.sibling.lch is None or not node.sibling.lch.is_red):

                # Swap colours of sibling and its right child.
                node.sibling.is_red = True
                node.sibling.rch.is_red = False
                self._rotate_left(node.sibling)

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
