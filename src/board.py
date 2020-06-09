import numpy as np
import colors
import pygame

from piece import PieceFactory

BLOCK_SIZE = 20

STARTING_POS = np.array([4, 0])

PIECE_FACTORIES = [
    PieceFactory(1,
                 colors.YELLOW,
                 np.array([[1, 1], [1, 1]]),
                 STARTING_POS),
    PieceFactory(2,
                 colors.RED,
                 np.array([[1, 1, 0], [0, 1, 1]]),
                 STARTING_POS),
    PieceFactory(3,
                 colors.GREEN,
                 np.array([[0, 1, 1], [1, 1, 0]]),
                 STARTING_POS),
    PieceFactory(4,
                 colors.ORANGE,
                 np.array([[0, 0, 1], [1, 1, 1]]),
                 STARTING_POS),
    PieceFactory(5,
                 colors.BLUE,
                 np.array([[1, 0, 0], [1, 1, 1]]),
                 STARTING_POS),
    PieceFactory(6,
                 colors.PURPLE,
                 np.array([[0, 1, 0], [1, 1, 1]]),
                 STARTING_POS),
    PieceFactory(7,
                 colors.CYAN,
                 np.array([[1, 1, 1, 1]]),
                 STARTING_POS),
]


class Board:
    def __init__(self, board_rows=20, board_cols=10):
        self._board = np.zeros((board_rows, board_cols), dtype=np.int)
        self.rows = board_rows
        self.cols = board_cols

    def add_piece(self, piece):
        pass

    def valid_move(self, piece, pos):
        return not self.out_of_bounds(piece, pos) and \
            not self.collides(piece, pos)

    def apply_command(
            self,
            piece,
            commands: np.array
    ):
        up, down, left, right = commands
        new_piece = piece.copy()
        if up:  # Do rotate
            new_piece.blocks = np.rot90(new_piece.blocks)
            if self.valid_move(new_piece, new_piece.pos):
                piece = new_piece.copy()

        if left:  # Move
            new_coords = piece.pos + np.array([-1, 0])
            if self.valid_move(piece, new_coords):
                piece.pos = new_coords.copy()
        elif right:  # Move
            new_coords = piece.pos + np.array([1, 0])
            if self.valid_move(piece, new_coords):
                piece.pos = new_coords.copy()

        if down:  # Drop
            while not piece.isSet:
                piece = \
                    self.move_down(piece)

        return piece.copy()

    def out_of_bounds(self, piece, pos):
        b_h, b_w = self._board.shape
        x, y = pos
        h, w = piece.blocks.shape
        return (x < 0 or y < 0) or (x + w > b_w or y + h > b_h)

    def collides(self, piece, pos):
        x, y = pos
        h, w = piece.blocks.shape
        sub_region = self._board[y:y + h, x:x + w].astype(bool).astype(int)
        return np.sum(piece.blocks.astype(bool).astype(int) & sub_region) != 0

    def game_over(self):
        return self._board[0].sum() != 0

    def check_rows(self):
        sums = \
            np.argwhere(self._board.astype(bool).astype(int).sum(axis=1)
                        == self._board.shape[1])
        if len(sums) == 0:
            return 0

        for row in reversed(range(self._board.shape[0])):
            if np.sum(self._board[row].astype(bool).astype(int)) == \
                    self._board.shape[1]:
                self._board[row, :] = np.zeros((1, self._board.shape[1]))

            if row == self._board.shape[0] - 1:
                continue

            offset = 0
            while offset + row + 1 < self._board.shape[0] and \
                    np.sum(self._board[row + 1 + offset]) == 0:
                self._board[row + offset + 1, :] = \
                    self._board[row + offset, :]
                self._board[row + offset, :] = \
                    np.zeros((1, self._board.shape[1]))
                offset += 1
        return len(sums)

    def move_down(self, piece):
        down_step = np.array([0, 1])

        # set piece in board
        if self.out_of_bounds(piece, piece.pos + down_step) or \
                self.collides(piece, piece.pos + down_step):
            x, y = piece.pos
            for j, row in enumerate(piece.blocks):
                for i, col in enumerate(row):
                    if col != 0:
                        self._board[y + j, x + i] = piece.ID
            piece.setDown()
            return piece.copy()
        else:
            piece.pos += down_step
            return piece.copy()

    def get_board(self):
        return np.copy(self._board)

    def draw_bordered_rect(
            self,
            screen,
            color,
            x,
            y,
            border=3
    ):
        r = pygame.Rect(
                (x * BLOCK_SIZE, BLOCK_SIZE * y),
                (BLOCK_SIZE, BLOCK_SIZE),
            )
        pygame.draw.rect(
            screen,
            colors.DARKGREY,
            r,
            border,
        )
        screen.fill(color, r)

    def render_piece(self, screen, piece):
        x, y = piece.pos
        color = piece.color
        for idx_r, row in enumerate(piece.blocks):
            for idx_c, col in enumerate(row):
                if col != 0:
                    self.draw_bordered_rect(
                        screen, color, idx_c+x, idx_r+y)

    def render(self, screen: pygame.Surface):
        for idx_r, row in enumerate(self._board):
            for idx_c, col in enumerate(row):
                if col != 0:
                    color = PIECE_FACTORIES[col-1].color
                else:
                    color = colors.BLACK
                self.draw_bordered_rect(
                    screen, color, idx_c, idx_r)
