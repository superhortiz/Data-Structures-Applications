import random
from .sweep_line_algorithm import *


def main() -> None:
    """
    Main function to set up and run the line intersection simulation.
    """
    # Remove the tick labels on both axes
    plt.xticks([])
    plt.yticks([])

    X_MIN = 0
    Y_MIN = 0
    X_MAX = 10
    Y_MAX = 10
    lines = []
    event_queue = []

    # Create lines
    for _ in range(40):
        x = random.uniform(X_MIN, X_MAX)
        lines.append(Line(x, random.uniform(Y_MIN, Y_MAX), x, random.uniform(Y_MIN, Y_MAX)))
        y = random.uniform(Y_MIN, Y_MAX)
        lines.append(Line(random.uniform(Y_MIN, Y_MAX), y, random.uniform(Y_MIN, Y_MAX), y))

    # Draw the lines and create events
    for line in lines:
        line.draw()
        create_event(line, event_queue)

    # Handle the events by finding the intersections
    handle_events(event_queue)

    plt.show()


if __name__ == "__main__":
    main()