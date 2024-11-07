import heapq
import matplotlib.pyplot as plt
from enum import Enum
from typing import List
from utils import Line, RedBlackBST


class EventType(Enum):
    """
    An enumeration representing the types of events in the sweep line algorithm.

    Attributes:
        START_LINE (int): Event type for the start of a horizontal line.
        VERTICAL_LINE (int): Event type for a vertical line.
        END_LINE (int): Event type for the end of a horizontal line.
    """

    START_LINE = 1
    VERTICAL_LINE = 2
    END_LINE = 3


class Event:
    """
    A class representing an event in the sweep line algorithm.

    Attributes:
        line (Line): The line associated with the event.
        event_type (EventType): The type of the event.
        x_coordinate (float): The x-coordinate of the event.

    Methods:
        __lt__(other): Compares this event with another event for ordering.
        __str__(): Returns a string representation of the Event object.
    """
    def __init__(self, line: Line, event_type: EventType, x_coordinate: float):
        """
        Initializes an Event object.

        Args:
            line (Line): The line associated with the event.
            event_type (EventType): The type of the event.
            x_coordinate (float): The x-coordinate of the event.
        """
        self.line = line
        self.event_type = event_type
        self.x_coordinate = x_coordinate

    def __lt__(self, other: 'Event') -> bool:
        """
        Compares this event with another event for ordering.

        Args:
            other (Event): The other event to compare with.

        Returns:
            bool: True if this event is less than the other event, False otherwise.
        """
        if self.x_coordinate == other.x_coordinate:
            return self.event_type.value < other.event_type.value
        return self.x_coordinate < other.x_coordinate

    def __str__(self):
        """Returns a string representation of the Event object."""
        return f"{self.x_coordinate}"


def create_event(line: Line, event_queue: List[Event]) -> None:
    """
    Creates events for a given line and adds them to the event queue.

    Args:
        line (Line): The line for which to create events.
        event_queue (List[Event]): The event queue to which the events will be added.
    """
    # Vertical line
    if line.x1 == line.x2:
        heapq.heappush(event_queue, Event(line, EventType.VERTICAL_LINE, line.x1))

    # Horizontal line
    elif line.y1 == line.y2:
        heapq.heappush(event_queue, Event(line, EventType.START_LINE, line.x1))
        heapq.heappush(event_queue, Event(line, EventType.END_LINE, line.x2))


def handle_events(event_queue: List[Event]) -> None:
    """
    Handles events from the event queue and processes intersections.

    Args:
        event_queue (List[Event]): The event queue containing events to be processed.
    """
    tree = RedBlackBST()

    while event_queue:
        event = heapq.heappop(event_queue)

        # Start line event
        if event.event_type == EventType.START_LINE:
            tree.add(event.line.y1)

        # End line event
        elif event.event_type == EventType.END_LINE:
            del tree[event.line.y1]

        # Vertical line event
        else:
            y_intersections = tree.range(event.line.y1, event.line.y2)
            for y_coordinate in y_intersections:
                plt.plot(event.x_coordinate, y_coordinate, 'x', color = 'blue')
