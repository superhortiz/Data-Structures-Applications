from utils import RedBlackBST, RectHV
from typing import Iterator, Tuple
import matplotlib.pyplot as plt


class RectangleST(RedBlackBST):
    """
    Rectangle Search Tree using Red-Black BST.
    
    This implementation assumes the Non-degeneracy assumption, meaning all x- and y-coordinates
    are distinct, particularly the ymin value for a rectangle, which is used as the key.

    Methods:
        add(rectangle): Adds a rectangle to the Rectangle Search Tree.
        intersects(rectangle): Finds all rectangles that intersect with the given rectangle.
        print_tree(): Prints the RectangleST in a structured format.
    """

    class TreeNode(RedBlackBST.TreeNode):
        """
        Represents a node in the Rectangle Search Tree.

        Attributes:
            key (float): The key of the node.
            value (rectangle): The rectangle stored in the node.
            color (bool): The color of the node (Red or Black).
            count (int): The number of nodes in the subtree rooted at this node.
            max_end (float): The maximum end value in the subtree rooted at this node.
        """

        def __init__(self, key: float, value: 'rectangle', color: bool, count: int, max_end: float) -> None:
            """
            Initializes a TreeNode instance.

            Args:
                key (float): The key of the node.
                value (rectangle): The rectangle stored in the node.
                color (bool): The color of the node (Red or Black).
                count (int): The number of nodes in the subtree rooted at this node.
                max_end (float): The maximum end value in the subtree rooted at this node.
            """

            super().__init__(key, value, color, count)
            self.max_end = max_end

        def update_max_end(self) -> None:
            """
            Updates the max_end attribute to the maximum end value in the subtree.
            """
            self.max_end = max(self.value.ymax,
                               self.left.max_end if self.left else self.value.ymax,
                               self.right.max_end if self.right else self.value.ymax)

    def __init__(self) -> None:
        """
        Initializes an RectangleST instance.
        """
        super().__init__()

    def add(self, rectangle: RectHV) -> None:
        """
        Adds an rectangle to the rectangle Search Tree.

        Args:
            rectangle (rectangle): The rectangle to add.
        """

        key = rectangle.ymin
        self._root = self._add(self._root, key, rectangle)

        # Set the root Black
        self._root.color = RedBlackBST.BLACK
        
    def _rotate_left(self, current_node: 'RectangleST.TreeNode') -> 'RectangleST.TreeNode':
        """
        Performs a left rotation on the given node.

        Args:
            current_node (RectangleST.TreeNode): The node to rotate.

        Returns:
            RectangleST.TreeNode: The new root after rotation.
        """

        new_root = super()._rotate_left(current_node)
        new_root.update_max_end()
        current_node.update_max_end()
        return new_root

    def _rotate_right(self, current_node: 'RectangleST.TreeNode') -> 'RectangleST.TreeNode':
        """
        Performs a right rotation on the given node.

        Args:
            current_node (RectangleST.TreeNode): The node to rotate.

        Returns:
            RectangleST.TreeNode: The new root after rotation.
        """

        new_root = super()._rotate_right(current_node)
        new_root.update_max_end()
        current_node.update_max_end()
        return new_root

    def _balance(self, node: 'RectangleST.TreeNode') -> 'RectangleST.TreeNode':
        """
        Balances the subtree rooted at the given node.

        Args:
            node (RectangleST.TreeNode): The node to balance.

        Returns:
            RectangleST.TreeNode: The balanced node.
        """

        node = super()._balance(node)
        node.update_max_end()
        return node

    def _add(self, node: 'RectangleST.TreeNode', key: float, value: RectHV) -> 'RectangleST.TreeNode':
        """
        Adds a new node with the given key and value to the subtree rooted at the given node.

        Args:
            node (RectangleST.TreeNode): The root of the subtree.
            key (float): The key of the new node.
            value (rectangle): The value of the new node.

        Returns:
            RectangleST.TreeNode: The root of the subtree after adding the new node.
        """

        # End of the tree reached, return a new TreeNode and color it RED
        if node is None:
            return self.TreeNode(key, value, RedBlackBST.RED, 1, value.ymax)

        # Explore recursively the left child
        if key < node.key:
            node.left = self._add(node.left, key, value)

        # Explore recursively the right child
        elif key > node.key:
            node.right = self._add(node.right, key, value)

        # The key is already in the tree, ovewrite the value
        elif key == node.key:
            node.value = value

        # Lean left
        if self._is_red(node.right) and not self._is_red(node.left):
            node = self._rotate_left(node)

        # Balance 4-node
        if self._is_red(node.left) and self._is_red(node.left.left):
            node = self._rotate_right(node)

        # Split 4-node
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(node)

        # Update the count
        node.count = 1 + self._size(node.left) + self._size(node.right)

        # Update the maximum value in the subtree
        node.update_max_end()

        # Return the corresponding link to the node
        return node

    def intersects(self, rectangle: RectHV) -> Iterator['rectangle']:
        """
        Finds all rectangles that intersect with the given rectangle.

        Args:
            rectangle (rectangle): The rectangle to check intersections with.

        Yields:
            rectangle: Each intersecting rectangle.
        """

        yield from self._intersects(self._root, rectangle)

    def _intersects(self, node: 'RectangleST.TreeNode', rectangle: RectHV) -> Iterator[RectHV]:
        """
        Helper method to find all rectangles that intersect with the given rectangle in the subtree rooted at the given node.

        Args:
            node (RectangleST.TreeNode): The root of the subtree.
            rectangle (rectangle): The rectangle to check intersections with.

        Yields:
            rectangle: Each intersecting rectangle.
        """

        if node is None:
            return

        # Check if the current node's rectangle intersects with the given rectangle
        if node.value.intersects(rectangle):
            yield node.value

        # Traverse the left subtree if it might contain intersecting rectangles
        if node.left and node.left.max_end >= rectangle.ymin:
            yield from self._intersects(node.left, rectangle)

        # Traverse the right subtree if it might contain intersecting rectangles
        if node.right and node.right.max_end >= rectangle.ymin:
            yield from self._intersects(node.right, rectangle)

    def print_tree(self) -> None:
        """
        Prints the RectangleST in a structured format.
        """
        self._print_tree(self._root)

    def _print_tree(self, node = None, level: int = 0, prefix: str = "Root: ") -> None:
        """
        Helper method to print the RectangleST in a structured format.

        Args:
            node (RectangleST.TreeNode): The root of the subtree.
            level (int): The current level in the tree (used for indentation).
            prefix (str): The prefix to print before the node value.
        """
        if node is not None:
            print(f"{' ' * (level * 4)}{prefix} {node.value}, max_subtree = {node.max_end}")
            if node.left:
                self._print_tree(node.left, level + 1, "L-->")
            if node.right:
                self._print_tree(node.right, level + 1, "R-->")
