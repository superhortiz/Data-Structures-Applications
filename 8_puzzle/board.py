import copy
from typing import List, Tuple
import numpy as np


class Board:
    """
    Represents an n x n board for the 8-puzzle problem (or similar puzzles).

    This class provides methods to calculate the Hamming and Manhattan distances,
    check if the board is in the goal state, generate neighboring boards, and create
    a twin board by swapping any pair of tiles.

    Attributes:
        n (int): The dimension of the board.
        board (List[List[int]]): The 2D list representing the board configuration.

    Methods:
        dimension(): Return the dimension of the board.
        find_indices_blank(): Find the indices of the blank tile (0) in the board.
        hamming(): Calculate the Hamming distance of the board.
        is_goal(): Check if the board is in the goal state.
        manhattan(): Calculate the Manhattan distance of the board.
        neighbors(): Generate all neighboring boards by sliding a tile into the blank space.
        twin(): Create a twin board by swapping any pair of tiles.

    Special Methods:
        __eq__(other): Check if two Board instances are equal.
        __str__(): Return a string representation of the board.
    """

    def __init__(self, tiles: np.ndarray) -> None:
        """
        Initialize the Board with a deep copy of the given tiles.

        Args:
            tiles (np.ndarray): The initial configuration of the board.
        """
        # Dimension of the board
        self.n = len(tiles)

        # 2D list to store the tiles
        self.board = copy.deepcopy(tiles)

    def __eq__(self, other: 'Board') -> bool:
        """
        Check if two Board instances are equal.

        Args:
            other (Board): The other Board instance to compare with.

        Returns:
            bool: True if both Board instances are equal, False otherwise.
        """
        if self is other:
            return True
        if other is None or not isinstance(other, Board):
            return False
        return self.n == other.n and np.array_equal(self.board, other.board)

    def __str__(self) -> str:
        """
        Return a string representation of the board.

        Returns:
            str: String representation of the board.
        """
        return f"{self.board}"

    def dimension(self) -> int:
        """
        Return the dimension of the board.

        Returns:
            int: The dimension of the board.
        """
        return self.n

    def hamming(self) -> int:
        """
        Calculate the Hamming distance of the board.

        The Hamming distance is the number of tiles out of place.

        Returns:
            int: The Hamming distance.
        """
        distance = 0;
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != self.n * i + j + 1 and self.board[i][j] != 0:
                    distance += 1
        return distance

    def manhattan(self) -> int:
        """
        Calculate the Manhattan distance of the board.

        The Manhattan distance is the sum of the distances of the tiles from their goal positions.

        Returns:
            int: The Manhattan distance.
        """
        distance = 0;
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    row = (value - 1) // self.n
                    col = (value - 1) % self.n
                    distance += abs(row - i) + abs(col - j)
        return distance

    def is_goal(self) -> bool:
        """
        Check if the board is in the goal state.

        The goal state is when all tiles are in order from 1 to n*n-1, with the blank tile (0) at the end.

        Returns:
            bool: True if the board is in the goal state, False otherwise.
        """
        for i in range(self.n):
            for j in range(self.n):
                if i == self.n - 1 and j == self.n - 1:
                    if self.board[i][j] != 0:
                        return False
                elif self.board[i][j] != self.n * i + j + 1:
                    return False
        return True

    def neighbors(self) -> List['Board']:
        """
        Generate all neighboring boards by sliding a tile into the blank space.

        Returns:
            List[Board]: A list of all neighboring board configurations.
        """
        neighbors = []
        i, j = self.find_indices_blank()
        candidates = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
        for candidate in candidates:
            x = candidate[0]
            y = candidate[1]
            if 0 <= x < self.n and 0 <= y < self.n:
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[x][y] = new_board[x][y], new_board[i][j]
                neighbors.append(Board(new_board))
        return neighbors

    def twin(self) -> 'Board':
        """
        Create a twin board by swapping any pair of tiles.

        Returns:
            Board: A new board instance with two tiles swapped.
        """
        x1, y1, x2, y2 = 0, 0, 0, 1
        new_board = copy.deepcopy(self.board)
        i, j = self.find_indices_blank()
        if (i == x1 and j == y1) or (i == x2 and j == y2):
            x1, x2, y1, y2 = self.n - 1, self.n - 1, self.n - 1, self.n - 2
        new_board[x1][y1], new_board[x2][y2] = new_board[x2][y2], new_board[x1][y1]
        return Board(new_board)

    def find_indices_blank(self) -> Tuple[int, int]:
        """
        Find the indices of the blank tile (0) in the board.

        Returns:
            Tuple[int, int]: The (row, column) indices of the blank tile.
        """
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    return (i, j)
        return (-1, -1)


# Example usage
if __name__ == "__main__":
    tiles = np.array([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
    board = Board(tiles)
    print(board)
    print("Hamming distance =", board.hamming())
    print("Manhattan distance =", board.manhattan())
    print("Is the goal?", board.is_goal())
    print("Neighbors:")
    for neighbor in board.neighbors():
        print(neighbor)

    print("Twin =\n", board.twin(), sep = '')