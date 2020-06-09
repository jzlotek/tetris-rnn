#!/usr/bin/env python
import copy
import numpy as np


class Piece():
    def __init__(
        self,
        ID: int,
        color: (int, int, int),
        blocks: np.array,
        pos: np.array
    ) -> 'Piece':
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
