import numpy as np
import pygame
import random
import time
from .board import Board
from .solver import Solver
from typing import Callable, Optional


# Window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
PUZZLE_WIDTH = 300
PUZZLE_HEIGHT = 300

# Offsets
BOARD_OFFSET_VERT = 125
BOARD_OFFSET_HORZ = 50
LINE_OFFSET = 2
TEXT_OFFSET = 2

# Puzzle dimensions
PUZZLE_SIZE = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
CHARCOAL_GRAY = (54, 69, 79)
HOVER_COLOR = (192, 192, 192)
PRESSED_COLOR = (128, 128, 128)


class Puzzle:
    """
    A class to represent an 8-puzzle game.

    The Puzzle class handles the initialization, drawing, and movement of tiles in an 8-puzzle game.
    It can generate a random solvable initial state or accept a predefined state. The class also
    includes methods to draw the puzzle on a Pygame screen and to move the blank tile.

    Attributes:
        tiles (Board): The current state of the puzzle represented as a Board object.
        solver (Solver): An instance of the Solver class.
        step_index (int): An index to track the steps in the solution.
        zero_index (tuple): The current position of the blank tile in the puzzle.
    """

    def __init__(self, tiles: Optional[np.ndarray] = None) -> None:
        """
        Initialize the Puzzle with a given tile configuration or generate a random solvable state.

        Args:
            tiles (Optional[np.ndarray]): A 2D numpy array representing the initial state of the puzzle.
        """

        # If a initial state is not specified it gets a new random solvable state
        if tiles is None:
            self.tiles = Board(self.generate_initial())

        # Here it initializes with a given initial state
        else:
            self.tiles = Board(tiles)
            
        self.solver = Solver(self.tiles)
        self.step_index = 0
        
        while not self.solver.is_solvable():
            self.tiles = Board(self.generate_initial())
            self.solver = Solver(self.tiles)

        # Auxiliar index to show the solution
        self.zero_index = self.tiles.find_indices_blank()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the current state of the puzzle on the given screen.

        Args:
            screen (pygame.Surface): The surface to draw the puzzle on.
        """

        # Width of each tile
        tile_width = PUZZLE_WIDTH // PUZZLE_SIZE

        # Height of each tile
        tile_height = PUZZLE_HEIGHT // PUZZLE_SIZE

        # Iterates over each tile in the puzzle
        for i in range(PUZZLE_SIZE):
            # Get x-coordinate
            x = BOARD_OFFSET_HORZ + i * tile_width

            for j in range(PUZZLE_SIZE):
                # Get y-coordinate
                y = BOARD_OFFSET_VERT + j * tile_height

                # Draw all tiles except the one with 0
                # The coordinate system starts from the top-left corner of the screen
                if self.tiles.board[j][i] != 0:
                    # Draw a outer rectangle
                    pygame.draw.rect(screen, DARK_GRAY, (x, y, tile_width, tile_height))
                    
                    # Draw a inner rectangle
                    pygame.draw.rect(screen, LIGHT_GRAY, (x + LINE_OFFSET, y + LINE_OFFSET,
                            tile_width - 2 * LINE_OFFSET, tile_height - 2 * LINE_OFFSET))

                    # Create a font object
                    font = pygame.font.SysFont("bahnschrift", 40)

                    # Render the text to a new Surface
                    text = font.render(str(self.tiles.board[j][i]), True, BLACK)

                    # Create a rectangle (Rect) that encloses the text surface
                    text_rect = text.get_rect(center = (x + tile_width // 2, y + tile_height // 2))

                    # Draw the text surface onto the main screen surface at the position specified by text_rect
                    screen.blit(text, text_rect)

                else:
                    # Draw an empty rectangle for 0
                    pygame.draw.rect(screen, DARK_GRAY, (x, y, tile_width, tile_height))

    def move_tile(self, direction: str) -> None:
        """
        Move the blank tile in the specified direction.

        Args:
            direction (str): The direction to move the blank tile ("up", "down", "left", "right").
        """

        # Get indices of black tile
        i, j = self.zero_index

        if direction == "up" and i > 0:
            self.tiles.board[i][j], self.tiles.board[i - 1][j] = self.tiles.board[i - 1][j], self.tiles.board[i][j]
            self.zero_index = self.tiles.find_indices_blank()
        elif direction == "down" and i < PUZZLE_SIZE - 1:
            self.tiles.board[i][j], self.tiles.board[i + 1][j] = self.tiles.board[i + 1][j], self.tiles.board[i][j]
            self.zero_index = self.tiles.find_indices_blank()
        elif direction == "left" and j > 0:
            self.tiles.board[i][j], self.tiles.board[i][j - 1] = self.tiles.board[i][j - 1], self.tiles.board[i][j]
            self.zero_index = self.tiles.find_indices_blank()
        elif direction == "right" and j < PUZZLE_SIZE - 1:
            self.tiles.board[i][j], self.tiles.board[i][j + 1] = self.tiles.board[i][j + 1], self.tiles.board[i][j]
            self.zero_index = self.tiles.find_indices_blank()

    def generate_initial(self) -> np.ndarray:
        """
        Generate a new random initial state for the puzzle.

        Returns:
            np.ndarray: A 2D numpy array representing the initial state of the puzzle.
        """
        tiles = np.arange(9)
        np.random.shuffle(tiles)
        return np.reshape(tiles, (3, 3))


class Button:
    """
    A class to represent a clickable button in a Pygame application.

    Attributes:
        rect (pygame.Rect): The rectangle defining the button's position and size.
        text (str): The text displayed on the button.
        color (tuple): The color of the button in its normal state.
        hover_color (tuple): The color of the button when the mouse hovers over it.
        pressed_color (tuple): The color of the button when it is pressed.
        action (Optional[Callable]): The function to call when the button is clicked.
        font (pygame.font.Font): The font used to render the button's text.
        is_pressed (bool): A flag indicating whether the button is currently pressed.
    """

    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple,
                hover_color: tuple, pressed_color: tuple, action: Optional[Callable] = None):
        """
        Initialize the Button with the specified attributes.

        Args:
            x (int): The x-coordinate of the button's top-left corner.
            y (int): The y-coordinate of the button's top-left corner.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text displayed on the button.
            color (tuple): The color of the button in its normal state.
            hover_color (tuple): The color of the button when the mouse hovers over it.
            pressed_color (tuple): The color of the button when it is pressed.
            action (Optional[Callable]): The function to call when the button is clicked.
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.action = action
        self.font = pygame.font.SysFont("arial", 22)
        self.is_pressed = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button on the given screen.

        Args:
            screen (pygame.Surface): The surface to draw the button on.
        """
        text_offset = 0

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # If the mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                # Draw the button with the pressed_color
                pygame.draw.rect(screen, self.pressed_color, self.rect)
                text_offset = TEXT_OFFSET
            else:
                # Draw the button with the hover_color
                pygame.draw.rect(screen, self.hover_color, self.rect)

        # Mouse not over the button
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Render text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center = (self.rect.centerx, self.rect.centery + text_offset))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle a Pygame event to update the button's state and execute its action if clicked.

        Args:
            event (pygame.event.Event): The event to handle.
        """

        # Check for mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True

        # Check for mouse button up event
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.is_pressed:
                if self.action:
                    self.action()
            self.is_pressed = False


class Game():
    """
    A class to represent the 8-Puzzle game.

    This class handles the initialization of the game, including setting up the game window,
    creating text and button instances, and managing the main game loop. It also processes
    user inputs and updates the game state accordingly.
    """

    def __init__(self) -> None:
        """
        Initialize the Game class.

        This method initializes Pygame modules, creates the game window, sets the window title,
        creates a clock object to control the frame rate, initializes the puzzle, and sets up
        text and button instances.
        """

        # Initialize Pygame modules
        pygame.init()

        # Create a window or screen with the specified width and height.
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Set the title of the window
        pygame.display.set_caption('8-Puzzle')

        # Create a Clock object to help control the frame rate of the game
        self._clock = pygame.time.Clock()

        # Create an instance of Puzzle
        self._puzzle = Puzzle()

        # Create instances for texts
        font = pygame.font.SysFont("Arial", 40)
        self._title_text = font.render("8-Puzzle", True, WHITE)
        self._title_rect = self._title_text.get_rect(center = (WINDOW_WIDTH // 2, 50))
        font_solved = pygame.font.SysFont("Arial", 22)
        self._title_text_solved = font_solved.render("Solved!", True, WHITE)
        self._title_rect_solved = self._title_text_solved.get_rect(center = (475, 375))

        # Create reset button
        x_coord, y_coord = 400, 250
        width_button, height_button = 150, 50
        self._button_reset = Button(x_coord, y_coord, width_button, height_button, "Start again",
            DARK_GRAY, HOVER_COLOR, PRESSED_COLOR, self._reset_button)

        # Create Solve button
        x_coord, y_coord = 400, 150
        self._button_solve = Button(x_coord, y_coord, width_button, height_button, "Solve it",
            DARK_GRAY, HOVER_COLOR, PRESSED_COLOR, self._solve_button)

        # Variables to show the solution path
        self._solve_delay = 0.5  # seconds
        self._last_solve_time = time.time()

    def run(self) -> None:
        """
        Start the main game loop.

        This method handles the main game loop, including event handling, drawing the puzzle,
        and showing the solution path when the Solve button is pressed.
        """

        # Flag to know when it is showing the solution path
        self.solving = False

        # Start the main game loop
        self.running = True

        while self.running:
            # Handle the events
            self._handle_events()

            # This is executed only when Solve button was pressed
            self._show_solution()

            # Draw the screen
            self._draw_puzzle()

        # Close pygame
        pygame.quit()

    def _handle_events(self) -> None:
        """
        Handle Pygame events.

        This method processes all events in the event queue, including quitting the game,
        handling key presses for puzzle movement, and handling button clicks for reset and solve actions.
        """

        # Loops through all events in the event queue
        for event in pygame.event.get():
            # To exit the loop
            if event.type == pygame.QUIT:
                self.running = False

            # Check if a key has been pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._puzzle.move_tile("up")
                elif event.key == pygame.K_DOWN:
                    self._puzzle.move_tile("down")
                elif event.key == pygame.K_LEFT:
                    self._puzzle.move_tile("left")
                elif event.key == pygame.K_RIGHT:
                    self._puzzle.move_tile("right")

            # Check for Reset button click
            self._button_reset.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._button_reset.rect.collidepoint(event.pos) and self._button_reset.is_pressed:
                    self._reset_button()
                    button_reset.is_pressed = False

            # Check for Solve button click
            self._button_solve.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._button_solve.rect.collidepoint(event.pos) and self._button_solve.is_pressed:
                    self._solve_button()
                    button_solve.is_pressed = False        

    def _draw_puzzle(self) -> None:
        """
        Draw the current state of the puzzle on the screen.

        This method fills the screen with a background color, draws the puzzle, buttons, and
        title text, and updates the display. If the puzzle is solved, it also displays a "Solved!" message.
        """

        # Fills the screen with CHARCOAL_GRAY to clear the previous frame
        self._screen.fill(CHARCOAL_GRAY)

        # Draw the current state of the puzzle
        self._puzzle.draw(self._screen)
        self._button_reset.draw(self._screen)
        self._button_solve.draw(self._screen)
        self._screen.blit(self._title_text, self._title_rect)

        # If the current state is solution show a message
        if self._puzzle.tiles.is_goal():
            self._screen.blit(self._title_text_solved, self._title_rect_solved)

        # Update the display to show the new frame
        pygame.display.flip()

        # Limits the frame rate to 60 frames per second to ensure smooth gameplay
        self._clock.tick(60)

    def _reset_button(self) -> None:
        """
        Reset the puzzle to a new instance.

        This method generates a new instance of the Puzzle class, effectively resetting the game.
        """

        # Generate a new instance of Puzzle
        self._puzzle = Puzzle()

    def _solve_button(self) -> None:
        """
        Solve the puzzle using the current board state.

        This method generates a new instance of the Puzzle class with the current board state
        and sets the solving flag to True.
        """

        # Generate a new instance of Puzzle, with the current board state
        self._puzzle = Puzzle(self._puzzle.tiles.board)

        # Change solving flag
        self.solving = True

    def _show_solution(self) -> None:
        """
        Show the solution steps for the puzzle.

        This method checks if the solve button was pressed and, if so, draws the solution steps
        at a specified delay.
        """

        # Solve button was pressed
        if self.solving:
            current_time = time.time()
            if current_time - self._last_solve_time >= self._solve_delay:
                self._draw_solution_steps()
                self._last_solve_time = current_time

    def _draw_solution_steps(self) -> None:
        """
        Draw the solution steps on the screen.

        This method iterates through the solution steps and updates the puzzle board with each step.
        If all steps are completed, it updates the puzzle to the final solved state.
        """

        # Go through the solution list
        if self._puzzle.step_index < self._puzzle.solver.moves():
            # Get the next movement
            next_step = self._puzzle.solver.solution()[self._puzzle.step_index]

            # Update the board with the next movement
            self._puzzle.tiles.board = next_step.board
            self._puzzle.step_index += 1
            
            # Redraw the screen
            self._draw_puzzle()

        else:
            # Change solving flag
            self.solving = False

            # Update the current state
            self._puzzle = Puzzle(self._puzzle.solver.solution()[-1].board)


if __name__ == "__main__":
    game = Game()
    game.run()