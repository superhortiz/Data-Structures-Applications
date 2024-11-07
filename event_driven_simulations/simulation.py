import heapq
import numpy as np
import pygame
from copy import deepcopy
from typing import List, Tuple


class Particle:
    """
    A class to represent a particle in a 2D box.

    Attributes:
        position (np.ndarray): The position of the particle.
        velocity (np.ndarray): The velocity of the particle.
        radius (float): The radius of the particle.
        color (Tuple[int, int, int]): The color of the particle in RGB format.
        box_width (float): The width of the box containing the particle.
        box_height (float): The height of the box containing the particle.
        density (float): The density of the particle.
        mass (float): The mass of the particle.
        collision_count (int): The number of collisions the particle has experienced.
        epsilon_collision(float): Coefficient of Restitution (COR) for collisions between particles,
            0 (perfectly inelastic) to 1 (perfectly elastic).
        epsilon_walls(float): Coefficient of Restitution (COR) for collisions between particles and walls,
            0 (perfectly inelastic) to 1 (perfectly elastic).

    Methods:
        move(delta_time): Updates the position of the particle based on its velocity and the elapsed time.
        draw(screen): Draws the particle on the given Pygame screen.
        time_to_hit(other): Calculates the time until this particle collides with another particle.
        time_to_hit_vert_wall(): Calculates the time until this particle collides with a vertical wall.
        time_to_hit_horz_wall(): Calculates the time until this particle collides with a horizontal wall.
        bounce_off(other): Handles the collision with another particle and updates velocities accordingly.
        bounce_off_vert_wall(): Handles the collision with a vertical wall and updates velocity accordingly.
        bounce_off_horz_wall(): Handles the collision with a horizontal wall and updates velocity accordingly.
    """

    def __init__(self,
                position: Tuple[float, float],
                velocity: Tuple[float, float],
                radius: float,
                color: Tuple[int, int, int],
                box_width: float,
                box_height: float,
                density: float = 1.,
                epsilon_collision: float = 1.,
                epsilon_walls: float = 1.):
        """
        Initializes a new particle.

        Args:
            position (Tuple[float, float]): The initial position of the particle.
            velocity (Tuple[float, float]): The initial velocity of the particle.
            radius (float): The radius of the particle.
            color (Tuple[int, int, int]): The color of the particle in RGB format.
            box_width (float): The width of the box containing the particle.
            box_height (float): The height of the box containing the particle.
            density (float, optional): The density of the particle. Defaults to 1.0.
            epsilon_collision(float): Coefficient of Restitution (COR) for collisions between particles,
                0 (perfectly inelastic) to 1 (perfectly elastic).
            epsilon_walls(float): Coefficient of Restitution (COR) for collisions between particles and walls,
                0 (perfectly inelastic) to 1 (perfectly elastic).
        """

        self.position = np.array(position, dtype = np.float64)
        self.velocity = np.array(velocity, dtype = np.float64)
        self.radius = radius
        self.color = color
        self.box_width = box_width
        self.box_height = box_height
        self.density = density
        self.epsilon_collision = epsilon_collision
        self.epsilon_walls = epsilon_walls
        self.mass = self.density * (4/3) * np.pi * self.radius ** 3
        self.collision_count = 0

    def move(self, delta_time: float) -> None:
        """
        Updates the position of the particle based on its velocity and the elapsed time.

        Args:
            delta_time (float): The time interval over which to update the position.
        """

        # Update position
        self.position += self.velocity * delta_time

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the particle on the given Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen to draw the particle on.
        """

        pygame.draw.circle(screen, self.color, list(map(int, self.position)), self.radius)

    def time_to_hit(self, other: 'Particle') -> float:
        """
        Calculates the time until this particle collides with another particle.

        Args:
            other (Particle): The other particle to check for collision.

        Returns:
            float: The time until collision, or infinity if no collision will occur.
        """

        if self == other:
            return float('inf')

        # Calculate deltas
        dx = other.position - self.position
        dv = other.velocity - self.velocity

        # If particles are moving away from each other
        if np.dot(dx, dv) >= 0:
            return float('inf')

        sigma = self.radius + other.radius
        discriminant = np.dot(dx, dv) ** 2 - np.dot(dv, dv) * (np.dot(dx, dx) - sigma ** 2)

        # Check if collision is possible
        if discriminant < 0:
            return float('inf')

        # The collision is possible, return the result
        return -(np.dot(dx, dv) + np.sqrt(discriminant)) / np.dot(dv, dv)

    def time_to_hit_vert_wall(self) -> float:
        """
        Calculates the time until this particle collides with a vertical wall.

        Returns:
            float: The time until collision with a vertical wall, or infinity if no collision will occur.
        """

        if self.velocity[0] > 0:
            return (self.box_width - self.radius - self.position[0]) / self.velocity[0]
        elif self.velocity[0] < 0:
            return (self.radius - self.position[0]) / self.velocity[0]
        else:
            return float('inf')

    def time_to_hit_horz_wall(self) -> float:
        """
        Calculates the time until this particle collides with a horizontal wall.

        Returns:
            float: The time until collision with a horizontal wall, or infinity if no collision will occur.
        """

        if self.velocity[1] > 0:
            return (self.box_height - self.radius - self.position[1]) / self.velocity[1]
        elif self.velocity[1] < 0:
            return (self.radius - self.position[1]) / self.velocity[1]
        else:
            return float('inf')

    def bounce_off(self, other: 'Particle') -> None:
        """
        Handles the collision with another particle and updates velocities accordingly.

        Args:
            other (Particle): The other particle to collide with.
        """

        # Calculate deltas
        dx = other.position - self.position
        dv = other.velocity - self.velocity

        # Calculate collision normal
        normal = dx / np.linalg.norm(dx)

        # Calculate impulse (J)
        J = (1 + self.epsilon_collision) * np.dot(dv, normal) * (self.mass * other.mass) / (self.mass + other.mass)

        # Update velocities
        self.velocity += J / self.mass * normal
        other.velocity -= J / other.mass * normal

        # Update collision count
        self.collision_count += 1
        other.collision_count += 1

    def bounce_off_vert_wall(self) -> None:
        """
        Handles the collision with a vertical wall and updates velocity accordingly.
        """

        self.velocity[0] *= -self.epsilon_walls
        self.collision_count += 1

    def bounce_off_horz_wall(self) -> None:
        """
        Handles the collision with a horizontal wall and updates velocity accordingly.
        """

        self.velocity[1] *= -self.epsilon_walls
        self.collision_count += 1


class Event:
    """
    Represents an event in the simulation.

    Conventions:
        Neither particle None: particle-particle collision.
        One particle None: particle-wall collision.

    Attributes:
        time (float): The time at which the event occurs.
        particle_a (Particle): The first particle involved in the event, or None if it's a wall collision.
        particle_b (Particle): The second particle involved in the event, or None if it's a wall collision.
        part_a_collision_count (int): The collision count of particle_a at the time of the event.
        part_b_collision_count (int): The collision count of particle_b at the time of the event.
    """

    def __init__(self, time: float, particle_a: 'Particle', particle_b: 'Particle') -> None:
        """
        Initializes a new event.

        Args:
            time (float): The time at which the event occurs.
            particle_a (Particle): The first particle involved in the event, or None if it's a wall collision.
            particle_b (Particle): The second particle involved in the event, or None if it's a wall collision.

        Methods:
            is_valid(): Checks if the event is still valid.

        Special Methods:
            __eq__(other): Checks if two events occur at the same time.
            __lt__(other): Compares the times of two events.
        """

        self.time = time
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.part_a_collision_count = None
        self.part_b_collision_count = None

    def __eq__(self, other: 'Event') -> bool:
        """
        Checks if two events occur at the same time.

        Args:
            other (Event): The other event to compare with.

        Returns:
            bool: True if the events occur at the same time, False otherwise.
        """

        return np.allclose(self.time, other.time)

    def __lt__(self, other: 'Event') -> bool:
        """
        Compares the times of two events.

        Args:
            other (Event): The other event to compare with.

        Returns:
            bool: True if this event occurs before the other event, False otherwise.
        """

        return self.time < other.time

    def is_valid(self) -> bool:
        """
        Checks if the event is still valid.

        Returns:
            bool: True if the event is valid, False otherwise.
        """

        # If the collision count has changed since the event creation then the event is not valid anymore
        if self.particle_a and self.particle_b:
            # Particle-particle collision
            return self.part_a_collision_count == self.particle_a.collision_count and \
                   self.part_b_collision_count == self.particle_b.collision_count

        elif self.particle_a and not self.particle_b:
            # Particle - vertical wall collision
            return self.part_a_collision_count == self.particle_a.collision_count

        else:
            # Particle - horizontal wall collision
            return self.part_b_collision_count == self.particle_b.collision_count


class CollisionSystem:
    """
    A class to represent the collision system for a set of particles.

    Attributes:
        particles (List[Particle]): The list of particles in the system.
        time (float): The current time in the simulation.
        min_heap (List[Event]): The priority queue (min-heap) of events.

    Methods:
        predict(current_particle): Predicts future events involving the given particle and adds them to the event queue.
        redraw(screen): Redraws all particles on the screen.
        simulate(screen, delta_time): Simulates the system for a given time step.
    """

    def __init__(self, particles: List['Particle']) -> None:
        """
        Initializes a new collision system.

        Args:
            particles (List[Particle]): The list of particles in the system.
        """

        self.particles = particles
        self.time = 0
        self.min_heap = []

    def predict(self, current_particle: 'Particle') -> None:
        """
        Predicts future events involving the given particle and adds them to the event queue.

        Args:
            current_particle (Particle): The particle for which to predict future events.
        """

        if current_particle is None:
            return

        # Check for events with other particles
        for particle in self.particles:
            if particle != current_particle:
                dt = current_particle.time_to_hit(particle)
                if dt < float('inf'):
                    event = Event(self.time + dt, current_particle, particle)
                    event.part_a_collision_count = deepcopy(current_particle.collision_count)
                    event.part_b_collision_count = deepcopy(particle.collision_count)
                    heapq.heappush(self.min_heap, event)
        
        # Check hit vertical wall
        dt = current_particle.time_to_hit_vert_wall()
        if dt < float('inf'):
            event = Event(self.time + dt, current_particle, None)
            event.part_a_collision_count = deepcopy(current_particle.collision_count)
            heapq.heappush(self.min_heap, event)

        # Check hit horizontal wall
        dt = current_particle.time_to_hit_horz_wall()
        if dt < float('inf'):
            event = Event(self.time + dt, None, current_particle)
            event.part_b_collision_count = deepcopy(current_particle.collision_count)
            heapq.heappush(self.min_heap, event)

    def redraw(self, screen: 'pygame.Surface') -> None:
        """
        Redraws all particles on the screen.

        Args:
            screen (pygame.Surface): The Pygame screen to draw the particles on.
        """

        for particle in self.particles:
            particle.draw(screen)

    def simulate(self, screen: 'pygame.Surface', delta_time: float) -> None:
        """
        Simulates the system for a given time step.

        Args:
            screen (pygame.Surface): The Pygame screen to draw the particles on.
            delta_time (float): The time interval over which to simulate the system.
        """

        self.time += delta_time

        # Handle collisions
        while self.min_heap and self.min_heap[0].time <= self.time:
            event = heapq.heappop(self.min_heap)

            if event.is_valid():
                particle_a = event.particle_a
                particle_b = event.particle_b

                if particle_a and particle_b:
                    particle_a.bounce_off(particle_b)
                elif particle_a:
                    particle_a.bounce_off_vert_wall()
                elif particle_b:
                    particle_b.bounce_off_horz_wall()

                self.predict(particle_a)
                self.predict(particle_b)

        # Empty list of events
        if not self.min_heap:
            for particle in self.particles:
                self.predict(particle)

        # Move particles
        for particle in self.particles:
            particle.move(delta_time)

        # Redraw
        self.redraw(screen)


class Simulation:
    """
    A class to represent a particle collision simulation.

    Attributes:
        fill_color (Tuple[int, int, int]): The color used to fill the screen.
        system (CollisionSystem): The collision system managing the particles.

    Methods:
        run(): Runs the simulation until the user quits.
    """

    def __init__(self, particles: List[Particle], box_width: int, box_height: int, fill_color: Tuple[int, int, int]):
        """
        Initializes the Simulation with particles, screen dimensions, and fill color.

        Args:
            particles (List[Particle]): A list of particles in the simulation.
            box_width (int): The width of the simulation box.
            box_height (int): The height of the simulation box.
            fill_color (Tuple[int, int, int]): The color used to fill the screen.
        """

        self.fill_color = fill_color

        # Initialize Pygame modules
        pygame.init()

        # Create a window or screen with the specified width and height.
        self._screen = pygame.display.set_mode((box_width, box_height))

        # Set the title of the window
        pygame.display.set_caption('Collision System')

        # Create a Clock object to help control the frame rate of the game
        self._clock = pygame.time.Clock()

        # Create system
        self.system = CollisionSystem(particles)

    def run(self) -> None:
        """
        Runs the simulation until the user quits.

        This method handles the main loop of the simulation, including event handling,
        updating the display, and controlling the frame rate.
        """

        self.running = True
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self._screen.fill(self.fill_color)
            self.system.simulate(self._screen, 1/120)
            pygame.display.flip()
            self._clock.tick(120)

        pygame.quit()