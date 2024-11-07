from utils import UnionFind


class Percolation:
    """
    Models a percolation system using an n-by-n grid.

    Attributes:
        n (int): Grid size.

    Methods:
        get_grid(): Returns the current state of the percolation grid.
        get_full(): Returns the current state of the full sites grid.
        is_full(row, col): Determines whether a site at (row, col) is full (connected to the top row).
        is_open(row, col): Checks whether a site at (row, col) is open (unblocked).
        number_open_sites(): Returns the total number of open sites.
        open(row, col): Opens the site at (row, col) if it is not already open.
        percolates(): Checks if the system percolates.
    """
    def __init__(self, n: int) -> None:
        """
        Initializes a Percolation system with an n-by-n grid.

        Args:
            n (int): Grid size.
        """

        # Create an n-by-n grid with all sites initially blocked (0 represents blocked sites)
        self.n = n
        self._grid = [False] * n ** 2

        # Define virtual top and bottom sites for percolation
        # Virtual top site
        self._top = n ** 2
        # Virtual bottom site
        self._bottom = n ** 2 + 1

        # Initialize union-find data structures
        # 2 extra spaces for virtual nodes
        self._uf = UnionFind(n ** 2 + 2)
        # To track full sites and avoid backwash
        self._full = UnionFind(n ** 2 + 2)
        # Counter for open sites
        self._open_sites = 0


    def open(self, row: int, col: int) -> None:
        """
        Opens the site at (row, col) if it is not already open.

        Args:
            row (int): Row index.
            col (int): Column index.
        """

        if not self.is_open(row, col):
            position = self._get_index(row, col)
            self._grid[position] = True  # Mark the site as open
            self._open_sites += 1  # Update the count of open sites

            if row == 1:
                # Connect the top row to the second-to-last element (virtual top site)
                self._uf.union(self._top, self._get_index(row, col))
                self._full.union(self._top, self._get_index(row, col))

            if row == self.n:
                # Connect the lower row to the last element (virtual bottom site)
                self._uf.union(self._bottom, self._get_index(row, col))

            # Check neighboring sites and connect if they are also open
            neighbours = [[row - 1, col], [row + 1, col], [row, col - 1], [row, col + 1]]
            for neighbour_row, neighbour_col in neighbours:
                if 1 <= neighbour_row <= self.n and 1 <= neighbour_col <= self.n:
                    position_j = self._get_index(neighbour_row, neighbour_col)
                    if self.is_open(neighbour_row, neighbour_col):
                        self._uf.union(position, position_j)  # Connect neighboring open sites
                        self._full.union(position, position_j)


    def is_open(self, row: int, col: int) -> bool:
        """
        Checks whether a site at (row, col) is open (unblocked).

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: True if the site is open, False otherwise.
        """

        position = self._get_index(row, col)
        return self._grid[position] == 1

    def is_full(self, row: int, col: int) -> bool:
        """
        Determines whether a site at (row, col) is full (connected to the top row).

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: True if the site is full, False otherwise.
        """

        position = self._get_index(row, col)
        return self._full._root(position) == self._full._root(self._top) and self.is_open(row, col)

    def number_open_sites(self) -> int:
        """
        Returns the total number of open sites.

        Returns:
            int: Number of open sites.
        """

        return self._open_sites

    def percolates(self) -> bool:
        """
        Checks if the system percolates.

        Returns:
            bool: True if the system percolates, False otherwise.
        """

        # Check if virtual top and bottom are connected
        return self._uf._root(self._top) == self._uf._root(self._bottom)

    def _get_index(self, row: int, col: int) -> int:
        """
        Calculates the index corresponding to a given row and column in a flattened grid.

        Args:
            row (int): Row number (1-based index).
            col (int): Column number (1-based index).

        Returns:
            int: The flattened index corresponding to the specified row and column.
        """

        return (row - 1) * self.n + col - 1

    def get_grid(self) -> list:
        """
        Returns the current state of the percolation grid.

        Returns:
            list: A list representing the grid, where each element indicates whether a site is open (True) or blocked (False).
        """
        return self._grid