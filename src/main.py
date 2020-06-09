import pygame
import sys
import colors
import numpy as np
import time
import threading
import random
import loguru

from pygame import K_DOWN, K_LEFT, K_UP, K_RIGHT, K_KP_ENTER

from piece import Piece
from board import Board, PIECE_FACTORIES
from data_model import DataStore, Instance

# Only initialize display and font engines
pygame.display.init()
pygame.font.init()

data_store = DataStore("joe")
logger = loguru.logger

size = width, height = 350, 400


def run_data_store() -> None:
    logger.info("Started data runner")
    data_store.run()


def get_inputs_user(event: pygame.event) -> np.array:
    key = pygame.key.get_pressed()
    return np.array([key[K_UP], key[K_DOWN], key[K_LEFT], key[K_RIGHT]])


def get_rand_piece() -> 'Piece':
    piece_idx = random.randint(1, len(PIECE_FACTORIES))
    curr_piece = PIECE_FACTORIES[piece_idx - 1].create_piece()
    return curr_piece


def calc_score(level: int, rows: int) -> int:
    pts = {1: 40, 2: 100, 3: 300, 4: 1200}
    return pts.get(rows, 0) * (level + 1)


def calc_speed(level: int) -> int:
    return max(1, 48 - (level * 5))


def print_line(screen: pygame.display, text: str, center: (int, int)) -> None:
    font = pygame.font.FontType('freesansbold.ttf', 20)
    surface = font.render(text, True, colors.WHITE)
    screen.blit(surface, dest=center)


def print_stats(
    screen: pygame.display,
    level: int,
    score: int,
    lines_cleared: int,
) -> None:
    print_line(screen, "Level: %d" % level, (235, 160))
    print_line(screen, "Score: %d" % score, (235, 180))
    print_line(screen, "Lines: %d" % lines_cleared, (235, 200))


def show_next_up(
    screen: pygame.display,
    board: 'Board',
    piece: 'Piece'
) -> None:
    print_line(screen, "Next piece:", (225, 10))
    cp = piece.copy()
    cp.pos = np.array([12, 2])
    board.render_piece(screen, cp)


def show_message(
    screen: pygame.display,
    msg: str
) -> None:
    screen.fill(colors.BLACK)
    font = pygame.font.FontType('freesansbold.ttf', 20)
    surface = font.render(msg, True, colors.WHITE)
    rectangle = surface.get_rect()
    rectangle.center = (width // 2, height // 2)
    screen.blit(surface, rectangle)
    pygame.display.update()


def play() -> None:
    # Initialize data collection
    data_store_thread = threading.Thread(target=run_data_store)
    data_store_thread.start()

    # Initialize game data
    score = 0
    level = 0
    lines_cleared = 0
    random.seed(time.time())

    screen = pygame.display.set_mode(size)

    TIME_BETWEEN_TICKS = 0.5
    last_tick_time = time.time()
    screen.fill(colors.BLACK)

    # Initial render
    board = Board()
    board.render(screen)
    pygame.display.update()

    # Initial pieces
    piece = get_rand_piece()
    npiece = get_rand_piece()
    curr_input = Instance(board.get_board(),  np.array([0, 0, 0, 0]),
                          np.array([0, 0, 0, 0]),  npiece.ID)

    # Game loop
    while not board.game_over():
        # Clear screen and inputs
        screen.fill(colors.BLACK)
        inputs = np.array([0, 0, 0, 0])

        show_next_up(screen, board, npiece)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # User provided input
                inputs = get_inputs_user(event)
                curr_input = Instance(
                    board.get_board(),
                    curr_input.current_move,
                    inputs,
                    npiece.ID
                )
                data_store.write(str(curr_input))
            if event.type == pygame.QUIT:  # Peacefully exit
                data_store.stop(write=False)
                data_store_thread.join()
                sys.exit()

        piece = board.apply_command(piece, inputs)  # Get updated piece

        # Simple game tick control, runs for each game tick
        if time.time() - last_tick_time > TIME_BETWEEN_TICKS:
            piece = board.move_down(piece)
            last_tick_time = time.time()
            curr_input = Instance(
                board.get_board(),
                curr_input.current_move,
                inputs,
                npiece.ID
            )
            data_store.write(str(curr_input))

        # Redraw board and moving piece
        board.render(screen)
        board.render_piece(screen, piece)

        if piece.isSet:  # collided with bottom or another piece on tick
            curr_input = Instance(
                board.get_board(),
                curr_input.current_move,
                inputs,
                npiece.ID
            )
            data_store.write(str(curr_input))

            # Bring in next piece, get next piece
            piece = npiece.copy()
            npiece = get_rand_piece()

            # Update stats
            removed_rows = board.check_rows()
            lines_cleared += removed_rows
            score += calc_score(level, removed_rows)
            level = lines_cleared // 10

        # Update screen
        print_stats(screen, level, score, lines_cleared)
        pygame.display.update()

    # Game over messages and clean up
    show_message(screen, "Game Over - Score: {} | saving...".format(score))
    data_store.stop()
    data_store_thread.join()
    show_message(screen, "ENTER to replay | q to quit")

    logger.info("Game over, data saved.")

    pygame.event.clear()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    pygame.key.get_pressed()[K_KP_ENTER]:
                return

            if hasattr(event, "key"):
                if event.key == 13:
                    return
                if event.key == 113:
                    sys.exit()


def main() -> None:
    while True:
        play()


if __name__ == "__main__":
    main()
