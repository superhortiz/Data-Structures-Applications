import numpy as np
import pygame
from typing import List
from PIL import Image, ImageFilter
from .n_body_simulation import *


# Define colors
DARK_GRAY = (50, 50, 50)

# Window dimensions
WIDTH, HEIGHT = 1300, 650

# Variables for simulation
mass = 1000
distance = 300
velocity = np.sqrt(G * mass / distance)  # Orbital velocity


class Simulation:
    """
    Manages the N-body simulation and visualization using Pygame.

    Attributes:
        bodies (List[Body]): List of Body instances in the simulation.
        screen (pygame.Surface): The Pygame display surface.
        simulation (NBodySimulation): The N-body simulation instance.
    """

    def __init__(self, bodies: List['Body']) -> None:
        """
        Initializes the Simulation instance.

        Args:
            bodies (List[Body]): List of Body instances to be simulated.
        """

        self.bodies = bodies
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.simulation = NBodySimulation(self.bodies)
        pygame.display.set_caption("N-Body Simulation")

    def run(self) -> None:
        """
        Runs the main loop of the simulation, handling events and updating the display.
        """
        # Parameters to rebuild the KDTree
        rebuild_frequency = 30
        time_step = 0
        theta = 1000

        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            time_step += 1
            self.screen.fill(DARK_GRAY)

            # Create an off-screen surface for the glow effect
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            glow_surface.fill((0, 0, 0, 0))  # Transparent background

            rebuild = time_step % time_step == 0
            self.simulation.update(1/60, theta, rebuild)

            for body in self.bodies:
                # Draw the glow circle on the glow surface
                pygame.draw.circle(glow_surface, (255, 255, 255, 128), (int(body.position[0]), int(body.position[1])),
                    body.diameter * 1.25)

                if body.position[0] > WIDTH or (np.linalg.norm(body.position - [WIDTH//2,HEIGHT//2]) < 10 and body.diameter == 4) \
                    or body.position[1] > HEIGHT or body.position[1] < 0:
                    body.position[0] = 0
                    body.position[1] = np.random.randint(100, HEIGHT-100)
                    body.velocity[0] = velocity
                    body.velocity[1] = 0

            # Apply Gaussian blur to the glow surface
            glow_surface_resized = pygame.transform.smoothscale(glow_surface, (WIDTH // 2, HEIGHT // 2))
            img_str = pygame.image.tostring(glow_surface_resized, "RGBA", False)
            im1 = Image.frombytes('RGBA', (WIDTH // 2, HEIGHT // 2), img_str)
            im1 = im1.filter(ImageFilter.GaussianBlur(body.diameter // 2))
            im1 = im1.tobytes()
            glow_surface_blurred = pygame.image.fromstring(im1, (WIDTH // 2, HEIGHT // 2), "RGBA")
            glow_surface_blurred = pygame.transform.smoothscale(glow_surface_blurred, (WIDTH, HEIGHT))

            # Blit the blurred glow surface onto the main screen
            self.screen.blit(glow_surface_blurred, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # Draw each body
            for body in self.bodies:
                # Draw the bodies
                pygame.draw.circle(self.screen, body.color, (int(body.position[0]), int(body.position[1])), body.diameter)

            # Update the self.screen
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()


def main() -> None:
    """
    The main function to initialize and run the N-body simulation.
    """
    bodies = []

    for i in range(30):
        bodies.append(Body([-150 * i, np.random.randint(0, HEIGHT)],
            [10000*velocity,0], mass/100000, np.random.randint(50,255,3), 4))

    bodies.append(Body([WIDTH//2,HEIGHT//2], [0,0], mass/10, np.random.randint(50,100,3), 20, False))
    simulation = Simulation(bodies)
    simulation.run()


if __name__ == "__main__":
    main()