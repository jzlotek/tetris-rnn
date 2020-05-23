import numpy as np
import colors
import pygame

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
    def __init__(self, board_rows=20, board_cols=10):
        self._board = np.zeros((board_rows, board_cols), dtype=np.int)
        # self._board = np.random.uniform(low=0, high=8, size=(board_rows, board_cols))
        # self._board = self._board.astype(np.int)

    def apply_command(self, piece, curr_coords: np.array, commands: np.array):
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

    def out_of_bounds(self, piece, pos):
        b_h, b_w = self._board.shape
        x, y = pos
        h, w = piece.shape
        return (x < 0 or y < 0) or (x + w > b_w or y + h > b_h)

    def collides(self, piece, pos):
        x, y = pos
        h, w = piece.shape
        sub_region = self._board[y:y + h, x:x + w].astype(bool).astype(int)
        return np.sum(piece.astype(bool).astype(int) & sub_region) != 0

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
