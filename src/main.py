import pygame
import sys
import colors
import numpy as np
import time
import threading
import random
import loguru

from pygame import K_DOWN, K_LEFT, K_UP, K_RIGHT, K_KP_ENTER

from board import Board, PIECES
from data_model import DataStore, Instance

# Only initialize display and font engines
pygame.display.init()
pygame.font.init()

data_store = DataStore("joe")
logger = loguru.logger

size = width, height = 640, 480


def run_data_store():
    logger.info("Started data runner")
    data_store.run()


def get_inputs_user(event: pygame.event) -> np.array:
    key = pygame.key.get_pressed()
    return np.array([key[K_UP], key[K_DOWN], key[K_LEFT], key[K_RIGHT]])


def get_rand_piece():
    piece_idx = random.randint(1, len(PIECES))
    curr_piece = PIECES[piece_idx - 1][1]
    return piece_idx, curr_piece


def calc_score(level, rows):
    pts = {1: 40, 2: 100, 3: 300, 4: 1200}
    return pts.get(rows, 0) * (level + 1)


def calc_speed(level):
    return max(1, 48 - (level * 5))


def print_line(screen, text, center):
    font = pygame.font.FontType('freesansbold.ttf', 12)
    surface = font.render(text, True, colors.WHITE)
    screen.blit(surface, dest=center)


def print_stats(screen, level, score, lines_cleared):
    print_line(screen, "Level: %d" % level, (225, 160))
    print_line(screen, "Score: %d" % score, (225, 175))
    print_line(screen, "Lines: %d" % lines_cleared, (225, 190))


def show_next_up(screen, board, piece, piece_idx):
    print_line(screen, "Next piece:", (225, 10))
    board.render_piece(screen, piece, (12, 2), piece_idx)


def main():
    data_store_thread = threading.Thread(target=run_data_store)
    data_store_thread.start()
    score = 0
    level = 0
    lines_cleared = 0

    random.seed(time.time())
    screen = pygame.display.set_mode(size)

    # clock = pygame.time.Clock()

    TIME_BETWEEN_TICKS = 0.25
    last_tick_time = time.time()
    screen.fill(colors.BLACK)
    board = Board()
    board.render(screen)
    pygame.display.update()

    piece_idx, piece = get_rand_piece()
    npiece_idx, npiece = get_rand_piece()
    piece_coords = np.array([(board.cols // 2)-1, 0])
    curr_input = Instance(board.get_board(),  np.array([0, 0, 0, 0]),
                          np.array([0, 0, 0, 0]),  npiece_idx)

    while not board.game_over():
        screen.fill(colors.BLACK)
        piece_set = False
        show_next_up(screen, board, npiece, npiece_idx)

        # tps = clock.tick(60)
        inputs = np.array([0, 0, 0, 0])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                inputs = get_inputs_user(event)
                curr_input = Instance(
                    board.get_board(),
                    curr_input.current_move,
                    inputs,
                    npiece_idx
                )
                data_store.write(str(curr_input))
            if event.type == pygame.QUIT:
                data_store.stop()
                data_store_thread.join()
                sys.exit()

        piece, piece_coords = \
            board.apply_command(piece_idx, piece, piece_coords, inputs)
        if time.time() - last_tick_time > TIME_BETWEEN_TICKS:
            piece, piece_coords, piece_set = \
                board.move_down(piece, piece_coords, piece_idx)
            last_tick_time = time.time()
            curr_input = Instance(
                board.get_board(),
                curr_input.current_move,
                inputs,
                npiece_idx
            )
            data_store.write(str(curr_input))
        else:
            pass
        board.render(screen)
        board.render_piece(screen, piece, piece_coords, piece_idx)

        if piece_set:  # collided with bottom or another piece on tick
            curr_input = Instance(
                board.get_board(),
                curr_input.current_move,
                inputs,
                npiece_idx
            )
            data_store.write(str(curr_input))
            piece_idx, piece = npiece_idx, npiece
            npiece_idx, npiece = get_rand_piece()
            piece_coords = np.array([(board.cols // 2)-1, 0])
            removed_rows = board.check_rows()
            lines_cleared += removed_rows
            score += calc_score(level, removed_rows)
            level = lines_cleared // 10

        print_stats(screen, level, score, lines_cleared)
        pygame.display.update()

    font = pygame.font.FontType('freesansbold.ttf', 20)
    text = "Game Over - Press Enter"
    surface = font.render(text, True, colors.WHITE)
    rectangle = surface.get_rect()
    rectangle.center = (width // 2, height // 2)
    screen.blit(surface, rectangle)

    pygame.display.update()

    data_store.stop()
    data_store_thread.join()

    logger.info("Data saved...")

    pygame.event.clear()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               pygame.key.get_pressed()[K_KP_ENTER] or \
               event.key == 13:
                sys.exit()


if __name__ == "__main__":
    main()
