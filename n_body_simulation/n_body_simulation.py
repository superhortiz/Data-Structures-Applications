import numpy as np
import pygame
from scipy.spatial import KDTree
from typing import List, Tuple


# Constants (Arbitrary values for simulation purposes; not based on physical constants)
G = 100_000
MAX_VEL = 600


class Body:
    """
    Represents a celestial body in an N-body simulation.

    Attributes:
        position (np.ndarray): The position of the body as a numpy array.
        velocity (np.ndarray): The velocity of the body as a numpy array.
        mass (float): The mass of the body.
        acceleration (np.ndarray): The acceleration of the body, initialized to zero.
        color (np.ndarray): The color of the body for visualization as a numpy array (for Pygame).
        diameter (int): The diameter of the body for visualization.
        move (bool): Flag indicating if the body is allowed to move.
    """

    def __init__(self, position: np.ndarray, velocity: np.ndarray, mass: float,
        color: np.ndarray, diameter: int, move: bool = True) -> None:
        """
        Initializes a Body instance.

        Args:
            position (np.ndarray): The initial position of the body as a numpy array.
            velocity (np.ndarray): The initial velocity of the body as a numpy array.
            mass (float): The mass of the body.
            color (np.ndarray): The color of the body for visualization as a numpy array (for Pygame).
            diameter (int): The diameter of the body for visualization.
            move (bool, optional): Flag indicating if the body is allowed to move. Defaults to True.
        """
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.mass = mass
        self.acceleration = np.zeros(2)
        self.color = color
        self.diameter = diameter
        self.move = move


class NBodySimulation:
    """
    Simulates an N-body system using the Appel algorithm.

    Attributes:
        bodies (List[Body]): List of Body instances in the simulation.
        kdtree (KDTree): KDTree for efficient spatial queries.
    """

    def __init__(self, bodies: List['Body']) -> None:
        """
        Initializes the NBodySimulation instance.

        Args:
            bodies (List[Body]): List of Body instances to be simulated.
        """
        self.bodies = bodies
        self.kdtree = None

    @staticmethod
    def compute_multipole_moments(bodies: List['Body']) -> Tuple[np.ndarray, float, np.ndarray, np.ndarray]:
        """
        Computes the multipole moments for a cluster of bodies.

        Args:
            bodies (List[Body]): List of Body instances in the cluster.

        Returns:
            Tuple[np.ndarray, float, np.ndarray, np.ndarray]: Center of mass, total mass, dipole moment, and quadrupole moment.
        """

        # Calculate the total mass
        total_mass = sum(body.mass for body in bodies)

        # Calculate the center of mass
        monopole = np.mean([body.position * body.mass for body in bodies], axis=0) / total_mass
        
        # Calculate the dipole moment (center of mass)
        dipole = sum(body.mass * (body.position - monopole) for body in bodies)
        
        # Initialize the quadrupole moment
        quadrupole = np.zeros((2, 2))
        
        for body in bodies:
            mass = body.mass
            position = body.position - monopole
            quadrupole += mass * (3 * np.outer(position, position) - np.eye(2) * np.dot(position, position))
        
        return monopole, total_mass, dipole, quadrupole

    def compute_force_cluster(self, body: 'Body', cluster: List['Body']) -> np.ndarray:
        """
        Computes the gravitational force on a body from a cluster of bodies using multipole moments.

        Args:
            body (Body): The body on which the force is being computed.
            cluster (List[Body]): The cluster of bodies exerting the force.

        Returns:
            np.ndarray: The computed force as a numpy array.
        """
        monopole, total_mass, dipole, quadrupole = self.compute_multipole_moments(cluster)
        r = body.position - monopole
        r_mag = np.linalg.norm(r)
        
        force = -G * total_mass * r / np.power(r_mag, 3)
        force -= G * (3 * np.dot(dipole, r) * r - dipole * np.power(r_mag, 2)) / np.power(r_mag, 5)
        
        for j in range(2):
            for k in range(2):
                force -= G * quadrupole[j, k] * (5 * r[j] * r[k] - (j == k) * np.power(r_mag, 2)) / np.power(r_mag, 7)
        
        return force

    def simplified_force_cluster(self, body: 'Body', cluster: List['Body']) -> np.ndarray:
        """
        Computes a simplified gravitational force on a body from a cluster of bodies.

        Args:
            body (Body): The body on which the force is being computed.
            cluster (List[Body]): The cluster of bodies exerting the force.

        Returns:
            np.ndarray: The computed force as a numpy array.
        """
        position_cluster, mass_cluster, _, _ = self.compute_multipole_moments(cluster)

        distance = np.linalg.norm(body.position - position_cluster)
        force = min(G * body.mass * mass_cluster / np.power(distance, 2), 900_000)
        direction = (position_cluster - body.position) / distance
        return force * direction

    def appel_algorithm(self, theta: float) -> None:
        """
        Applies the Appel algorithm to compute forces on all bodies in the simulation.

        Args:
            theta (float): Threshold parameter for the Appel algorithm.
        """

        for i, body in enumerate(self.bodies):
            body.acceleration = np.zeros(2)  # Reset acceleration

            # Query nearby bodies using K-d tree
            nearby_indices = self.kdtree.query_ball_point(body.position, theta)

            # Compute forces for nearby bodies
            for index in nearby_indices:
                if index != i:  # Exclude self
                    other_body = self.bodies[index]
                    distance = np.linalg.norm(body.position - other_body.position)
                    force = min(G * body.mass * other_body.mass / np.power(distance, 2), 500_000)
                    direction = (other_body.position - body.position) / (distance + 1e-3)
                    body.acceleration += force * direction / body.mass

            # Computer forces for far clusters
            cluster = [self.bodies[k] for k in range(len(self.bodies)) if k not in nearby_indices and k != i]

            if cluster:
                force_cluster = self.compute_force_cluster(body, cluster)
                body.acceleration += force_cluster / body.mass

    def rebuild_tree(self) -> None:
        """
        Rebuilds the KDTree for the current positions of the bodies.
        """
        positions = np.array([body.position for body in self.bodies])
        self.kdtree = KDTree(positions) 

    def update_velocities(self, dt: float) -> None:
        """
        Updates the velocities of all bodies based on their accelerations.

        Args:
            dt (float): Time step for the update.
        """
        for body in self.bodies:
            body.velocity += body.acceleration * dt

            # Limit the norm of the velocity to 300
            velocity_norm = np.linalg.norm(body.velocity)

            if velocity_norm > MAX_VEL:
                body.velocity = body.velocity * (MAX_VEL / velocity_norm)

    def update_positions(self, dt: float) -> None:
        """
        Updates the positions of all bodies based on their velocities.

        Args:
            dt (float): Time step for the update.
        """
        for body in self.bodies:
            if body.move:
                body.position += body.velocity * dt

    def update(self, dt: float, theta: float, rebuild: bool) -> None:
        """
        Updates the simulation for a single time step.

        Args:
            dt (float): Time step for the simulation.
            theta (float): Threshold parameter for the Appel algorithm.
            rebuild (bool): Flag indicating whether to rebuild the KDTree.
        """
        if rebuild:
            self.rebuild_tree()
        self.appel_algorithm(theta)
        self.update_velocities(dt)
        self.update_positions(dt)
