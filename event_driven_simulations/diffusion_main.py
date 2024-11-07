import numpy as np
from .simulation import *


def main() -> None:
    """
    Main function to set up and run the particle collision simulation.

    This function initializes the simulation box dimensions, colors, and particles,
    then runs the event-driven simulation to model the diffusion phenomenon from thermodynamics.

    The simulation is event-driven, handling user inputs and updating the display
    accordingly. It simulates the diffusion process, where particles spread out
    from an area of higher concentration to an area of lower concentration over time.
    """

    # Box dimensions
    BOX_WIDTH: int = 600
    BOX_HEIGHT: int = 600

    # Colors
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    PURPLE: Tuple[int, int, int] = (131, 72, 150)
    DARK_PURPLE: Tuple[int, int, int] = (60, 9, 41)
    DARK_GRAY: Tuple[int, int, int] = (50, 50, 50)

    particles: List[Particle] = []
    radius_block = 15
    radius_particles = 4

    for _ in range(200):
        position = np.array([np.random.randint(0, BOX_WIDTH // 2 - radius_block), np.random.randint(0, BOX_HEIGHT)])
        velocity = np.random.randint(-150, 150, 2)
        particles.append(Particle(position, velocity, radius_particles, np.random.randint(0, 255, 3), BOX_WIDTH, BOX_HEIGHT, 0.001))

    for i in range(BOX_HEIGHT // (2 * radius_block - 1)):
        if i not in [9, 10]:
            particles.append(Particle(np.array([BOX_WIDTH // 2, i * radius_block * 2 + radius_block]), np.array([0, 0]),
                                                radius_block, BLACK, BOX_WIDTH, BOX_HEIGHT, 2e10))

    simulation = Simulation(particles, BOX_WIDTH, BOX_HEIGHT, DARK_GRAY)
    simulation.run()


if __name__ == "__main__":
    main()