from .interval_st import *
import random


def main() -> None:
    """
    Main function to demonstrate the use of Interval Search Tree (IntervalST) with random intervals.
    It adds intervals to the tree, searches for intersections with a random interval, and plots the results.
    """

    # Define list of intervals
    intervals = [Interval((10.44, 12.82)),
                 Interval((20.45, 23.70)),
                 Interval((2.18, 4.03)), 
                 Interval((9.20, 16.57)), 
                 Interval((5.96, 14.62)), 
                 Interval((8.31, 11.70)), 
                 Interval((5.19, 8.92)), 
                 Interval((1.23, 4.45)), 
                 Interval((3.67, 4.44)), 
                 Interval((4.72, 12.72)), 
                 Interval((2.61, 8.78)), 
                 Interval((20.95, 24.04)), 
                 Interval((1.51, 5.97)), 
                 Interval((7.66, 12.85)), 
                 Interval((13.57, 15.98)), 
                 Interval((9.36, 12.25)), 
                 Interval((8.03, 14.32)), 
                 Interval((12.85, 16.59)), 
                 Interval((3.05, 7.29)), 
                 Interval((15.60, 18.04)), 
                 Interval((17.15, 22.60)), 
                 Interval((12.68, 18.35)), 
                 Interval((15.97, 21.28)), 
                 Interval((0.75, 3.07)), 
                 Interval((7.76, 13.64)), 
                 Interval((17.97, 20.93)), 
                 Interval((0.39, 1.53)), 
                 Interval((5.91, 10.55)), 
                 Interval((0.63, 3.31)), 
                 Interval((2.83, 3.16)),
                 ]

    # Define variables
    X_MIN = 0
    X_MAX = 25
    Y_MIN = -2
    Y_MAX = len(intervals)
    plt.xlim(X_MIN, X_MAX)
    plt.ylim(Y_MIN, Y_MAX)
    plt.yticks([])

    # Create an instance of the Interval Seach Tree
    tree = IntervalST()

    # Add the intervals to the Interval Seach Tree
    for interval in intervals:
        tree.add(interval)

    # Define the interval search and plot it
    interval_search = Interval((random.uniform(X_MIN, X_MAX), random.uniform(X_MIN, X_MAX)))
    plt.plot([interval_search.start, interval_search.start], [Y_MIN, Y_MAX], '--', color = 'gray', linewidth=0.75)
    plt.plot([interval_search.end, interval_search.end], [Y_MIN, Y_MAX], '--', color = 'gray', linewidth=0.75)

    # Get the elements in the tree that intersect the interval request
    intersection_list = list(tree.intersects(interval_search))

    # Plot the solution
    for i, interval in enumerate(intervals):
        if interval in intersection_list:
            interval.draw(i, 'red')
        else:
            interval.draw(i, 'gray')

    interval_search.draw(-1, 'blue')
    plt.show()


if __name__ == "__main__":
    main()