from collections import defaultdict
from typing import Iterator, List, Set, Union


class UnionFind:
    """
    A weighted quick union data structure with path compression.
    Provides methods for checking connectivity and merging components.

    Methods:
        connected(p, q): Checks if sites p and q are in the same component.
        union(p, q): Merges the components containing sites p and q.

    Special Methods:
        __getitem__(index): Allows indexing, supports both integer indices and slice objects.
        __iter__(): Returns an iterator over the connected components.
        __len__(): Returns the number of connected components.
        __repr__(): Returns a string representation of connected components in the Union Find structure.
    """

    def __init__(self: 'UnionFind', n: int) -> None:
        """
        Initializes a Weighted Quick Union data structure.

        Args:
            n (int): The number of sites in the system.

        Raises:
            ValueError: If the argument is not an integer.
        """

        if not isinstance(n, int):
            raise ValueError("ValueError: Argument must be an integer.")

        # Initialize the id array: Each site is initially its own root.
        self._id = list(range(n))
        self._size = [1] * (n) # Initialize component sizes

    def _components(self: 'UnionFind') -> list:
        """
        Returns the connected components in the Union Find structure.

        Returns:
            components (list): A dictionary where keys are roots and values are sets of connected sites.
        """
        components = defaultdict(set)

        for i, index in enumerate(self._id):
            root = self._root(i)
            components[root].add(i)

        return list(components.values())

    def _root(self: 'UnionFind', i: int) -> int:
        """
        Finds the root (representative) of the component containing site i.

        Args:
            i (int): Site index.

        Returns:
            i (int): Root of the component.
        """

        # Chase parent pointers until reach root (path compression)
        while self._id[i] != i:

            # Path compression: Flatten the tree by updating parent pointers
            self._id[i] = self._id[self._id[i]]
            i = self._id[i]

        return i

    def connected(self: 'UnionFind', p: int, q: int) -> bool:
        """
        Checks if sites p and q are in the same component.

        Args:
            p (int): Site index.
            q (int): Site index.

        Returns:
            bool: True if p and q are connected, False otherwise.

        Raises:
            ValueError: If the value of p or q is not an integer.
            IndexError: If the value of p or q is out of the range.
        """
        if not isinstance(p, int) or not isinstance(q, int):
            raise ValueError

        if not 0 <= p <= len(self._size) or not 0 <= q <= len(self._size):
            raise IndexError

        return self._root(p) == self._root(q)

    def union(self: 'UnionFind', p: int, q: int) -> None:
        """
        Merges the components containing sites p and q.

        Args:
            p (int): Site index.
            q (int): Site index.

        Raises:
            ValueError: If the value of p or q is not an integer.
            IndexError: If the value of p or q is out of the range.
        """
        if not isinstance(p, int) or not isinstance(q, int):
            raise ValueError

        if not 0 <= p <= len(self._size) or not 0 <= q <= len(self._size):
            raise IndexError

        # Change root of p to point to root of q (weighted union)
        i = self._root(p)
        j = self._root(q)

        if i == j:
            return

        if self._size[i] < self._size[j]:
            self._id[i] = j
            self._size[j] += self._size[i]

        else:
            self._id[j] = i
            self._size[i] += self._size[j]

    def __getitem__(self: 'UnionFind', index: Union[int, slice]) -> Union[Set[int], List[Set[int]]]:
        """
        Allows indexing, supports both integer indices and slice objects.

        Args:
            index (Union[int, slice]): The index or slice to retrieve components.

        Returns:
            Union[Set[int], List[Set[int]]]: The component at the specified index or a list of components for the specified slice.
        """
        return self._components()[index]

    def __iter__(self: 'UnionFind') -> Iterator[List[Set[int]]]:
        """
        Returns an iterator over the connected components.

        Returns:
            Iterator[List[Set[int]]]: An iterator over the list of sets,
            where each set contains a connected component.
        """
        return iter(self._components())

    def __len__(self: 'UnionFind') -> int:
        """
        Returns the number of connected components.

        Returns:
            int: The number of connected components.
        """
        return len(self._components())

    def __repr__(self: 'UnionFind') -> str:
        """
        Returns a string representation of connected components in the
        Union Find structure.

        Returns:
            str: A string showing the connected components.
        """
        return f"{self._components()}"