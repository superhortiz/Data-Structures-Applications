from typing import Any, Iterator, List, Optional, Union
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)


class RedBlackBST:
    """
    A class representing a Red-Black Binary Search Tree (RedBlackBST) for efficient searching and insertion.
    This implementation is based on the algorithms and data structures described in the book
    "Algorithms, Part I, Fourth Edition" by Robert Sedgewick and Kevin Wayne, Princeton University.

    Worst Case Performance:
        - Search: O(log N)
        - Insert: O(log N)
        - Delete: O(log N)

    Methods:
        add(value): Adds a new node with the given value, using the value as the key.
        ceiling(key): Finds the smallest key in the RedBlackBST that is greater than or equal to the given key.
        delete_max(): Deletes the maximum node in the Red-Black BST.
        delete_min(): Deletes the minimum node in the Red-Black BST.
        floor(key): Finds the largest key in the RedBlackBST that is less than or equal to the given key.
        max(): Finds the maximum key in the RedBlackBST.
        min(): Finds the minimum key in the RedBlackBST.
        print_tree(): Prints the RedBlackBST in a structured format.
        print_tree_balanced(): Prints the RedBlackBST as a 2-3 Tree in a structured format.
        rank(key): Returns the number of keys less than the given key in the RedBlackBST.
        range(key_lo, key_hi): Finds and returns all keys within the specified range [key_lo, key_hi].

    Special Methods:
        __bool__(): Checks if the RedBlackBST is not empty.
        __contains__(key): Checks if a key is in the RedBlackBST.
        __delitem__(key): Deletes the node with the given key from the RedBlackBST.
        __getitem__(key): Gets the value associated with the given key or a range of keys.
        __iter__(): Returns an iterator for in-order traversal of the RedBlackBST.
        __len__(): Gets the number of nodes in the RedBlackBST.
        __setitem__(key, value): Sets the value for the given key in the RedBlackBST.
        __repr__(): Returns a string representation of the RedBlackBST.
        __reversed__(): Returns an iterator for reverse in-order traversal of the RedBlackBST.

    Notes:
        Insertion Methods:
            - add(value): Inserts elements using the value as the key. This method can accept
            any comparable data type.

            - __setitem__(key, value): Inserts elements using an integer key. This allows the use
            of `__getitem__(key)`, where the key can be an integer or a slice.

        Range Queries:
            - range(key_lo, key_hi): Returns all values within the specified range [key_lo, key_hi].
    """

    RED = True
    BLACK = False

    class TreeNode:
        """
        A class representing a node in the Binary Search Tree.

        Attributes:
            color (bool): Color of the link to the node's parent.
            count (int): The size of the subtree rooted at this node.
            key (int): The key of the node.
            left (TreeNode): The left child of this node.
            right (TreeNode): The right child of this node.
            value (Any): The value associated with the key.
        """
        def __init__(self: 'TreeNode', key: int, value: Any, color: bool, count: int) -> None:
            """
            Initializes a TreeNode.

            Args:
                color (bool): Color of the link to the node's parent.
                count (int): The size of the subtree rooted at this node.
                key (int): The key of the node.
                value (Any): The value associated with the key.
            """
            self.key = key
            self.value = value
            self.color = color
            self.count = count
            self.left = None
            self.right = None

    def __init__(self: 'RedBlackBST') -> None:
        """
        Initializes an empty RedBlackBST.
        """
        self._root = None

    def _is_red(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> bool:
        """
        Checks if a given node is red.

        Args:
            node (RedBlackBST.TreeNode): The node to check.

        Returns:
            bool: True if the node is red, False if the node is black or None.
        """
        # None links are considered black
        if node is None:
            return False

        # Return True if the node's color is RED, otherwise False
        return node.color == RedBlackBST.RED

    def _rotate_left(self: 'RedBlackBST', current_node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Performs a left rotation on the given node.

        This method is used to maintain the balance of the Red-Black tree by rotating
        the right child of the current node to the left. It assumes that the right child
        of the current node is red.

        Args:
            current_node (RedBlackBST.TreeNode): The node on which to perform the left rotation.

        Returns:
            RedBlackBST.TreeNode: The new root of the subtree after rotation.
        """
        assert self._is_red(current_node.right), "Rotate left was called, but there is no red links leaning in the wrong direction."

        # Finds the node to exchange
        new_root = current_node.right

        # Completes the new connections for current_node
        current_node.right = new_root.left

        # Completes the new connections for new_root
        new_root.left = current_node

        # Assigns black for new_root
        new_root.color = current_node.color

        # Assigns red for current_node
        current_node.color = RedBlackBST.RED

        # Update node counts
        new_root.count = current_node.count
        current_node.count = 1 + self._size(current_node.left) + self._size(current_node.right)

        # Returns new_root instead of current_node
        return new_root

    def _rotate_right(self: 'RedBlackBST', current_node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Performs a right rotation on the given node.

        This method is used to maintain the balance of the Red-Black tree by rotating
        the left child of the current node to the right. It assumes that the left child
        of the current node is red.

        Args:
            current_node (RedBlackBST.TreeNode): The node on which to perform the right rotation.

        Returns:
            RedBlackBST.TreeNode: The new root of the subtree after rotation.
        """
        assert self._is_red(current_node.left), "Rotate right was called, but there is no red links leaning in the wrong direction."

        # Finds the node to exchange
        new_root = current_node.left

        # Completes the new connections for current_node
        current_node.left = new_root.right

        # Completes the new connections for new_root
        new_root.right = current_node

        # Assigns black for new_root
        new_root.color = current_node.color

        # Assigns red for current_node
        current_node.color = RedBlackBST.RED

        # Update node counts
        new_root.count = current_node.count
        current_node.count = 1 + self._size(current_node.left) + self._size(current_node.right)

        # Returns new_root instead of current_node
        return new_root

    def _flip_colors(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> None:
        """
        Flips the colors of the given node and its children.

        Args:
            node (RedBlackBST.TreeNode): The node whose colors are to be flipped.
        """
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    def _move_red_left(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Ensures the left-leaning property of the Red-Black tree during deletion operations.

        Args:
            node (RedBlackBST.TreeNode): The current node being processed.

        Returns:
            RedBlackBST.TreeNode: The modified node after color flips and rotations.
        """
        # Flip the colors of node and its children
        self._flip_colors(node)

        # Check if the left child of node.right is red
        if self._is_red(node.right.left):
            # Perform a right rotation on node.right
            node.right = self._rotate_right(node.right)
            # Perform a left rotation on node
            node = self._rotate_left(node)

        # Return the modified node
        return node

    def _move_red_right(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Ensures the left-leaning property of the Red-Black tree during deletion operations.

        Args:
            node (RedBlackBST.TreeNode): The current node being processed.

        Returns:
            RedBlackBST.TreeNode: The modified node after color flips and rotations.
        """
        # Flip the colors of node and its children
        self._flip_colors(node)

        # Check if the left child of node.left is red
        if self._is_red(node.left.left):
            # Perform a left rotation on node
            node = self._rotate_right(node)

        # Return the modified node
        return node

    def _balance(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Balances the Red-Black tree by performing rotations and color flips.

        This method ensures that the Red-Black tree maintains its balanced properties
        by performing necessary rotations and color flips. It also updates the count
        of nodes in the subtree rooted at the given node.

        Args:
            node (RedBlackBST.TreeNode): The node to balance.

        Returns:
            RedBlackBST.TreeNode: The balanced node.
        """
        # Perform a left rotation if the right child is red
        if self._is_red(node.right):
            node = self._rotate_left(node)  
          
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

        # Return the corresponding link to the node
        return node

    def __setitem__(self: 'RedBlackBST', key: int, value: Any) -> None:
        """
        Sets the value for the given key in the RedBlackBST.

        Args:
            key (int): The key of the node.
            value (Any): The value to be set for the key.

        Raises:
            ValueError: If 'key' is not an int type.
            ValueError: If 'value' is None.
        """
        if not isinstance(key, int):
            raise ValueError("The key must be a integer type.")

        if value is None:
            raise ValueError("ValueError: Invalid value.")

        # This handles the case when the client sets the key.
        self._root = self._add(self._root, key, value)

        # Set the root Black
        self._root.color = RedBlackBST.BLACK

    def add(self: 'RedBlackBST', value: int) -> None:
        """
        Adds a new node with the given value, using the value as the key.

        Args:
            value (int): The value to be added as both key and value.

        """

        # This handles the case when the client does not provide a key.
        # Then we use key = value.
        self._root = self._add(self._root, value, value)

        # Set the root Black
        self._root.color = RedBlackBST.BLACK

    def _add(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode', key: int, value: Any) -> 'RedBlackBST.TreeNode':
        """
        Helper method to add a new node to the RedBlackBST.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.
            key (int): The key of the new node.
            value (Any): The value associated with the key.

        Returns:
            RedBlackBST.TreeNode: The root of the subtree after insertion.
        """

        # End of the tree reached, return a new TreeNode and color it RED
        if node is None:
            return self.TreeNode(key, value, RedBlackBST.RED, 1)

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

        # Return the corresponding link to the node
        return node

    def delete_min(self: 'RedBlackBST') -> None:
        """
        Deletes the minimum node in the Red-Black BST.
        It calls the helper method _delete_min(node) to perform the actual deletion.
        """
        if self._root is None:
            return

        # Simplify the operations by setting RED the color of the root
        if not self._is_red(self._root.left) and not self._is_red(self._root.right):
            self._root.color = RedBlackBST.RED
        
        # Call private method
        self._root = self._delete_min(self._root)

        # Ensure that the root is BLACK again
        if self._root is not None:
            self._root.color = RedBlackBST.BLACK

    def _delete_min(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Helper method to delete the minimum node in the subtree.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.

        Returns:
            RedBlackBST.TreeNode: The root of the subtree after deletion.
        """
        # We have reached the minimum, delete it returning None
        if node.left is None:
            return None

        # If both the left child and its left child are black, move red to the left
        if not self._is_red(node.left) and not self._is_red(node.left.left):
            node = self._move_red_left(node)

        # Recursively delete the minimum node in the left subtree
        node.left = self._delete_min(node.left)

        # Balance the tree and return the modified node
        return self._balance(node)

    def delete_max(self: 'RedBlackBST') -> None:
        """
        Deletes the maximum node in the Red-Black BST.
        It calls the helper method _delete_max(node) to perform the actual deletion.
        """
        if self._root is None:
            return

        # Simplify the operations by setting RED the color of the root
        if not self._is_red(self._root.left) and not self._is_red(self._root.right):
            self._root.color = RedBlackBST.RED
        
        # Call private method
        self._root = self._delete_max(self._root)

        # Ensure that the root is BLACK again
        if self._root is not None:
            self._root.color = RedBlackBST.BLACK

    def _delete_max(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Helper method to delete the maximum node in the subtree.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.

        Returns:
            RedBlackBST.TreeNode: The root of the subtree after deletion.
        """
        # If the left child is red, perform a right rotation to maintain balance
        if self._is_red(node.left):
            node = self._rotate_right(node)

        # We have reached the maximum, delete it returning None
        if node.right is None:
            return None

        # If both the right child and its left child are black, move red to the right
        if not self._is_red(node.right) and not self._is_red(node.right.left):
            node = self._move_red_left(node)

        # Recursively delete the maximum node in the right subtree
        node.right = self._delete_max(node.right)

        # Balance the tree and return the modified node
        return self._balance(node)

    def __delitem__(self: 'RedBlackBST', key: int) -> None:
        """
        Deletes the node with the given key from the RedBlackBST.

        Args:
            key (int): The key of the node to delete.

        Raises:
            IndexError: If the key is not found in the RedBlackBST.
        """
        if not self.__contains__(key):
            raise IndexError("The tree does not contain the specified key")

        # Simplify the operations by setting RED the color of the root
        if not self._is_red(self._root.left) and not self._is_red(self._root.right):
            self._root.color = RedBlackBST.RED

        # Call private method
        self._root = self._delete(self._root, key)

        # Ensure that the root is BLACK again
        if self._root is not None:
            self._root.color = RedBlackBST.BLACK

    def _delete(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode', key: int) -> 'RedBlackBST.TreeNode':
        """
        Helper method to delete a node with the given key from the RedBlackBST.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.
            key (int): The key of the node to delete.

        Returns:
            RedBlackBST.TreeNode: The root of the subtree after deletion.
        """

        # Search for the key in the left subtree
        if key < node.key:
            # Move red to the left if necessary
            if not self._is_red(node.left) and not self._is_red(node.left.left):
                node = self._move_red_left(node)

            # Recursively call _delete method in the left subtree
            node.left = self._delete(node.left, key)

        # Search for the key in the right subtree
        else:
            # Rotate right if the left child is red
            if self._is_red(node.left):
                node = self._rotate_right(node)

            # If the key is found and there is no right child, delete the node
            if key == node.key and node.right is None:
                return None

            # Move red to the right if necessary
            if not self._is_red(node.right) and not self._is_red(node.right.left):
                node = self._move_red_right(node)

            # If the key is found, replace it with the minimum node in the right subtree
            if key == node.key:
                min_node = self._min(node.right)
                node.key = min_node.key
                node.value = min_node.value
                node.right = self._delete_min(node.right)
            else:
                # Recursively call _delete method in the right subtree
                node.right = self._delete(node.right, key)

        # Balance the tree and return the modified node
        return self._balance(node)

    # The following methods are the same as those in the BST implementation
    def __bool__(self: 'RedBlackBST') -> bool:
        """
        Checks if the RedBlackBST is not empty.

        Returns:
            bool: True if the tree is not empty, False otherwise.
        """
        return self._root is not None

    def __len__(self: 'RedBlackBST') -> int:
        """
        Gets the number of nodes in the RedBlackBST.

        Returns:
            int: The total number of nodes in the tree.
        """
        return self._size(self._root)

    def _size(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> int:
        """
        Returns the size of the subtree rooted at the given node.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.

        Returns:
            int: The total number of nodes in the subtree.
        """
        if node is None:
            return 0
        return node.count

    def __getitem__(self: 'RedBlackBST', key: Union[int, slice]) -> Union[Any, List[Any]]:
        """
        Gets the value associated with the given key or a range of keys.

        Args:
            key (Union[int, slice]): The key or slice of keys to retrieve.

        Returns:
            Union[Any, List[Any]]: The value associated with the key, or a list of values for the range of keys.

        Raises:
            KeyError: If the key is not found in the tree.
            TypeError: If the argument is not an int or slice.
        """
        # Case 1: Requesting a specific index
        if isinstance(key, int):
            node = self._root

            # Iterate through the tree until the key is found
            while node:
                if key < node.key:
                    node = node.left
                elif key > node.key:
                    node = node.right
                elif key == node.key:
                    return node.value
            raise KeyError(f"Key {key} not found in the tree.")

        # Case 2: Requesting a slice
        elif isinstance(key, slice):

            # Adapt the slices to the size of the tree
            start, stop, step = key.indices(self.__len__())

            def range(node: 'RedBlackBST.TreeNode', key_lo: int, key_hi: int, step: int) -> List[int]:
                """
                Helper generator to yield keys within the specified range.

                Args:
                    node (RedBlackBST.TreeNode): The root of the subtree.
                    key_lo (int): The lower bound of the range.
                    key_hi (int): The upper bound of the range.
                    step (int): The step value for the range.

                Yields:
                    int: The keys within the specified range.
                """
                # End of the tree reached, return
                if node is None:
                    return

                # Explore recursively the left child
                if key_lo < node.key:
                    yield from range(node.left, key_lo, key_hi, step)

                # The key of the current node falls within the specified range
                if key_lo <= node.key and key_hi > node.key:

                    # Filter out the keys that do not match the specified step value
                    if (node.key - key_lo) % step == 0:
                        yield node.key

                # Explore recursively the right child
                if key_hi > node.key:
                    yield from range(node.right, key_lo, key_hi, step)

            return range(self._root, start, stop, step)

        # Case 3: Invalid argument
        else:
            raise TypeError("Invalid argument.")

    def __contains__(self: 'RedBlackBST', key: int) -> bool:
        """
        Checks if a key is in the RedBlackBST.

        Args:
            key (int): The key to check for.

        Returns:
            bool: True if the key is in the RedBlackBST, False otherwise.
        """

        node = self._root

        # Go through all the tree looking for the key
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            elif key == node.key:
                return True
        return False

    def __iter__(self: 'RedBlackBST') -> Iterator[Any]:
        """
        Returns an iterator for in-order traversal of the RedBlackBST.

        Yields:
            Any: The values of the nodes ordered by their key.
        """
        def in_order(node: 'RedBlackBST.TreeNode')-> Iterator[Any]:
            """
            Helper generator for in-order traversal.

            Args:
                node (RedBlackBST.TreeNode): The root of the subtree.

            Yields:
                Any: The values of the nodes in in-order.
            """
            # We have reached the leaf node
            if node is None:
                return

            # Recursively go to the left
            yield from in_order(node.left)

            # Return the current node
            yield node.value

            # Recursively go to the right
            yield from in_order(node.right)

        # Call the nested function
        return in_order(self._root)

    def __reversed__(self: 'RedBlackBST') -> Iterator[Any]:
        """
        Returns an iterator for reverse in-order traversal of the RedBlackBST.

        Yields:
            Any: The values of the nodes in reverse in-order.
        """
        def reversed_order(node: 'RedBlackBST.TreeNode')-> Iterator[Any]:
            """
            Helper generator for reverse in-order traversal.

            Args:
                node (RedBlackBST.TreeNode): The root of the subtree.

            Yields:
                Any: The values of the nodes in reverse in-order.
            """
            # We have reached the leaf node
            if node is None:
                return

            # Recursively go to the right
            yield from reversed_order(node.right)

            # Return the current node
            yield node.value

            # Recursively go to the left
            yield from reversed_order(node.left)

        # Call the nested function
        return reversed_order(self._root)

    def __repr__(self: 'RedBlackBST') -> str:
        """
        Returns a string representation of the RedBlackBST.

        Returns:
            str: A string representation of the RedBlackBST.
        """
        return f"RedBlackBST({list(self.__iter__())})"

    def ceiling(self: 'RedBlackBST', key: int) -> int:
        """
        Finds the smallest key in the RedBlackBST that is greater than or equal to the given key.

        Args:
            key (int): The key to find the ceiling for.

        Returns:
            int: The ceiling key, or None if no ceiling exists.
        """
        # Calls the private method
        node = self._ceiling(self._root, key)

        # It means that there is no ceiling for the given key
        if node is None:
            return None

        # The ceiling is found, return the key
        return node.key

    def _ceiling(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode', key: int) -> 'RedBlackBST.TreeNode':
        """
        Helper method to find the ceiling node in the RedBlackBST.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.
            key (int): The key to find the ceiling for.

        Returns:
            RedBlackBST.TreeNode: The ceiling node, or None if no ceiling exists.
        """
        # We have reached the end of the path without finding the ceiling
        if node is None:
            return None

        # Case 1: The ceiling of key is key
        if key == node.key:
            return node

        # Case 2: The ceiling of key is in the right subtree
        if key > node.key:
            return self._ceiling(node.right, key)

        # Case 3: The ceiling of key is in the left subtree if there is any k >= key in left subtree;
        # otherwise it is the key in the root.
        left_subtree_floor = self._ceiling(node.left, key)

        if left_subtree_floor is not None:
            return left_subtree_floor
        else:
            return node

    def floor(self: 'RedBlackBST', key: int) -> int:
        """
        Finds the largest key in the RedBlackBST that is less than or equal to the given key.

        Args:
            key (int): The key to find the floor for.

        Returns:
            int: The floor key, or None if no floor exists.
        """
        # Calls the private method
        node = self._floor(self._root, key)

        # It means that there is no floor for the given key
        if node is None:
            return None

        # The floor is found, return the key
        return node.key

    def _floor(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode', key: int)-> 'RedBlackBST.TreeNode':
        """
        Helper method to find the floor node in the RedBlackBST.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.
            key (int): The key to find the floor for.

        Returns:
            RedBlackBST.TreeNode: The floor node, or None if no floor exists.
        """
        # We have reached the end of the path without finding the floor
        if node is None:
            return None

        # Case 1: The floor of key is key
        if key == node.key:
            return node

        # Case 2: The floor of key is in the left subtree
        if key < node.key:
            return self._floor(node.left, key)

        # Case 3: The floor of key is in the right subtree if there is any k <= key in right subtree;
        # otherwise it is the key in the root.

        right_subtree_floor = self._floor(node.right, key)

        if right_subtree_floor is not None:
            return right_subtree_floor
        else:
            return node

    def max(self: 'RedBlackBST') -> int:
        """
        Finds the maximum key in the RedBlackBST.

        Returns:
            int: The maximum key in the RedBlackBST.
        """
        return self._max(self._root).key

    def _max(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Helper method to find the node with the maximum key in the RedBlackBST.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.

        Returns:
            RedBlackBST.TreeNode: The node with the maximum key.
        """
        # Recursively go to the right until the end
        if node.right is None:
            return node
        return self._max(node.right)

    def min(self: 'RedBlackBST') -> int:
        """
        Finds the minimum key in the RedBlackBST.

        Returns:
            int: The minimum key in the RedBlackBST.
        """
        return self._min(self._root).key

    def _min(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode') -> 'RedBlackBST.TreeNode':
        """
        Helper method to find the node with the minimum key in the RedBlackBST.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.

        Returns:
            RedBlackBST.TreeNode: The node with the minimum key.
        """
        # Recursively go to the left until the end
        if node.left is None:
            return node
        return self._min(node.left)

    def print_tree(self: 'RedBlackBST') -> None:
        """
        Prints the RedBlackBST in a structured format.
        """
        self._print_tree(self._root)

    def _print_tree(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode' = None, level: int = 0, prefix: str = "Root: ") -> None:
        """
        Helper method to print the RedBlackBST in a structured format.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.
            level (int): The current level in the tree (used for indentation).
            prefix (str): The prefix to print before the node value.
        """
        if node is not None:
            color = Fore.RED if self._is_red(node) else Fore.RESET
            print(f"{color}{' ' * (level * 4)}{prefix} {node.value}")
            if node.left:
                self._print_tree(node.left, level + 1, "L-->")
            if node.right:
                self._print_tree(node.right, level + 1, "R-->")

    def print_tree_balanced(self: 'RedBlackBST') -> None:
        """
        Prints the RedBlackBST as a 2-3 Tree in a structured format.
        """
        self._print_tree_balanced(self._root)

    def _print_tree_balanced(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode' = None, level: int = 0, prefix: str = "Root: ") -> None:
        """
        Helper method to print the RedBlackBST as a 2-3 Tree in a structured format.

        Args:
            node (RedBlackBST.TreeNode): The root of the subtree.
            level (int): The current level in the tree (used for indentation).
            prefix (str): The prefix to print before the node value.
        """
        if node is not None:
            color = Fore.RED if self._is_red(node) else Fore.RESET
            level -= 1 if self._is_red(node) else 0
            print(f"{color}{' ' * (level * 4)}{prefix} {node.value}")

            if node.left:
                self._print_tree_balanced(node.left, level + 1, "L-->")
            if node.right:
                if self._is_red(node):
                    self._print_tree_balanced(node.right, level + 1, "B-->")
                else:
                    self._print_tree_balanced(node.right, level + 1, "R-->")

    def rank(self: 'RedBlackBST', key: int) -> int:
        """
        Returns the number of keys less than the given key in the RedBlackBST.

        Args:
            key (int): The key to find the rank for.

        Returns:
            int: The number of keys less than the given key.
        """
        return self._rank(key, self._root)

    def _rank(self: 'RedBlackBST', key: int, node: 'RedBlackBST.TreeNode') -> int:
        """
        Helper method to return the number of keys less than the given key in the subtree rooted at the given node.

        Args:
            key (int): The key to find the rank for.
            node (RedBlackBST.TreeNode): The root of the subtree.

        Returns:
            int: The number of keys less than the given key in the subtree.
        """

        if node is None:
            # We have reached the leaf node, there are no more node to compare
            return 0

        if key < node.key:
            # Recursively go to the left subtree, because all the keys in the left
            # are less than the current node's key
            return self._rank(key, node.left)

        elif key > node.key:
            # We add 1 for the current node plus the size of the left subtree.
            # Recursively go to the right subtree.
            return 1 + self._size(node.left) + self._rank(key, node.right)

        elif key == node.key:
            # Returns the size of the left subtree, because all those keys are less
            # than the current node's key
            return self._size(node.left)

    def range(self, key_lo: Any, key_hi: Any) -> List[Any]:
        """
        Finds and returns all keys within the specified range [key_lo, key_hi].

        Args:
            key_lo (Any): The lower bound of the range.
            key_hi (Any): The upper bound of the range.

        Returns:
            List[Any]: A list of keys within the specified range.
        """
        return self._range(self._root, key_lo, key_hi)

    def _range(self: 'RedBlackBST', node: 'RedBlackBST.TreeNode', key_lo: Any, key_hi: Any) -> List[Any]:
        """
        Helper function to recursively find all keys within the specified range.

        Args:
            node (TreeNode): The current node being explored.
            key_lo (Any): The lower bound of the range.
            key_hi (Any): The upper bound of the range.

        Yields:
            Any: Keys within the specified range.
        """

        # End of the tree reached, return
        if node is None:
            return

        # Explore recursively the left child
        if key_lo < node.key:
            yield from self._range(node.left, key_lo, key_hi)

        # The key of the current node falls within the specified range
        if key_lo <= node.key <= key_hi:
            yield node.key

        # Explore recursively the right child
        if key_hi > node.key:
            yield from self._range(node.right, key_lo, key_hi)