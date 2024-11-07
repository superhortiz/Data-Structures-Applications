import matplotlib.pyplot as plt


class Line:
    """
    A class representing a line segment in a 2D plane.

    Attributes:
        x1 (float): The x-coordinate of the first point.
        y1 (float): The y-coordinate of the first point.
        x2 (float): The x-coordinate of the second point.
        y2 (float): The y-coordinate of the second point.

    Methods:
        draw(): Draws the line using Matplotlib.
        __str__(): Returns a string representation of the Line object.
    """

    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """
        Initializes a Line object with the given coordinates.

        Args:
            x1 (float): The x-coordinate of the first point.
            y1 (float): The y-coordinate of the first point.
            x2 (float): The x-coordinate of the second point.
            y2 (float): The y-coordinate of the second point.
        """
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)

    def draw(self) -> None:
        """Draws the line using Matplotlib."""
        plt.plot([self.x1, self.x2], [self.y1, self.y2], color = 'gray')

    def __str__(self) -> str:
        """Returns a string representation of the Line object."""
        return f"Line({self.x1}, {self.y1}, {self.x2}, {self.y2})"
