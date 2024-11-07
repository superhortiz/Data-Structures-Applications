import heapq
import numpy as np
from .board import Board
from typing import List


class Solver:
    """
    Solver class to find a solution to the initial board using the A* algorithm.

    This class provides methods to solve the 8-puzzle problem (or similar puzzles) by finding the 
    shortest path from the initial board configuration to the goal configuration. It uses the A* 
    search algorithm to solve this problem.

    Attributes:
        solution_path (List[Board]): The sequence of board configurations from the initial to the goal state.

    Methods:
        is_solvable(): Determines if the puzzle is solvable.
        moves(): Returns the number of moves to solve the puzzle.
        solution(): Returns the sequence of boards in the solution path.
    """

    class SearchNode:
        """
        Represents a node in the search tree for solving the board.

        Attributes:
            board (Board): The current state of the board.
            prev_node (SearchNode): The previous node in the search path.
            f (int): The f-score of the node, which is the sum of g and the Manhattan distance heuristic.
            g (int): The number of moves made to reach this node (real cost taken so far).
        """
        def __init__(self, board: Board, g: int, prev_node: 'SearchNode') -> None:
            """
            Initializes a search node with the given board, move count, and previous node.

            Args:
                board (Board): The current state of the board.
                g (int): The number of moves made to reach this node.
                prev_node (SearchNode): The previous node in the search path.
            """
            self.board = board
            self.g = g
            self.prev_node = prev_node

            # f-score = g (number of moves made) + h (heuristic)
            self.f = g + board.manhattan()

        def __lt__(self, other: 'SearchNode') -> bool:
            """
            Less-than comparison based on the f-score for priority queue ordering.

            Args:
                other (SearchNode): The other search node to compare against.

            Returns:
                bool: True if this node's f-score is less than the other node's f-score, False otherwise.
            """
            return self.f < other.f

        def __eq__(self, other: 'SearchNode') -> bool:
            """
            Equality comparison based on the f-score.

            Args:
                other (SearchNode): The other search node to compare against.

            Returns:
                bool: True if this node's f-score is equal to the other node's f-score, False otherwise.
            """
            # Case 1: Other is the same object
            if self is other:
                return True

            # Case 2: Other is not instance of SearchNode
            if other is None or not isinstance(other, Solver.SearchNode):
                return False

            # Case 3: Evaluate equality based on f-score
            return self.f == other.f

    def __init__(self, initial: Board) -> None:
        """
        Initializes the Solver with the initial board configuration.

        Args:
            initial (Board): The initial board configuration.

        Raises:
            ValueError: If the initial board is None.
        """
        if initial is None:
            raise ValueError("Invalid argument.")

        self.solution_path = []
        pq, pq_twin = [], []

        # Create initial search nodes for the board and its twin
        first_node = self.SearchNode(initial, g = 0, prev_node = None)
        first_twin_node = self.SearchNode(initial.twin(), g = 0, prev_node = None)

        # Push the initial nodes onto their respective priority queues
        heapq.heappush(pq, (first_node.f, first_node))
        heapq.heappush(pq_twin, (first_twin_node.f, first_twin_node))

        # Process the priority queues until a solution is found or both are empty
        while pq and pq_twin:
            current_node = heapq.heappop(pq)[1]
            current_twin_node = heapq.heappop(pq_twin)[1]

            # Check if the current node or its twin is the goal
            if current_node.board.is_goal():
                self._build_path(current_node)
                return

            if current_twin_node.board.is_goal():
                self.solution_path = None
                return

            # Add neighbors of the current node to the priority queue
            for neighbor in current_node.board.neighbors():
                if current_node.prev_node is None or current_node.prev_node.board != neighbor:
                    node = self.SearchNode(neighbor, current_node.g + 1, current_node)
                    heapq.heappush(pq, (node.f, node))

            # Add neighbors of the current twin node to the twin priority queue
            for neighbor in current_twin_node.board.neighbors():
                if current_twin_node.prev_node is None or current_twin_node.prev_node.board != neighbor:
                    node = self.SearchNode(neighbor, current_twin_node.g + 1, current_twin_node)
                    heapq.heappush(pq_twin, (node.f, node))

    def is_solvable(self) -> bool:
        """
        Determines if the puzzle is solvable.

        Returns:
            bool: True if the puzzle is solvable, False otherwise.
        """
        return self.solution_path is not None

    def moves(self) -> int:
        """
        Returns the number of moves to solve the puzzle.

        Returns:
            int: The number of moves to solve the puzzle, or -1 if the puzzle is unsolvable.
        """
        if not self.is_solvable():
            return -1

        return len(self.solution_path) - 1

    def solution(self) -> List['Board']:
        """
        Returns the sequence of boards in the solution path.

        Returns:
            List[Board]: The sequence of board configurations from the initial to the goal state, or None if the puzzle is unsolvable.
        """
        return self.solution_path

    def _build_path(self, node: 'Solver.SearchNode') -> None:
        """
        Builds the solution path from the goal node to the initial node.

        Args:
            node (SearchNode): The goal node from which to build the path.
        """
        while node:
            self.solution_path.append(node.board)
            node = node.prev_node

        self.solution_path.reverse()
