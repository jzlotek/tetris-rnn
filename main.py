import pygame
import sys
import colors
import numpy as np
import time

from pygame import K_DOWN, K_LEFT, K_UP, K_RIGHT, K_KP_ENTER

from board import Board

pygame.init()

size = width, height = 640, 480

def get_inputs_user() -> np.array:
    key = pygame.key.get_pressed()
    return np.array([key[K_UP], key[K_DOWN], key[K_LEFT], key[K_RIGHT]])


def main():
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    screen.fill(colors.BLACK)
    TIME_BETWEEN_TICKS = 1
    last_tick_time = time.time()
    board = Board()

    board.check_rows()
    board.render(screen)
    pygame.display.update()

    while not board.game_over():
        tps = clock.tick(60)
        # fps = clock.get_fps()
        inputs = get_inputs_user()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if time.time() - last_tick_time > TIME_BETWEEN_TICKS:
            board.tick_piece()
            board.check_rows()
            board.render(screen)
            last_tick_time = time.time()
        else:
            pass

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
