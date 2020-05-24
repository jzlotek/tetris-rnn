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


def main():
    random.seed(time.time())
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    screen.fill(colors.BLACK)
    TIME_BETWEEN_TICKS = 0.25
    last_tick_time = time.time()
    board = Board()
    board.render(screen)
    pygame.display.update()

    piece_idx, piece = get_rand_piece()
    piece_coords = np.array([0, 0])
    while not board.game_over():
        piece_set = False
        tps = clock.tick(60)
        inputs = np.array([0,0,0,0])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                inputs = get_inputs_user(event)
            if event.type == pygame.QUIT:
                sys.exit()

        piece, piece_coords = board.apply_command(piece, piece_coords, inputs)
        if time.time() - last_tick_time > TIME_BETWEEN_TICKS:
            piece, piece_coords, piece_set = board.move_down(piece, piece_coords, piece_idx)

            board.check_rows()
            last_tick_time = time.time()
        else:
            pass
        board.render(screen)
        board.render_piece(screen, piece, piece_coords, piece_idx)

        if piece_set:  # collided with bottom or another piece on tick
            piece_idx, piece = get_rand_piece()
            piece_coords = np.array([0, 0])

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
