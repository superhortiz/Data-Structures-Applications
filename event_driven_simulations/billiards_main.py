import numpy as np
from .simulation import *


def main() -> None:
    """
    Main function to set up and run the simplified billiards simulation.

    This function initializes the simulation box dimensions, colors, and particles,
    then runs the event-driven simulation to model a simplified billiards game.

    The simulation is event-driven, handling user inputs and updating the display
    accordingly. It simulates the motion and collisions of billiard balls on a table.
    The collisions between balls are inelastic, using a Coefficient of Restitution (COR) = 0.75.
    """

    # Box dimensions
    BOX_WIDTH: int = 350
    BOX_HEIGHT: int = 600

    # Colors
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    PURPLE: Tuple[int, int, int] = (131, 72, 150)
    DARK_PURPLE: Tuple[int, int, int] = (60, 9, 41)
    DARK_GRAY: Tuple[int, int, int] = (50, 50, 50)

    particles: List[Particle] = []
    radius = 15

    # Coefficient of Restitution (COR)
    epsilon = 0.75

    for i in range(5):
        for j in range(i):
            position = np.array([BOX_WIDTH // 2 + j * 2 * radius - i * radius, 200 - i * 2 * radius * 0.8661])
            velocity = np.zeros((2,))
            particles.append(Particle(position, velocity, radius,
                np.random.randint(50, 255, 3), BOX_WIDTH, BOX_HEIGHT, 1, epsilon))

    particles.append(Particle(np.array([175, 500]), np.array([np.random.randint(-25, 25), -300]),
        radius, WHITE, BOX_WIDTH, BOX_HEIGHT, 1, epsilon))

    simulation = Simulation(particles, BOX_WIDTH, BOX_HEIGHT, DARK_GRAY)
    simulation.run()


if __name__ == "__main__":
    main()