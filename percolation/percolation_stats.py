import sys
import random
import statistics
from .percolation_solver import Percolation


class PercolationStats:
    """
    Performs a series of computational experiments to estimate the percolation threshold.

    Attributes:
        n (int): The grid size for percolation experiments.
        trials (int): The number of independent trials to compute the statictics.

    Methods:
        confidence_lo(): Returns the lower bound of the 95% confidence interval.
        confidence_hi(): Returns the upper bound of the 95% confidence interval.
        mean(): Returns the mean percolation threshold.
        stddev(): Returns the standard deviation of percolation thresholds.
    """
    CONFIDENCE_95 = 1.96

    def __init__(self, n: int, trials: int) -> None:
        """
        Initializes a PercolationStats object.

        Args:
            n (int): The grid size for percolation experiments.
            trials (int): The number of independent trials to compute the statictics.
        """

        self.n = n
        self.trials = trials
        results = []

        # Perform independent trials
        for i in range(trials):
            self.percolation = Percolation(n)


            while not self.percolation.percolates():
                # Get random positions to open
                row, col = random.randint(1, n), random.randint(1, n)
                self.percolation.open(row, col)

            results.append(self.percolation.number_open_sites() / (n ** 2))

        # Compute statistics
        self._mean_value = statistics.mean(results)
        self._stddev_value = statistics.stdev(results)
        self._confidence_lo_value = self._mean_value - PercolationStats.CONFIDENCE_95 * self._stddev_value / (trials ** (1 / 2))
        self._confidence_hi_value = self._mean_value + PercolationStats.CONFIDENCE_95 * self._stddev_value / (trials ** (1 / 2))

    def mean(self) -> float:
        """
        Returns the mean percolation threshold.
        """

        return self._mean_value

    def stddev(self) -> float:
        """
        Returns the standard deviation of percolation thresholds.
        """

        return self._stddev_value

    def confidence_lo(self) -> float:
        """
        Returns the lower bound of the 95% confidence interval.
        """

        return self._confidence_lo_value

    def confidence_hi(self) -> float:
        """
        Returns the upper bound of the 95% confidence interval.
        """

        return self._confidence_hi_value


def main() -> None:
    """
    Entry point for the PercolationStats script.

    Reads command-line arguments for grid size (n) and number of trials (trials).
    Computes percolation statistics and prints the results.

    Usage:
        python percolation_stats.py n trials

    Args:
        None (reads from sys.argv)

    Returns:
        None
    """

    # args is a list of the command-line args
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: python percolation_stats.py n trials')
        return

    n, trials = map(int, args)
    if n < 0 or trials < 2:
        raise ValueError("'n' must be a positive integer, 'trials' must be equal or bigger than 2.")

    percolation = PercolationStats(n, trials)
    print(f"Received n = {n}, trials = {trials}")
    print("mean                    =", percolation.mean())
    print("stddev                  =", percolation.stddev())
    print("95% confidence interval =", [percolation.confidence_lo(), percolation.confidence_hi()])


if __name__ == "__main__":
    main()