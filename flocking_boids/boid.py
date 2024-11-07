import pygame
import numpy as np
from typing import List, Tuple


COHESION_STRENGTH: int = 0.004
MINIMUM_DISTANVE: int = 20
ALIGNMENT_FACTOR: int = 10
REPULSION_FORCE_BOUNDARIES: float = 0.75
BOUNDARY_THRESHOLD: int = 100
MAX_VELOCITY: int = 6


class Boid:
    """
    A class to represent a boid in a flocking simulation.

    Attributes:
        position (np.ndarray): Current position of the boid.
        velocity (np.ndarray): Current velocity of the boid.
        color (str): Color of the boid.

    Methods:
        cohesion(neighbors): Tendency of boids to move towards the center of the flock.
        separation(neighbors): Tendency of boids to maintain a minimum distance from nearby boids.
        alignment(neighbors): Tendency of boids to match their velocity with nearby boids.
        update(neighbors): Update the boid's position and velocity based on the behaviors of cohesion, separation, and alignment.
    """

    def __init__(self, color: np.ndarray, width: int, height: int) -> None:
        """
        Initializes a new instance of the Boid class.

        Args:
            color (np.ndarray): Color of the boid.
        """
        self.color = color
        self.width = width
        self.height = height
        self.position = np.random.uniform(0, 1, 2) * [self.width, self.height]
        self.velocity = np.random.rand(2) * 2

    def cohesion(self, neighbors: List['Boid']) -> None:
        """
        Tendency of boids to move towards the center of the flock.
        For this simulation, it just considers the nearby boids.

        Args:
            neighbors (List[Boid]): List of neighboring boids.
        """
        # Average position
        center = np.mean([boid.position for boid in neighbors], axis=0)

        # Velocity update for cohesion
        self.velocity += (center - self.position) * COHESION_STRENGTH

    def separation(self, neighbors: List['Boid']) -> None:
        """
        Tendency of boids to maintain a minimum distance from nearby boids.

        Args:
            neighbors (List[Boid]): List of neighboring boids.
        """
        for neighbor in neighbors:
            if neighbor != self:

                # Calculate distance between self and neighbor
                distance = np.linalg.norm(self.position - neighbor.position)

                if distance < MINIMUM_DISTANVE:
                    self.velocity -= (neighbor.position - self.position) / (distance + 1e-4)

    def alignment(self, neighbors: List['Boid']) -> None:
        """
        Tendency of boids to match their velocity with nearby boids.

        Args:
            neighbors (List[Boid]): List of neighboring boids.
        """
        # Average velocity
        avg_nearby_velocity = np.mean([boid.velocity for boid in neighbors], axis=0)

        # Update velocity
        self.velocity += (avg_nearby_velocity - self.velocity) / ALIGNMENT_FACTOR

    def update(self, neighbors: List['Boid']) -> None:
        """
        Update the boid's position and velocity based on the behaviors of cohesion, separation, and alignment.

        Args:
            neighbors (List[Boid]): List of neighboring boids.
        """
        # Apply cohesion, separation and alignment
        self.cohesion(neighbors)
        self.separation(neighbors)
        self.alignment(neighbors)

        # Limit the velocity not to cross the boundaries (boundary repulsion)
        if self.position[0] < BOUNDARY_THRESHOLD:
            repulsion = REPULSION_FORCE_BOUNDARIES * (BOUNDARY_THRESHOLD - self.position[0]) / BOUNDARY_THRESHOLD
            self.velocity[0] += repulsion
        elif self.position[0] > self.width - BOUNDARY_THRESHOLD:
            repulsion = REPULSION_FORCE_BOUNDARIES * (self.position[0] - (self.width - BOUNDARY_THRESHOLD)) / BOUNDARY_THRESHOLD
            self.velocity[0] -= repulsion

        if self.position[1] < BOUNDARY_THRESHOLD:
            repulsion = REPULSION_FORCE_BOUNDARIES * (BOUNDARY_THRESHOLD - self.position[1]) / BOUNDARY_THRESHOLD
            self.velocity[1] += repulsion
        elif self.position[1] > self.height - BOUNDARY_THRESHOLD:
            repulsion = REPULSION_FORCE_BOUNDARIES * (self.position[1] - (self.height - BOUNDARY_THRESHOLD)) / BOUNDARY_THRESHOLD
            self.velocity[1] -= repulsion

        # Limit the velocity magnitude
        velocity_magnitude = np.linalg.norm(self.velocity)
        self.velocity = self.velocity / velocity_magnitude * min(velocity_magnitude, MAX_VELOCITY)

        # Update the position
        self.position += self.velocity


def draw_fish(screen, x_coordinate: int, y_coordinate: int, width: int, color: np.ndarray, velocity: np.ndarray) -> None:
    """
    Draws a fish on the screen at the given coordinates with the specified width, color, and velocity.

    Args:
        x_coordinate (int): The x-coordinate of the fish's position.
        y_coordinate (int): The y-coordinate of the fish's position.
        width (int): The width of the fish.
        color (np.ndarray): The color of the fish.
        velocity (np.ndarray): The velocity of the fish.
    """
    height = width // 2

    # Draw the body of the fish (ellipse)
    pygame.draw.ellipse(screen, color, (x_coordinate, y_coordinate, width, height))

    if velocity[0] >= 0:
        # Draw the tail of the fish (polygon)
        pygame.draw.polygon(screen, color, [(x_coordinate, y_coordinate + height // 2),
            (x_coordinate - width // 3, y_coordinate + height), (x_coordinate - width // 3, y_coordinate)])

        pygame.draw.polygon(screen, color, [(x_coordinate + width // 2, y_coordinate),
        (x_coordinate + width // 4, y_coordinate), (x_coordinate + width // 6, y_coordinate - height // 2)])

    else:
        # Draw the tail of the fish (polygon)
        pygame.draw.polygon(screen, color, [(x_coordinate + width, y_coordinate + height // 2),
            (x_coordinate + width + width // 3, y_coordinate + height), (x_coordinate + width + width // 3, y_coordinate)])

        pygame.draw.polygon(screen, color, [(x_coordinate + width // 2, y_coordinate),
            (x_coordinate + (3 * width) // 4, y_coordinate), (x_coordinate + (5 * width) // 6, y_coordinate - height // 2)])
