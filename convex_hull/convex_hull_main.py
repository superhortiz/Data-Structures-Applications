from matplotlib import pyplot as plt
from utils import Point2D
from random import uniform
from typing import List, Tuple
import matplotlib.animation as animation
import math
import numpy as np


MIN_COORD = 0
MAX_COORD = 10
NUMBER_OF_POINTS = 200


class ConvexHull:
    """
    A class to represent and compute the convex hull of a set of 2D points using the Graham scan algorithm.

    Attributes:
        points (list[Point2D]): A list of Point2D objects representing the input points.
        hull (list[Point2D]): A list of Point2D objects representing the points on the convex hull.

    Methods:
        animate(): Animates the process of constructing the convex hull using matplotlib.
        draw(): Draws the convex hull and the points using matplotlib.
    """
    def __init__(self, points: List[Point2D]) -> None:
        """
        Initialize the ConvexHull with a list of points.

        Args:
            points (list[Point2D]): A list of Point2D objects representing the points.
        """
        self.points = points

        # Get the point the lowest y-coordinate
        min_point = min(self.points)

        # Sort the points by their polar angle with respect to the point with the minimum coordinates
        self.points.sort(key = lambda x: self._polar_angle(min_point, x))

        # Include the first 2 points
        self.hull = self.points[:2]

        # Use the Graham scan algortihm
        self._graham_scan()

    def _graham_scan(self) -> None:
        """
        Perform the Graham scan algorithm to find the convex hull.
        """
        # Iterate over the list of points starting from the third point
        for i in range(2, len(self.points)):
            # While the last three points do not form a counterclockwise turn,
            # remove the last point from the hull
            while not self._is_ccw(self.hull[-2], self.hull[-1], self.points[i]):
                self.hull.pop()

            # Append the current point to the hull
            self.hull.append(self.points[i])

        # Add the first point
        self.hull.append(self.points[0])

    def draw(self) -> None:
        """
        Draw the convex hull and the points using matplotlib.
        """
        # Remove the tick labels on both axes
        plt.xticks([])
        plt.yticks([])

        # Draw all the lines
        for i in range(len(self.hull) - 1):
            plt.plot([self.hull[i + 1].x, self.hull[i].x], [self.hull[i + 1].y, self.hull[i].y], color = 'blue')

        # Draw all the points
        [point.draw() for point in self.points]

        # Draw vertex points
        [point.draw('blue') for point in self.hull]

        # Draw pivot point
        plt.plot(self.points[0].x, self.points[0].y, 'o', color='red', markersize = 5)
        plt.text(self.points[0].x + 0.1, self.points[0].y + 0.3, 'p', fontsize=12, color='red')

        # Show the plot
        plt.show()

    def animate(self) -> None:
        """
        Animate the process of constructing the convex hull using matplotlib.

        This method sets up the plot, initializes the animation, and defines the update function
        to show the step-by-step construction of the convex hull.
        """
        fig, ax = plt.subplots()

        # Set the background color
        ax.set_facecolor('lightgray')

        # Set the drawing limits
        ax.set_xlim(MIN_COORD - 1, MAX_COORD + 1)
        ax.set_ylim(MIN_COORD - 1, MAX_COORD + 1)

        # Remove the tick labels on both axes
        ax.set_xticks([])
        ax.set_yticks([])

        # Draw all the points
        [point.draw() for point in self.points]

        # Draw pivot point
        plt.plot(self.points[0].x, self.points[0].y, 'o', color='red', markersize=5)
        plt.text(self.points[0].x + 0.1, self.points[0].y + 0.3, 'p', fontsize=12, color='red')

        # Define lists of lines to draw
        x_data_line = []
        y_data_line = []
        x_data_line_seg = []
        y_data_line_seg = []
        line, = ax.plot(x_data_line, y_data_line, color='blue')
        line_seg, = ax.plot(x_data_line, y_data_line, '--', color='gray')

        # Auxiliar variables for animation
        self._index = 2
        self._first_visit = True
        hull_aux = self.points[:2]

        def update(frame: int) -> Tuple[plt.Line2D, plt.Line2D]:
            """
            Update function for the animation.

            Args:
                frame (int): The current frame number.

            Returns:
                tuple: Updated line and segment line objects.
            """
            # Draw line for the first 2 points
            if frame <= 1:
                x_data_line.append(self.hull[frame].x)
                y_data_line.append(self.hull[frame].y)
                line.set_data(x_data_line, y_data_line)

            # Graham scan representation
            elif self._index < len(self.points):
                # Draw segment line
                if self._first_visit:
                    x_data_line_seg = [hull_aux[-1].x, self.points[self._index].x]
                    y_data_line_seg = [hull_aux[-1].y, self.points[self._index].y]
                    self._index -= 1
                    self._first_visit = False

                else:
                    self._first_visit = True

                    # The new point forms a counterclockwise turn
                    if self._is_ccw(hull_aux[-2], hull_aux[-1], self.points[self._index]):
                        x_data_line_seg = []
                        y_data_line_seg = []
                        hull_aux.append(self.points[self._index])
                        x_data_line.append(self.points[self._index].x)
                        y_data_line.append(self.points[self._index].y)

                    # The new point does not form a counterclockwise turn
                    else:
                        hull_aux.pop()
                        x_data_line.pop()
                        y_data_line.pop()
                        x_data_line_seg = [hull_aux[-1].x, self.points[self._index].x]
                        y_data_line_seg = [hull_aux[-1].y, self.points[self._index].y]
                        self._index -= 1

                # Update the drawing
                self._index += 1
                line.set_data(x_data_line, y_data_line)
                line_seg.set_data(x_data_line_seg, y_data_line_seg)

            # Last step, complete solution
            else:
                # Draw vertex points in blue
                [ax.plot(point.x, point.y, 'o', color='blue', markersize=5) for point in self.hull]

                # Update the lines
                x_data_line_seg = []
                y_data_line_seg = []
                x_data_line.append(self.points[0].x)
                y_data_line.append(self.points[0].y)
                line.set_data(x_data_line, y_data_line)
                line_seg.set_data(x_data_line_seg, y_data_line_seg)

            return line, line_seg

        # Create the animation
        ani = animation.FuncAnimation(fig, update, frames=NUMBER_OF_POINTS**2, interval=50, repeat=False)

        # Show the plot
        plt.show()

    @staticmethod
    def _polar_angle(point_reference: Point2D, point: Point2D) -> float:
        """
        Calculate the polar angle between two points.

        Args:
            point_reference (Point2D): The reference point.
            point (Point2D): The point for which the polar angle is calculated.

        Returns:
            float: The polar angle between p0 and p1.
        """
        return math.atan2((point.y - point_reference.y), (point.x - point_reference.x))

    @staticmethod
    def _is_ccw(point_a: Point2D, point_b: Point2D, point_c: Point2D) -> bool:
        """
        Check if three points make a counterclockwise turn.

        Args:
            point_a (Point2D): The first point.
            point_b (Point2D): The second point.
            point_c (Point2D): The third point.

        Returns:
            bool: True if the points make a counterclockwise turn, False otherwise.
        """
        vector_1 = point_b.array - point_a.array
        vector_2 = point_c.array - point_b.array
        return np.cross(vector_1, vector_2) > 0


def main() -> None:
    """
    Example usage, generate random points
    """
    points = [Point2D(uniform(MIN_COORD, MAX_COORD), uniform(MIN_COORD, MAX_COORD)) for _ in range(NUMBER_OF_POINTS)]
    convex_hull = ConvexHull(points)
    convex_hull.animate()


if __name__ == "__main__":
    main()