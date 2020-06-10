#!/usr/bin/env python
import copy
import numpy as np

import colors


STARTING_POS = np.array([4, 0])


class Piece():
    def __init__(
        self,
        ID: int,
        color: (int, int, int),
        blocks: np.array,
        pos: np.array
    ):
        self.ID = ID
        self.color = color
        self.blocks = blocks
        self.pos = pos
        self.isSet = False

    def setDown(self) -> None:
        self.isSet = True

    def copy(self) -> 'Piece':
        return copy.deepcopy(self)


class PieceFactory():
    def __init__(
        self,
        ID: int,
        color: (int, int, int),
        blocks: np.array,
        pos: np.array
    ) -> 'PieceFactory':
        self.ID = ID
        self.color = color
        self.blocks = blocks
        self.pos = pos

    def create_piece(self) -> 'Piece':
        return Piece(self.ID, self.color, self.blocks, self.pos)

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
