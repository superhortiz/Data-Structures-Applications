import pygame
import numpy as np
from scipy.spatial import KDTree
from multiprocessing import Pool
from typing import List


class VerletObject:
    """
    Represents a physical object using Verlet integration for motion simulation.

    Attributes:
        position (np.ndarray): The current position of the object as a 2D array (x, y).
        position_last (np.ndarray): The previous position of the object for integration.
        acceleration (np.ndarray): The current acceleration of the object as a 2D array.
        radius (float): The radius of the object.
        color (np.ndarray): The color of the object as an RGB tuple.
        density (float): The density of the object.
        mass (float): The mass of the object, calculated from its density and volume.
    """

    def __init__(
            self,
            position: np.ndarray,
            radius: float = 10.0,
            color: np.ndarray = np.array((255, 255, 255)),
            density: float = 1.0,
            ):
        """
        Initializes a VerletObject with a given position, radius, color, and density.

        Args:
            position (np.ndarray): The initial position of the object as a 2D array (x, y).
            radius (float, optional): The radius of the object. Default is 10.0.
            color (tuple, optional): The color of the object as an RGB tuple. Default is (255, 255, 255).
            density (float, optional): The density of the object. Default is 1.0.
        """
        self.position: np.ndarray = np.asarray(position, dtype=float)
        self.position_last: np.ndarray = self.position.copy()
        self.acceleration: np.ndarray = np.zeros(2)
        self.radius: float = radius
        self.color: Tuple[int, int, int] = color
        self.density: float = density
        self.mass: float = self.density * (4/3) * np.pi * self.radius ** 3

    def update(self, dt: float) -> None:
        """
        Updates the position of the object using Verlet integration.

        Verlet integration formula:
            x(t+dt) = 2x(t) - x(t-dt) + a(t) dt**2
        Equivalent formula:
            x(t+dt) = x(t) + (x(t) - x(t-dt)) + a(t) dt**2

        Args:
            dt (float): The time step for the update.
        """
        displacement = self.position - self.position_last
        self.position_last[:] = self.position
        self.position += displacement + self.acceleration * dt**2
        self.acceleration.fill(0)

    def accelerate(self, a: np.ndarray) -> None:
        """
        Applies an acceleration to the object.

        Args:
            a (np.ndarray): The acceleration to be applied as an (ax, ay) vector.
        """
        self.acceleration += np.asarray(a, dtype=float)

    def set_velocity(self, v: np.ndarray, dt: float) -> None:
        """
        Sets the velocity of the object by modifying the last position.

        Args:
            v (np.ndarray): The velocity to be set as a (vx, vy) vector.
            dt (float): The time step used to set the velocity.
        """
        self.position_last = self.position - np.asarray(v, dtype=float) * dt

    def add_velocity(self, v: np.ndarray, dt: float) -> None:
        """
        Adds a velocity to the object by modifying the last position.

        Args:
            v (np.ndarray): The velocity to be added as a (vx, vy) vector.
            dt (float): The time step used to add the velocity.
        """
        self.position_last -= np.asarray(v, dtype=float) * dt

    def get_velocity(self, dt: float) -> np.ndarray:
        """
        Calculates and returns the current velocity of the object.

        Args:
            dt (float): The time step used to calculate the velocity.

        Returns:
            numpy.ndarray: The current velocity as a (vx, vy) vector.
        """
        return (self.position - self.position_last) / dt


class Solver:
    """
    A class to simulate physical objects using Verlet integration and constraint handling.
    
    Attributes:
        sub_steps (int): The number of sub-steps in each frame.
        gravity (np.ndarray): The gravity vector applied to all objects.
        constraint_center (np.ndarray): The center of the circular constraint.
        constraint_radius (float): The radius of the circular constraint.
        objects (List[VerletObject]): List of Verlet objects in the simulation.
        kdtree (List[KDTree]): KDTree for efficient spatial queries.
        frame_dt (float): The duration of each frame.
        step_dt (float): The time step duration for each sub-step.
        epoch (int): The current epoch or simulation step.
    """

    def __init__(
            self,
            fps_rate: int = 30,
            sub_steps: int = 8,
            gravity: np.ndarray = np.array([0.0, 981.0]),
            constraint_center: np.ndarray = np.array([0, 0]),
            constraint_radius: float = 100.0,
            ):
        """
        Initializes the Solver with given parameters.

        Args:
            fps_rate (int, optional): Frames per second rate. Default is 30.
            sub_steps (int, optional): Number of sub-steps per frame. Default is 8.
            gravity (np.ndarray, optional): Gravity vector. Default is np.array([0.0, 981.0]).
            constraint_center (np.ndarray, optional): Center of the circular constraint. Default is np.array([0, 0]).
            constraint_radius (float, optional): Radius of the circular constraint. Default is 100.0.
        """
        self.sub_steps: int = sub_steps
        self.gravity: np.ndarray = np.asarray(gravity, dtype=float)
        self.constraint_center: np.ndarray = np.asarray(constraint_center, dtype=float)
        self.constraint_radius: float = constraint_radius
        self.objects: List[VerletObject] = []
        self.kdtree: List[KDTree] = []
        self.frame_dt: float = 1.0 / fps_rate
        self.step_dt: float = self.frame_dt / self.sub_steps
        self.epoch: int = 0

    def add_object(self, position: np.ndarray, radius: float, color: np.ndarray) -> VerletObject:
        """
        Adds a new Verlet object to the solver.

        Args:
            position (np.ndarray): The initial position of the object as an (x, y) coordinate.
            radius (float): The radius of the object.
            color (tuple): The color of the object as an RGB tuple.

        Returns:
            VerletObject: The newly created Verlet object.
        """
        new_object = VerletObject(position, radius, color)
        self.objects.append(new_object)
        return new_object

    def apply_gravity(self) -> None:
        """
        Applies gravity to all Verlet objects.
        """
        [obj.accelerate(self.gravity) for obj in self.objects]

    def update_objects(self, dt: float) -> None:
        """
        Updates the positions of all Verlet objects.

        Args:
            dt (float): The time step for the update.
        """
        [obj.update(dt) for obj in self.objects]

    def set_object_velocity(self, obj: VerletObject, v: np.ndarray) -> None:
        """
        Sets the velocity of a specific object.

        Args:
            obj (VerletObject): The Verlet object whose velocity is to be set.
            v (tuple): The velocity to be set as a (vx, vy) vector.
        """
        obj.set_velocity(v, self.step_dt)

    def build_kdtree(self) -> None:
        """
        Builds a KDTree for efficient spatial queries of object positions.
        """
        if self.epoch % 2 != 0:
            return

        positions = np.empty((len(self.objects), 2), dtype=float)
        for i, obj in enumerate(self.objects):
            positions[i] = obj.position
        self.kdtree = KDTree(positions, balanced_tree=False)

    def update(self) -> None:
        """
        Updates the simulation for each sub-step.
        """
        self.build_kdtree()

        for _ in range(self.sub_steps):
            self.apply_gravity()
            self.check_collisions(self.step_dt)
            self.apply_constraint()
            self.update_objects(self.step_dt)

        self.epoch += 1

    def check_collisions(self, dt: float) -> None:
        """
        Checks and resolves collisions between Verlet objects.

        Args:
            dt (float): The time step for the collision check.
        """
        restitution_coefficient = 0.9

        for object_1 in self.objects:
            query_radius = object_1.radius * 2
            nearby_indices = self.kdtree.query_ball_point(object_1.position,
                             query_radius, eps=0.1, p=2, workers=2, return_sorted=False)
            for index in nearby_indices:
                object_2 = self.objects[index]
                if object_1 != object_2:
                    position_difference = object_1.position - object_2.position
                    squared_distance = np.dot(position_difference, position_difference)
                    min_distance = object_1.radius + object_2.radius

                    if squared_distance < min_distance**2:
                        distance = np.sqrt(squared_distance)
                        normal_vector = position_difference / distance
                        mass_ratio1 = object_1.mass / (object_1.mass + object_2.mass)
                        delta = 0.5 * restitution_coefficient * (distance - min_distance)

                        object_1.position -= normal_vector * ((1 - mass_ratio1) * delta)
                        object_2.position += normal_vector * (mass_ratio1 * delta)

    def set_constraint(self, position: np.ndarray, radius: float) -> None:
        """
        Sets the constraint parameters for the simulation.

        Args:
            position (tuple): The center position of the constraint as an (x, y) coordinate.
            radius (float): The radius of the constraint.
        """
        self.constraint_center = np.asarray(position, dtype=float)
        self.constraint_radius = radius

    def apply_constraint(self) -> None:
        """
        Applies the constraint to all Verlet objects, keeping them within bounds.
        """
        for obj in self.objects:
            position_difference = self.constraint_center - obj.position
            distance = np.linalg.norm(position_difference)
            if distance + obj.radius > self.constraint_radius:
                normal_vector = position_difference / distance
                obj.position = self.constraint_center - normal_vector * (self.constraint_radius - obj.radius)