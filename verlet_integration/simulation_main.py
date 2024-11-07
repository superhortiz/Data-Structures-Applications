from typing import Tuple
import pygame
import numpy as np
from .verlet import *

# Window dimensions
WINDOW_SIZE: Tuple[int, int] = (800, 600)

# Define colors
DARK_GRAY: Tuple[int, int, int] = (50, 50, 50)
BLACK: Tuple[int, int, int] = (0, 0, 0)

# Number of objects
N: int = 150

# Container dimensions
CENTER: Tuple[int, int] = (400, 300)
RADIUS: int = 250


def main() -> None:
    """
    Main function to run the Pygame simulation using Verlet Integration.
    """
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Simulation using Verlet Integration')
    clock = pygame.time.Clock()

    # Create Solver and objects
    solver = Solver()
    solver.set_constraint(CENTER, RADIUS)
    solver.add_object(np.array([400, 100]), 15, np.random.randint(50, 255, 3))

    epoch = 0
    running = True

    while running:
        epoch += 1

        if epoch % 10 == 0 and len(solver.objects) < N:
            solver.add_object(np.array([420, 100]), np.random.randint(8, 26), np.random.randint(50, 255, 3))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the container
        pygame.draw.circle(screen, DARK_GRAY, CENTER, RADIUS)

        # Create an off-screen surface for the glow effect
        glow_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        glow_surface.fill((0, 0, 0, 0))  # Transparent background

        # Update the solver
        solver.update()

        # Draw the objects
        for obj in solver.objects:
            pygame.draw.circle(screen, obj.color, obj.position.astype(int), int(obj.radius))

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()