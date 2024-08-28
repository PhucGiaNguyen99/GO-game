class Player:
    def __init__(self, color):
        self.color = color
        self.captured_stones = 0  # Keep track the number of captured stones
        self.territory = 0  # Keep track the number of territory points

    def make_move(self, board, row, col):
        if board.place_stone(row, col, self.color):
            return True
        return False

    def capture_stones(self, number):
        # Increase the number of captured stones
        self.captured_stones += number

    def add_territory(self, points):
        self.territory += points

    def score(self):
        return (
            self.captured_stones + self.territory
        )  # For now, the score is sum of captured stones and territory
