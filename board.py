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
        self.rows = board_rows
        self.cols = board_cols

    def add_piece(self, piece):
        pass

    def valid_move(self, piece, pos):
        return not self.out_of_bounds(piece, pos) and not self.collides(piece, pos)

    def apply_command(self, piece, curr_coords: np.array, commands: np.array):
        up, down, left, right = commands
        if up:  # Do rotate
            new_piece = np.rot90(piece)
            if self.valid_move(new_piece, curr_coords):
                piece = new_piece

        if left:  # LEFT
            new_coords = curr_coords + np.array([-1, 0])
            if self.valid_move(piece, new_coords):
                curr_coords = new_coords
        elif right:
            new_coords = curr_coords + np.array([1, 0])
            if self.valid_move(piece, new_coords):
                curr_coords = new_coords

        return piece, np.array(curr_coords)

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
            return 0

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
        return len(sums)

    def move_down(self, piece, pos, piece_idx):
        if self.out_of_bounds(piece, pos + np.array([0, 1])) or self.collides(piece, pos + np.array([0, 1])):  # set piece in board
            x, y = pos
            for j, row in enumerate(piece):
                for i, col in enumerate(row):
                    if col != 0:
                        self._board[y + j, x + i] = piece_idx
            return piece, pos, True
        else:
            return piece, pos + np.array([0, 1]), False



    def get_board(self):
        return np.copy(self._board)

    def render_piece(self, screen, piece, pos, piece_idx):
        x, y = pos
        for idx_r, row in enumerate(piece):
            for idx_c, col in enumerate(row):
                color = PIECES[piece_idx - 1][0]
                if col != 0:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(
                            ((idx_c + x) * BLOCK_SIZE, BLOCK_SIZE * (idx_r + y)),
                            (BLOCK_SIZE, BLOCK_SIZE)
                        )
                    )

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
