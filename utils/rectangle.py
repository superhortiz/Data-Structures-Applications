import matplotlib.pyplot as plt
from typing import Tuple


class RectHV:
    """
    Represents a 2D axis-aligned rectangle with coordinates (xmin, ymin) and (xmax, ymax).

    Attributes:
        xmin (float): The minimum x-coordinate.
        ymin (float): The minimum y-coordinate.
        xmax (float): The maximum x-coordinate.
        ymax (float): The maximum y-coordinate.

    Methods:
        contains(point): Checks if the rectangle contains a given point.
        distance_squared_to(point): Computes the square of the Euclidean distance from the rectangle to a point.
        distance_to(point): Computes the Euclidean distance from the rectangle to a point.
        draw(): Draws the rectangle represented by this object on a matplotlib plot.
        intersects(other): Checks if the rectangle intersects with another rectangle.
        intersection(other): Computes the intersection of this rectangle with another rectangle.

    Special Methods:
        __eq__(other): Checks if this rectangle is equal to another rectangle.
        __repr__(): Returns a string representation of the rectangle.
        __str__(): Returns a string representation of the rectangle.
    """

    def __init__(self: 'RectHV', xmin: float, ymin: float, xmax: float, ymax: float) -> None:
        """
        Initializes a new rectangle with the specified coordinates.
        
        Args:
            xmin (float): The minimum x-coordinate.
            ymin (float): The minimum y-coordinate.
            xmax (float): The maximum x-coordinate.
            ymax (float): The maximum y-coordinate.
        """

        self._xmin = min(xmin, xmax)
        self._ymin = min(ymin, ymax)
        self._xmax = max(xmin, xmax)
        self._ymax = max(ymin, ymax)

    @property
    def xmin(self: 'RectHV') -> float:
        """
        Returns the minimum x-coordinate of the rectangle.
        
        Returns:
            float: The minimum x-coordinate.
        """
        return self._xmin

    @property
    def ymin(self: 'RectHV') -> float:
        """
        Returns the minimum y-coordinate of the rectangle.
        
        Returns:
            float: The minimum y-coordinate.
        """
        return self._ymin

    @property
    def xmax(self: 'RectHV') -> float:
        """
        Returns the maximum x-coordinate of the rectangle.
        
        Returns:
            float: The maximum x-coordinate.
        """
        return self._xmax

    @property
    def ymax(self: 'RectHV') -> float:
        """
        Returns the maximum y-coordinate of the rectangle.
        
        Returns:
            float: The maximum y-coordinate.
        """
        return self._ymax

    def contains(self: 'RectHV', point: 'Point2D') -> bool:
        """
        Checks if the rectangle contains a given point.
        
        Args:
            point (Point2D): The point to check.
        
        Returns:
            bool: True if the rectangle contains the point, False otherwise.

        Raises:
            ValueError: If 'point' is not a Point2D object.
        """
        if not isinstance(point, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        return self.xmin <= point.x <= self.xmax and self.ymin <= point.y <= self.ymax

    def intersects(self: 'RectHV', other: 'RectHV') -> bool:
        """
        Checks if the rectangle intersects with another rectangle.
        
        Args:
            other (RectHV): The other rectangle to check.
        
        Returns:
            bool: True if the rectangles intersect, False otherwise.

        Raises:
            ValueError: If 'other' is not a RectHV object.
        """
        if not isinstance(other, RectHV):
            raise ValueError("Argument must be a RectHV object.")

        return self.xmax >= other.xmin and self.xmin <= other.xmax and self.ymax >= other.ymin and self.ymin <= other.ymax

    def intersection(self: 'RectHV', other: 'RectHV') -> Tuple[float, float, float, float]:
        """
        Computes the intersection of this rectangle with another rectangle.

        Args:
            other (RectHV): Another rectangle to intersect with.

        Returns:
            Tuple[float, float, float, float]: A tuple containing the coordinates of the intersection rectangle
            in the form (xmin, ymin, xmax, ymax).
        """
        if self.intersects(other):
            xmin = max(self.xmin, other.xmin)
            xmax = min(self.xmax, other.xmax)
            ymin = max(self.ymin, other.ymin)
            ymax = min(self.ymax, other.ymax)
            return xmin, ymin, xmax, ymax

    def distance_to(self: 'RectHV', point: 'Point2D') -> float:
        """
        Computes the Euclidean distance from the rectangle to a point.
        
        Args:
            point (Point2D): The point to compute the distance to.
        
        Returns:
            float: The Euclidean distance to the point.

        Raises:
            ValueError: If 'point' is not a Point2D object.
        """
        if not isinstance(point, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        return self.distance_squared_to(point) ** 0.5

    def distance_squared_to(self: 'RectHV', point: 'Point2D') -> float:
        """
        Computes the square of the Euclidean distance from the rectangle to a point.
        
        Args:
            point (Point2D): The point to compute the distance to.
        
        Returns:
            float: The square of the Euclidean distance to the point.

        Raises:
            ValueError: If 'point' is not a Point2D object.
        """
        if not isinstance(point, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        dx, dy = 0, 0

        if point.x > self.xmax:
            dx = point.x - self.xmax
        elif point.x < self.xmin:
            dx = self.xmin - point.x
        if point.y > self.ymax:
            dy = point.y - self.ymax
        elif point.y < self.ymin:
            dy = self.ymin - point.y

        return dx ** 2 + dy ** 2

    def draw(self: 'RectHV') -> None:
        """
        Draws the rectangle represented by this object on a matplotlib plot.
        The rectangle is plotted using green lines.
        """
        x = [self.xmin, self.xmax, self.xmax, self.xmin, self.xmin]
        y = [self.ymin, self.ymin, self.ymax, self.ymax, self.ymin]

        plt.plot(x, y, 'b-')

    def __eq__(self: 'RectHV', other: 'RectHV') -> bool:
        """
        Checks if this rectangle is equal to another rectangle.
        
        Args:
            other (RectHV): The other rectangle to compare.
        
        Returns:
            bool: True if the rectangles are equal, False otherwise.

        Raises:
            ValueError: If 'other' is not a RectHV object.
        """
        if not isinstance(other, RectHV):
            raise ValueError("Argument must be a RectHV object.")

        return self.xmin == other.xmin and self.xmax == other.xmax and self.ymin == other.ymin and self.ymax == other.ymax

    def __repr__(self: 'RectHV') -> str:
        """
        Returns a string representation of the rectangle.

        Returns:
            str: The string representation of the rectangle.
        """
        return f"{__class__.__name__}({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax})"
