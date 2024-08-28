from go_game.board import Board
from go_game.player import Player


def main():
    board = Board()
    player_black = Player("B")
    player_white = Player("W")

    current_player = player_black
    board.set_current_player(current_player)

    while True:
        board.display()
        row, col = map(
            int,
            input(
                f"Player { current_player.color}, enter your move (row col): "
            ).split(),
        )
        if current_player.make_move(board, row, col):
            # After a successful move, switch to the next player
            current_player = (
                player_white if current_player == player_black else player_black
            )
            board.set_current_player(current_player)
        else:
            print("Invalid move, try again.")


if __name__ == "__main__":
    main()
