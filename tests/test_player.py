import unittest
from go_game.board import Board
from go_game.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player_black = Player("B")
        self.player_white = Player("W")

    def test_make_move(self):
        result = self.player_black.make_move(self.board, 2, 2)
        self.assertTrue(result)
        self.assertEqual(self.board.grid[2][2], "B")

    def test_capture_and_score(self):
        self.board.set_current_player(self.player_white)
        self.player_black.make_move(self.board, 2, 2)
        self.player_white.make_move(self.board, 1, 2)
        self.player_white.make_move(self.board, 3, 2)
        self.player_white.make_move(self.board, 2, 1)
        self.player_white.make_move(self.board, 2, 3)
        self.assertEqual(self.player_white.captured_stones, 1)
        self.assertEqual(self.player_white.score(), 1)


if __name__ == "__main__":
    unittest.main()
