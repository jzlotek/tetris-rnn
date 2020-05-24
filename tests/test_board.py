import unittest

from board import Board, PIECES


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_init(self):
        self.assertEqual(self.board.get_board().sum(), 0)

    def test_game_over(self):
        self.assertFalse(self.board.game_over())
        self.board._board[:, 1] = 1
        self.assertTrue(self.board.game_over())

    def test_collides(self):
        self.board._board[-1, :] = 1
        piece = PIECES[0][1]
        pos = [0, 18]
        self.assertTrue(self.board.collides(piece, pos))
        pos = [0, 17]
        self.assertFalse(self.board.collides(piece, pos))

    def test_out_of_bounds(self):
        piece = PIECES[0][1]
        pos = [0, 18]
        self.assertFalse(self.board.out_of_bounds(piece, pos))
        pos = [0, 19]
        self.assertTrue(self.board.out_of_bounds(piece, pos))
        pos = [-1, 18]
        self.assertTrue(self.board.out_of_bounds(piece, pos))
        pos = [19, 18]
        self.assertTrue(self.board.out_of_bounds(piece, pos))
        pos = [0, -1]
        self.assertTrue(self.board.out_of_bounds(piece, pos))

    def test_check_rows(self):
        self.board._board[1:, :] = 1
        self.assertTrue(self.board.check_rows())
        self.assertEqual(self.board.get_board().sum(), 0)

        self.board._board[0, 0] = 1
        self.board._board[0, 1] = 2
        self.board._board[1:, :] = 1
        self.assertTrue(self.board.check_rows())
        self.assertEqual(self.board.get_board().sum(), 3)
        self.assertEqual(self.board.get_board()[-1, 1], 2)

        self.board = Board()
        self.assertEqual(self.board.get_board().sum(), 0)
        self.assertFalse(self.board.check_rows())
