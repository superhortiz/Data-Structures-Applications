import pygame
import numpy as np
from PIL import Image, ImageFilter
from scipy.spatial import KDTree
from typing import List, Tuple
from .boid import *


# Window dimensions
WIDTH, HEIGHT = 1300, 650

# Define colors
DARK_GRAY = (50, 50, 50)


class Simulation:
    """
    A class to represent the flocking simulation.

    Attributes:
        number_of_boids (int): Number of boids in the simulation.
        number_of_neighbors (int): Number of neighbors to consider for each boid.
        size_boids (int): Size of each boid.
        screen (pygame.Surface): The Pygame screen where the simulation is drawn.
        boids (List[Boid]): List of boid instances in the simulation.
    """

    def __init__(self, number_of_boids: int, number_of_neighbors: int, size_boids: int) -> None:
        """
        Initializes the simulation with the given parameters.

        Args:
            number_of_boids (int): Number of boids in the simulation.
            number_of_neighbors (int): Number of neighbors to consider for each boid.
            size_boids (int): Size of each boid.
        """

        self.number_of_boids = number_of_boids
        self.number_of_neighbors = number_of_neighbors
        self.size_boids = size_boids

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flocking Boids")

        # Create boids using random colors
        self.boids = [Boid(np.random.randint(50, 255, 3), WIDTH, HEIGHT) for _ in range(number_of_boids)]

    def run(self) -> None:
        """
        Runs the main loop of the simulation.
        """
        # Build KDTree
        boid_positions = np.array([boid.position for boid in self.boids])
        kdtree = KDTree(boid_positions)

        # Parameters to rebuild the KDTree
        rebuild_frequency = 30
        time_step = 0

        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            time_step += 1

            if time_step % rebuild_frequency == 0:
                # Build a new KDTree
                boid_positions = np.array([boid.position for boid in self.boids])
                kdtree = KDTree(boid_positions)

            self.screen.fill(DARK_GRAY)

            # Create an off-screen surface for the glow effect
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            glow_surface.fill((0, 0, 0, 0))  # Transparent background

            for boid in self.boids:
                nearby_boids = kdtree.query(boid.position, k=self.number_of_neighbors)
                neighbors = [self.boids[i] for i in nearby_boids[1]]

                # Perform cohesion, separation, alignment with neighbors
                boid.update(neighbors)

                # Draw the glow circle on the glow surface
                pygame.draw.circle(glow_surface, (*boid.color, 128), (int(boid.position[0] + self.size_boids // 2),
                    int(boid.position[1])), self.size_boids // 2)

            # Apply Gaussian blur to the glow surface
            glow_surface_resized = pygame.transform.smoothscale(glow_surface, (WIDTH // 2, HEIGHT // 2))
            img_str = pygame.image.tostring(glow_surface_resized, "RGBA", False)
            im1 = Image.frombytes('RGBA', (WIDTH // 2, HEIGHT // 2), img_str)
            im1 = im1.filter(ImageFilter.GaussianBlur(self.size_boids // 2))
            im1 = im1.tobytes()
            glow_surface_blurred = pygame.image.fromstring(im1, (WIDTH // 2, HEIGHT // 2), "RGBA")
            glow_surface_blurred = pygame.transform.smoothscale(glow_surface_blurred, (WIDTH, HEIGHT))

            # Blit the blurred glow surface onto the main screen
            self.screen.blit(glow_surface_blurred, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # Draw each boid
            for boid in self.boids:
                draw_fish(self.screen, int(boid.position[0]), int(boid.position[1]), self.size_boids, boid.color, boid.velocity)

            # Update the screen
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()


def main() -> None:
    """
    Main function to run the simulation.
    """
    number_of_boids = 200
    number_of_neighbors = 5
    size_boids = 10
    simulation = Simulation(number_of_boids, number_of_neighbors, size_boids)
    simulation.run()


if __name__ == "__main__":
    main()