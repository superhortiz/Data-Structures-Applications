import heapq
import matplotlib.pyplot as plt
from enum import Enum
from typing import List
from .rectangle_st import *
from utils import RectHV


class EventType(Enum):
    """
    An enumeration representing the types of events in the sweep line algorithm.

    Attributes:
        START_RECTANGLE (int): Event type for the start of a rectangle.
        END_RECTANGLE (int): Event type for the end of a rectangle.
    """

    START_RECTANGLE = 1
    END_RECTANGLE = 2


class Event:
    """
    A class representing an event in the sweep line algorithm.

    Attributes:
        rectangle (RectHV): The rectangle associated with the event.
        event_type (EventType): The type of the event.
        x_coordinate (float): The x-coordinate of the event.

    Methods:
        __lt__(other): Compares this event with another event for ordering.
        __str__(): Returns a string representation of the Event object.
    """

    def __init__(self, rectangle: RectHV, event_type: EventType, x_coordinate: float):
        """
        Initializes an Event object.

        Args:
            rectangle (RectHV): The rectangle associated with the event.
            event_type (EventType): The type of the event.
            x_coordinate (float): The x-coordinate of the event.
        """

        self.rectangle = rectangle
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


def create_event(rectangle: RectHV, event_queue: List[Event]) -> None:
    """
    Creates events for a given rectangle and adds them to the event queue.

    Args:
        rectangle (RectHV): The rectangle for which to create events.
        event_queue (List[Event]): The event queue to which the events will be added.
    """
    # Left endpoint
    heapq.heappush(event_queue, Event(rectangle, EventType.START_RECTANGLE, rectangle.xmin))

    # Right endpoint
    heapq.heappush(event_queue, Event(rectangle, EventType.END_RECTANGLE, rectangle.xmax))


def handle_events(event_queue: List[Event]) -> None:
    """
    Handles events from the event queue and processes intersections.

    Args:
        event_queue (List[Event]): The event queue containing events to be processed.
    """
    tree = RectangleST()

    while event_queue:
        event = heapq.heappop(event_queue)

        # Start rectangle event
        if event.event_type == EventType.START_RECTANGLE:
            rectangle = event.rectangle

            # Search for intersections
            intersections = list(tree.intersects(rectangle))

            # Draw the intersections
            for rect_intersected in intersections:
                xmin, ymin, xmax, ymax = rectangle.intersection(rect_intersected)
                x = [xmin, xmax, xmax, xmin, xmin]
                y = [ymin, ymin, ymax, ymax, ymin]
                plt.fill(x, y, color='gray', alpha=0.3)

            # Add the current rectangle to the queue
            tree.add(rectangle)

        # End rectangle event
        elif event.event_type == EventType.END_RECTANGLE:

            # Remove the rectangle to the queue
            del tree[event.rectangle.ymin]
