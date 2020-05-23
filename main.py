import pygame
import sys
import colors
import numpy as np
import time

from pygame import K_DOWN, K_LEFT, K_UP, K_RIGHT, K_KP_ENTER

pygame.init()

size = width, height = 640, 480

BLOCK_SIZE = 20

PIECES = [
    (colors.YELLOW, np.array([[1, 1], [1, 1]])),
    (colors.RED, np.array([[1, 1, 0], [0, 1, 1]])),
    (colors.GREEN, np.array([[0, 1, 1], [1, 1, 0]])),
    (colors.ORANGE, np.array([[0, 0, 1], [1, 1, 1]])),
    (colors.BLUE, np.array([[1, 0, 0], [1, 1, 1]])),
    (colors.PURPLE, np.array([[0, 1, 0], [1, 1, 1]])),
    (colors.CYAN, np.array([[1, 1, 1, 1]]))
]


class Board:
    def __init__(self, BOARD_ROWS=20, BOARD_COLS=10):
        self._board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=np.int)
        self._board = np.random.uniform(low=0, high=8, size=(BOARD_ROWS, BOARD_COLS))
        self._board = self._board.astype(np.int)

    def apply_command(self, piece, curr_coords, commands):
        """
        :param piece: np.array
        :param commands: [UP, DOWN, LEFT, RIGHT] bool
        """
        x, y = curr_coords
        if commands[0]:  # UP
            new_piece = np.rot90(piece)
            piece_loc = np.zeros(self._board.shape, dtype=np.int)
            piece_loc[y:new_piece.shape[1], x:new_piece.shape[0]] = new_piece[:, :]

            if np.sum(self._board.astype(bool).astype(int) & piece_loc.astype(bool).astype(int)) == 0:  # no collision
                piece = new_piece
                self._board.astype(bool).astype(int) & piece_loc.astype(bool).astype(int)

        elif commands[2]:  # LEFT
            piece_loc = np.zeros(self._board.shape, dtype=np.int)
            piece_loc[y:piece.shape[1], x:piece_loc.shape[0]] = piece_loc[:, :]

            if np.sum(self._board.astype(bool).astype(int) & piece_loc.astype(bool).astype(int)) == 0:  # no collision
                pass

    def game_over(self):
        return self._board[0].sum() != 0

    def check_rows(self):
        sums = np.argwhere(self._board.astype(bool).astype(int).sum(axis=1) == self._board.shape[1])
        if len(sums) == 0:
            return False

        for row in reversed(range(self._board.shape[0])):
            if np.sum(self._board[row].astype(bool).astype(int)) == self._board.shape[1]:
                self._board[row, :] = np.zeros((1, self._board.shape[1]))

            if row == self._board.shape[0] - 1:
                continue

            offset = 0
            while offset + row + 1 < self._board.shape[0] and np.sum(self._board[row + 1 + offset]) == 0:
                self._board[row + offset + 1, :] = self._board[row + offset, :]
                self._board[row + offset, :] = np.zeros((1, self._board.shape[1]))
                offset += 1
        return True

    def get_board(self):
        return np.copy(self._board)

    def render(self, screen: pygame.Surface):
        for idx_r, row in enumerate(self._board):
            for idx_c, col in enumerate(row):
                color = PIECES[col - 1][0] if col != 0 else colors.BLACK
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        (idx_c * BLOCK_SIZE, BLOCK_SIZE * idx_r),
                        (BLOCK_SIZE, BLOCK_SIZE)
                    )
                )


def get_inputs():
    key = pygame.key.get_pressed()
    return (key[K_UP], key[K_DOWN], key[K_LEFT], key[K_RIGHT])


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
        inputs = get_inputs()
        print(inputs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if time.time() - last_tick_time > TIME_BETWEEN_TICKS:
            # board.tick_piece()
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
