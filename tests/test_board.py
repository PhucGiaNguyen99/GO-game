import unittest
from go_game.board import Board
from go_game.player import Player


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_place_stone_valid_move(self):
        result = self.board.place_stone(0, 0, "B")
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], "B")

    def test_place_stone_on_occupied_spot(self):
        self.board.place_stone(0, 0, "B")
        result = self.board.place_stone(0, 0, "W")
        self.assertFalse(result)
        self.assertEqual(self.board.grid[0][0], "B")

    def test_place_stone_outside_board(self):
        result = self.board.place_stone(5, 5, "B")
        self.assertFalse(result)
        result = self.board.place_stone(-1, -2, "W")
        self.assertFalse(result)
        # Ensure that the board remains unchanged
        for row in self.board.grid:
            self.assertTrue(all(cell == "." for cell in row))

    def test_get_liberties(self):
        # Place a stone with all liberties open
        self.board.place_stone(1, 1, "B")
        liberties = self.board.get_liberties(1, 1)
        self.assertEqual(liberties, 4)

        # Place stones around the first stone to redure its liberties
        self.board.place_stone(0, 1, "W")
        self.board.place_stone(2, 1, "W")
        self.board.place_stone(1, 2, "W")
        liberties = self.board.get_liberties(1, 1)
        self.assertEqual(liberties, 1)

        # Fully surround the stone
        self.board.place_stone(1, 0, "W")
        liberties = self.board.get_liberties(1, 1)
        self.assertEqual(liberties, 0)

    def test_liberties_of_vertical_group(self):
        self.board.place_stone(1, 1, "B")
        self.board.place_stone(2, 1, "B")
        liberties = self.board.get_liberties(1, 1)
        self.assertEqual(liberties, 6)

    def test_liberties_of_horizontal_group(self):
        self.board.place_stone(1, 1, "B")
        self.board.place_stone(1, 2, "B")
        liberties = self.board.get_liberties(1, 1)
        self.assertEqual(liberties, 6)

    def test_liberties_of_l_shaped_group(self):
        self.board.place_stone(2, 1, "B")
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(3, 1, "B")
        liberties = self.board.get_liberties(2, 1)
        self.assertEqual(liberties, 7)

    def test_liberties_of_fully_surrounded_group(self):
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(2, 3, "B")
        self.board.place_stone(1, 2, "W")
        self.board.place_stone(1, 3, "W")
        self.board.place_stone(3, 2, "W")
        self.board.place_stone(3, 3, "W")
        self.board.place_stone(2, 1, "W")
        self.board.place_stone(2, 4, "W")

        liberties = self.board.get_liberties(2, 2)
        self.assertEqual(liberties, 0)

    def test_liberties_of_large_group(self):
        self.board.place_stone(1, 1, "B")
        self.board.place_stone(1, 2, "B")
        self.board.place_stone(2, 1, "B")
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(3, 1, "B")
        self.board.place_stone(3, 2, "B")

        liberties = self.board.get_liberties(2, 2)
        self.assertEqual(liberties, 10)

    def test_capture_single_stone(self):
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(1, 2, "W")
        self.board.place_stone(3, 2, "W")
        self.board.place_stone(2, 1, "W")
        self.board.place_stone(2, 3, "W")

        self.assertEqual(self.board.grid[2][2], ".")  # Black stone should be captured

    def test_capture_group_of_stones(self):
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(2, 3, "B")
        self.board.place_stone(1, 2, "W")
        self.board.place_stone(1, 3, "W")
        self.board.place_stone(3, 2, "W")
        self.board.place_stone(3, 3, "W")
        self.board.place_stone(2, 1, "W")
        self.board.place_stone(2, 4, "W")

        self.assertEqual(self.board.grid[2][2], ".")  # The group should be captured
        self.assertEqual(self.board.grid[2][3], ".")

    def test_no_capture_if_liberties_remain(self):
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(1, 2, "W")
        self.board.place_stone(3, 2, "W")
        self.board.place_stone(2, 1, "W")
        # One liberty remains at (2,3)
        self.assertEqual(
            self.board.grid[2][2], "B"
        )  # Black stone should not be captured

    def test_capture_after_filling_last_liberty(self):
        self.board.place_stone(2, 2, "B")
        self.board.place_stone(1, 2, "W")
        self.board.place_stone(3, 2, "W")
        self.board.place_stone(2, 1, "W")
        self.board.place_stone(2, 3, "W")  # This should capture the black stone

        self.assertEqual(self.board.grid[2][2], ".")  # Black stone should be captured

    def test_ko_rule(self):
        self.board.set_current_player(self.player_black)
        self.player_black.make_move(self.board, 2, 2)
        self.player_white.make_move(self.board, 1, 2)
        self.player_white.make_move(self.board, 3, 2)
        self.player_white.make_move(self.board, 2, 1)
        self.player_white.make_move(self.board, 2, 3)

        # Black retakes the position
        self.board.set_current_player(self.player_black)
        self.player_black.make_move(self.board, 1, 3)
        # Now White tries to make a Ko move
        ko_move = self.player_white.make_move(self.board, 2, 2)
        self.assertFalse(ko_move)

    def test_single_point_territory(self):
        # Black surrounds a single empty point
        self.board.grid = [
            [".", ".", ".", ".", "."],
            [".", "B", "B", "B", "."],
            [".", "B", ".", "B", "."],
            [".", "B", "B", "B", "."],
            [".", ".", ".", ".", "."],
        ]
        self.player_black = Player("B")
        self.player_white = Player("W")
        self.board.calculate_territory(self.player_black)
        self.assertEqual(self.player_black.territory, 1)


if __name__ == "__main__":
    unittest.main()
