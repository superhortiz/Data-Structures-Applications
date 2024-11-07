from matplotlib import pyplot as plt
import numpy as np


class Point2D:
    """
    A class to represent a point in 2D space.
    
    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        array (np.ndarray): A NumPy array representing the point's coordinates.

    Methods:
        distance_squared_to(that): Calculate the squared Euclidean distance to another point.
        distance_to(that): Calculate the Euclidean distance to another point.
        draw(): Draws the point represented by this object on a matplotlib plot.

    Special Methods:
        __eq__(): Check if this point is equal to another point.
        __lt__(): Check if this point is less than another point.
        __repr__(): Return a string representation of the point.
        __str__(): Return a string representation of the point.
    """

    def __init__(self: 'Point2D', x: float, y: float) -> None:
        """
        Initialize the Point2D object with x and y coordinates.

        Args:
            x (float): The x-coordinate of the point.
            y (float): The y-coordinate of the point.

        Raises:
            ValueError: If x or y are not valid values.
        """
        if not isinstance(x, float) or not isinstance(y, float):
            raise ValueError("Coordinates must be numbers (float).")

        self._x = x
        self._y = y
        self._array = np.array([self._x, self._y])

    @property
    def x(self: 'Point2D') -> float:
        """
        Get the x-coordinate of the point.

        Returns:
            float: The x-coordinate of the point.
        """
        return self._x

    @property
    def y(self: 'Point2D') -> float:
        """
        Get the y-coordinate of the point.

        Returns:
            float: The y-coordinate of the point.
        """
        return self._y

    @property
    def array(self: 'Point2D') -> np.ndarray:
        """
        Get the NumPy array representing the point's coordinates.

        Returns:
            np.ndarray: A NumPy array [x, y].
        """
        return self._array

    def distance_to(self: 'Point2D', that: 'Point2D') -> float:
        """
        Calculate the Euclidean distance to another point.

        Args:
            that (Point2D): Another point to which the distance is calculated.

        Returns:
            float: The Euclidean distance to the other point.

        Raises:
            ValueError: If 'that' is not a Point2D object.
        """
        if not isinstance(that, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        return self.distance_squared_to(that) ** 0.5

    def distance_squared_to(self: 'Point2D', that: 'Point2D') -> float:
        """
        Calculate the squared Euclidean distance to another point.

        Args:
            that (Point2D): Another point to which the squared distance is calculated.

        Returns:
            float: The squared Euclidean distance to the other point.

        Raises:
            ValueError: If 'that' is not a Point2D object.
        """
        if not isinstance(that, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        return (self.x - that.x) ** 2 + (self.y - that.y) ** 2

    def draw(self: 'Point2D', color: str = 'black') -> None:
        """
        Draws the point represented by this object on a matplotlib plot.
        The point is plotted as a black circle.
        """
        plt.plot(self.x, self.y, 'o', color = color, markersize = 4)

    def __eq__(self: 'Point2D', that: 'Point2D') -> bool:
        """
        Check if this point is equal to another point.

        Args:
            that (Point2D): Another point to compare with.

        Returns:
            bool: True if the points are equal, False otherwise.

        Raises:
            ValueError: If 'that' is not a Point2D object.
        """
        if not isinstance(that, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        return self.x == that.x and self.y == that.y

    def __lt__(self: 'Point2D', that: 'Point2D') -> bool:
        """
        Check if this point is less than another point.

        Args:
            that (Point2D): Another point to compare with.

        Returns:
            bool: True if this point is less than the other point, False otherwise.

        Raises:
            ValueError: If 'that' is not a Point2D object.
        """
        if not isinstance(that, Point2D):
            raise ValueError("Argument must be a Point2D object.")

        if self.y != that.y:
            return self.y < that.y

        return self.x < that.x

    def __repr__(self: 'Point2D') -> str:
        """
        Return a string representation of the point.

        Returns:
            str: A string representation of the point in the format Point2D(x, y).
        """
        return f"{__class__.__name__}({self.x:.2f}, {self.y:.2f})"

    def __str__(self: 'Point2D') -> str:
        """
        Return a string representation of the point.

        Returns:
            str: A string representation of the point in the format (x, y).
        """
        return f"({self.x:.2f}, {self.y:.2f})"