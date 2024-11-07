from utils import RedBlackBST
from typing import Iterator, Tuple
import matplotlib.pyplot as plt


class IntervalST(RedBlackBST):
    """
    Interval Search Tree using Red-Black BST.
    
    This algorithm works under the Nondegeneracy assumption (No two intervals have the same left endpoint).

    Methods:
        add(interval): Adds an interval to the Interval Search Tree.
        intersects(interval): Finds all intervals that intersect with the given interval.
        print_tree(): Prints the IntervalST in a structured format.
    """

    class TreeNode(RedBlackBST.TreeNode):
        """
        Represents a node in the Interval Search Tree.

        Attributes:
            key (float): The key of the node.
            value (Interval): The interval stored in the node.
            color (bool): The color of the node (Red or Black).
            count (int): The number of nodes in the subtree rooted at this node.
            max_end (float): The maximum end value in the subtree rooted at this node.
        """

        def __init__(self, key: float, value: 'Interval', color: bool, count: int, max_end: float) -> None:
            """
            Initializes a TreeNode instance.

            Args:
                key (float): The key of the node.
                value (Interval): The interval stored in the node.
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
            self.max_end = max(self.value.end,
                               self.left.max_end if self.left else self.value.end,
                               self.right.max_end if self.right else self.value.end)

    def __init__(self) -> None:
        """
        Initializes an IntervalST instance.
        """
        super().__init__()

    def add(self, interval: 'Interval') -> None:
        """
        Adds an interval to the Interval Search Tree.

        Args:
            interval (Interval): The interval to add.
        """

        key = interval.start
        self._root = self._add(self._root, key, interval)

        # Set the root Black
        self._root.color = RedBlackBST.BLACK
        
    def _rotate_left(self, current_node: 'IntervalST.TreeNode') -> 'IntervalST.TreeNode':
        """
        Performs a left rotation on the given node.

        Args:
            current_node (IntervalST.TreeNode): The node to rotate.

        Returns:
            IntervalST.TreeNode: The new root after rotation.
        """

        new_root = super()._rotate_left(current_node)
        new_root.update_max_end()
        current_node.update_max_end()
        return new_root

    def _rotate_right(self, current_node: 'IntervalST.TreeNode') -> 'IntervalST.TreeNode':
        """
        Performs a right rotation on the given node.

        Args:
            current_node (IntervalST.TreeNode): The node to rotate.

        Returns:
            IntervalST.TreeNode: The new root after rotation.
        """

        new_root = super()._rotate_right(current_node)
        new_root.update_max_end()
        current_node.update_max_end()
        return new_root

    def _balance(self, node: 'IntervalST.TreeNode') -> 'IntervalST.TreeNode':
        """
        Balances the subtree rooted at the given node.

        Args:
            node (IntervalST.TreeNode): The node to balance.

        Returns:
            IntervalST.TreeNode: The balanced node.
        """

        node = super()._balance(node)
        node.update_max_end()
        return node

    def _add(self, node: 'IntervalST.TreeNode', key: float, value: 'Interval') -> 'IntervalST.TreeNode':
        """
        Adds a new node with the given key and value to the subtree rooted at the given node.

        Args:
            node (IntervalST.TreeNode): The root of the subtree.
            key (float): The key of the new node.
            value (Interval): The value of the new node.

        Returns:
            IntervalST.TreeNode: The root of the subtree after adding the new node.
        """

        # End of the tree reached, return a new TreeNode and color it RED
        if node is None:
            return self.TreeNode(key, value, RedBlackBST.RED, 1, value.end)

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

    def intersects(self, interval: 'Interval') -> Iterator['Interval']:
        """
        Finds all intervals that intersect with the given interval.

        Args:
            interval (Interval): The interval to check intersections with.

        Yields:
            Interval: Each intersecting interval.
        """

        yield from self._intersects(self._root, interval)

    def _intersects(self, node: 'IntervalST.TreeNode', interval: 'Interval') -> Iterator['Interval']:
        """
        Helper method to find all intervals that intersect with the given interval in the subtree rooted at the given node.

        Args:
            node (IntervalST.TreeNode): The root of the subtree.
            interval (Interval): The interval to check intersections with.

        Yields:
            Interval: Each intersecting interval.
        """

        if node is None:
            return

        # Check if the current node's interval intersects with the given interval
        if node.value.intersects(interval):
            yield node.value

        # Traverse the left subtree if it might contain intersecting intervals
        if node.left and node.left.max_end >= interval.start:
            yield from self._intersects(node.left, interval)

        # Traverse the right subtree if it might contain intersecting intervals
        if node.right and node.right.max_end >= interval.start:
            yield from self._intersects(node.right, interval)

    def print_tree(self) -> None:
        """
        Prints the IntervalST in a structured format.
        """
        self._print_tree(self._root)

    def _print_tree(self, node = None, level: int = 0, prefix: str = "Root: ") -> None:
        """
        Helper method to print the IntervalST in a structured format.

        Args:
            node (IntervalST.TreeNode): The root of the subtree.
            level (int): The current level in the tree (used for indentation).
            prefix (str): The prefix to print before the node value.
        """
        if node is not None:
            print(f"{' ' * (level * 4)}{prefix} {node.value}, max_subtree = {node.max_end}")
            if node.left:
                self._print_tree(node.left, level + 1, "L-->")
            if node.right:
                self._print_tree(node.right, level + 1, "R-->")


class Interval:
    """
    Represents an interval with a start and end point.

    Attributes:
        start (float): The start point of the interval.
        end (float): The end point of the interval.

    Methods:
        intersects(other): Determines if this interval intersects with another interval.
        draw(y_coordinate: float, color): Draws the interval as a horizontal line with vertical
        markers at the start and end points.

    Special Methods:
        __lt__(other): Compares this interval with another interval for sorting.
        __repr__(): Returns a string representation of the interval.
    """

    def __init__(self, interval: Tuple[float, float]) -> None:
        """
        Initializes an Interval instance.

        Args:
            interval (tuple[float, float]): A tuple containing the start and end points of the interval.
        """

        self.start = min(interval)
        self.end = max(interval)

    def intersects(self, other: 'Interval') -> bool:
        """
        Determines if this interval intersects with another interval.

        Args:
            other (Interval): Another interval to check for intersection.

        Returns:
            bool: True if the intervals intersect, False otherwise.
        """

        return not (self.end < other.start or self.start > other.end)

    def draw(self, y_coordinate: float, color: str) -> None:
        """
        Draws the interval as a horizontal line with vertical markers at the start and end points.

        Args:
            y_coordinate (float): The y-coordinate at which to draw the interval.
            color (str): The color of the line and markers.
        """

        plt.plot([self.start, self.end], [y_coordinate, y_coordinate], color = color)
        plt.plot(self.start, y_coordinate, '|', color = color)
        plt.plot(self.end, y_coordinate, '|', color = color)

    def __lt__(self, other: 'Interval') -> bool:
        """
        Compares this interval with another interval for sorting.

        Args:
            other (Interval): Another interval to compare with.

        Returns:
            bool: True if this interval is less than the other interval, False otherwise.
        """

        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start

    def __repr__(self) -> str:
        """
        Returns a string representation of the interval.

        Returns:
            str: A string representation of the interval.
        """

        return f"{self.__class__.__name__}(({self.start:.2f}, {self.end:.2f}))"
