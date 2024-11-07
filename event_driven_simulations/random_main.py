import numpy as np
from .simulation import *


def main() -> None:
    """
    Main function to set up and run the particle collision simulation.

    This function initializes the simulation box dimensions, colors, and particles,
    then runs the event-driven and Brownian motion simulation.

    The simulation is event-driven, handling user inputs and updating the display
    accordingly. It also simulates Brownian motion, where particles move in random
    directions with random velocities.
    """

    # Box dimensions
    BOX_WIDTH: int = 600
    BOX_HEIGHT: int = 600

    # Colors
    PURPLE: Tuple[int, int, int] = (131, 72, 150)
    DARK_PURPLE: Tuple[int, int, int] = (245, 98, 194)
    DARK_GRAY: Tuple[int, int, int] = (50, 50, 50)

    particles: List[Particle] = []

    for _ in range(50):
        position = np.random.randint(0, BOX_HEIGHT, 2)
        velocity = np.random.randint(-150, 150, 2)
        color = np.random.randint(50, 255, 3)
        radius = 15
        particles.append(Particle(position, velocity, radius, color, BOX_WIDTH, BOX_HEIGHT))

    simulation = Simulation(particles, BOX_WIDTH, BOX_HEIGHT, DARK_GRAY)
    simulation.run()


if __name__ == "__main__":
    main()