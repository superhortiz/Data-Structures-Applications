from .percolation_solver import Percolation
from typing import Tuple
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import random
import numpy as np


class PercolationVisualize:
    """
    Simulates and visualizes the process of percolation on an n x n grid.
    It randomly open grid sites until the system percolates.

    Attributes:
        n (int): The grid size for percolation experiments.
        percolation (Percolation): The percolation model.

    Methods:
        animate_percolation(): Animates the percolation process on the grid.
    """

    def __init__(self, n: int) -> None:
        """
        Initializes a PercolationVisualize object.

        Args:
            n (int): The grid size for percolation experiments.
        """
        self.n = n
        self.percolation = Percolation(n)

        # This ensures that animate_percolation will be inside a loop
        while not self.percolation.percolates():
            self.animate_percolation()

    def animate_percolation(self) -> None:
        """
        Animates the percolation process on the grid.
        """
        # Create a figure and a set of subplots
        fig, ax = plt.subplots()

        # Obtain grid representation of the percolation system
        grid = self._get_representation()

        # Custom color map: black for blocked, white for open, cyan for full
        cmap = mcolors.ListedColormap(['black', '#D2D2CF', 'cyan'])

        # Bounds:
        # 0 to 1: Maps to black (blocked sites).
        # 1 to 2: Maps to white (open sites)
        # 2 to 3: Maps to cyan (full sites)
        bounds = [0, 1, 2, 3]

        # Creates a normalization object that maps data values to the intervals defined in bounds
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        # Display the image
        image = ax.imshow(grid, cmap = cmap, norm = norm, interpolation = 'nearest')

        # Remove the tick labels on both axes
        ax.set_xticks([])
        ax.set_yticks([])

        # Create custom legend handles
        legend_handles = [
            mpatches.Patch(color='cyan', label='Full'),
            mpatches.Patch(color='black', label='Blocked'),
            mpatches.Patch(color='#D2D2CF', label='Open'),
        ]

        # Add the legend to the plot, outside the axes
        ax.legend(handles = legend_handles, loc = 'center left', bbox_to_anchor = (1, 0.5))

        def update(frame: int) -> None:
            """
            This function will generate the next states for the system
            """
            # Iterative process
            if not self.percolation.percolates():
                row, col = self._get_random_position()
                self.percolation.open(row, col)

            # Obtain the updated grid representation of the percolation system
            grid = self._get_representation()

            # Update the data of the image
            image.set_array(grid)

            # Check if the system percolates
            if self.percolation.percolates():

                # Show texts when it percolates
                ax.annotate('The system percolates', xy=(0.5, 1.1), xycoords='axes fraction',
                        ha='center', va='bottom', color='red')

                open_sites = self.percolation.number_open_sites()

                ax.annotate(f"Number of open sites: {open_sites} ({open_sites / self.n ** 2 * 100:.1f}%)",
                        xy=(0.5, 1.05), xycoords='axes fraction', ha='center', va='bottom', color='black')

            # Return the updated image
            return image

        # Define interval
        interval = 1 / (self.n ** 4)

        # Update the animation
        ani = animation.FuncAnimation(fig, update, frames = self.n ** 2, interval = interval, repeat = False)
        plt.show()

    def _get_random_position(self) -> Tuple[int, int]:
        """
        Gets a random position on the grid that is not already open.

        Returns:
            Tuple[int, int]: A tuple containing the row and column of the random position.
        """
        row, col = random.randint(1, self.n), random.randint(1, self.n)

        while self.percolation.is_open(row, col):
            row, col = random.randint(1, self.n), random.randint(1, self.n)

        return row, col

    def _get_representation(self) -> np.ndarray:
        """
        Gets the grid representation of the percolation system.

        Returns:
            np.ndarray: A 2D numpy array representing the grid.
        """
        # Start with all sites blocked
        grid = np.zeros((self.n, self.n))

        # Iterate over all the positions
        for row in range(1, self.n + 1):
            for col in range(1, self.n + 1):
                # Gets full sites
                if self.percolation.is_full(row, col):
                    grid[row - 1, col - 1] = 2

                # Gets open sites
                elif self.percolation.is_open(row, col):
                    grid[row - 1, col - 1] = 1
        return grid


def main() -> None:
    """
    Runs an example usage of PercolationVisualize class.
    """
    n = 50
    percolation = PercolationVisualize(n)


if __name__ == "__main__":
    main()