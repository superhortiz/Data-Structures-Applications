from utils import RectHV
from .sweep_line_rectangles import create_event, handle_events
import matplotlib.pyplot as plt


def main() -> None:
    """
    Main function to set up and run the rectangle intersection simulation.
    """
    # Remove the tick labels on both axes
    plt.xticks([])
    plt.yticks([])
    event_queue = []

    # Create rectangles
    rectangles = [
        RectHV(0., 0., 4., 4.),
        RectHV(6., 6., 9., 9.5),
        RectHV(1., 1., 5., 3.),
        RectHV(7., 0., 9., 2.5),
        RectHV(2., 8., 5., 10.),
        RectHV(0., 7., 3., 9.),
        RectHV(4.5, 2., 7.5, 4.),
        RectHV(8., 5., 11., 9.),
        RectHV(10., 1., 13., 3.),
        RectHV(1., 11., 4., 13.),
        RectHV(5.5, 3.5, 6.5, 13),
        RectHV(0.5, 11.5, 12, 11.8),

    ]

    # Draw the rectangles and create events
    for rectangle in rectangles:
        rectangle.draw()
        create_event(rectangle, event_queue)

    # Handle the events by finding the intersections
    handle_events(event_queue)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()