import pygame
import sys
import colors
import numpy as np
import time
import random

from pygame import K_DOWN, K_LEFT, K_UP, K_RIGHT, K_KP_ENTER

from board import Board, PIECES

pygame.init()

size = width, height = 640, 480


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
    font = pygame.font.Font(pygame.font.get_default_font(), 12)
    surface = font.render(text, False, colors.WHITE)
    screen.blit(surface, dest=center)


def print_stats(screen, level, score, lines_cleared):
    print_line(screen, "Level: %d" % level, (400, 10))
    print_line(screen, "Score: %d" % score, (400, 25))
    print_line(screen, "Lines: %d" % lines_cleared, (400, 40))


def main():
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
    piece_coords = np.array([board.cols // 2, 0])

    while not board.game_over():
        screen.fill(colors.BLACK)
        piece_set = False
        # tps = clock.tick(60)
        inputs = np.array([0, 0, 0, 0])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                inputs = get_inputs_user(event)
            if event.type == pygame.QUIT:
                sys.exit()

        piece, piece_coords = \
            board.apply_command(piece_idx, piece, piece_coords, inputs)
        if time.time() - last_tick_time > TIME_BETWEEN_TICKS:
            piece, piece_coords, piece_set = \
                board.move_down(piece, piece_coords, piece_idx)
            last_tick_time = time.time()
        else:
            pass
        board.render(screen)
        board.render_piece(screen, piece, piece_coords, piece_idx)

        if piece_set:  # collided with bottom or another piece on tick
            piece_idx, piece = get_rand_piece()
            piece_coords = np.array([0, 0])
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

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.key.get_pressed()[K_KP_ENTER]:
                sys.exit()


if __name__ == "__main__":
    main()
