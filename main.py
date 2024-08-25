from go_game.board import Board
from go_game.player import Player


def main():

    board = Board()
    player_black = Player("B")
    player_white = Player("W")
    player_black.make_move(board, 2, 2)
    player_white.make_move(board, 1, 2)
    player_white.make_move(board, 3, 2)

    player_white.make_move(board, 2, 1)
    player_white.make_move(board, 2, 3)
    print("Captured stones of White: ", player_white.captured_stones)


if __name__ == "__main__":
    main()
