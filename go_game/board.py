class Board:
    def __init__(self, size=5):
        self.size = 5
        self.grid = [["." for _ in range(size)] for _ in range(size)]

    def display(self):
        for row in self.grid:
            print(" ".join(row))
        print()

    def is_valid_move(self, row, col):
        # Check if the move is within the grid and the position is not empty
        return (
            0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == "."
        )

    def place_stone(self, row, col, stone):
        if self.is_valid_move(row, col):
            self.grid[row][col] = stone

            # After placing the stone, check and handle captures
            opponent_stone = "W" if stone == "B" else "B"
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.grid[r][c] == opponent_stone:
                        if self.get_liberties(r, c) == 0:
                            self.remove_stones(r, c)

            return True
        else:
            print("Invalid move. Try again.")
            return False

    def _explore_liberties(self, row, col, stone, visited, liberties):
        # Use DFS to explore connected stones and count liberties
        if (row, col) in visited:
            return

        visited.add((row, col))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size:
                if self.grid[r][c] == ".":
                    liberties.add((r, c))  # Add the position of the liberty to the set
                elif self.grid[r][c] == stone:
                    self._explore_liberties(r, c, stone, visited, liberties)

        return liberties

    def get_liberties(self, row, col):
        # Ensure the position is within the grid and has a stone
        if not (0 <= row < self.size and 0 <= col < self.size):
            return 0
        stone = self.grid[row][col]
        if stone == ".":
            return 0

        visited = set()
        liberties = set()  # Create a set to store unique liberties
        liberties = self._explore_liberties(row, col, stone, visited, liberties)
        return len(liberties)

    def _collect_stones_to_remove(self, row, col, stone, visited, stones_to_remove):
        if (row, col) in visited:
            return

        visited.add((row, col))
        stones_to_remove.append((row, col))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size:
                if self.grid[r][c] == stone:
                    self._collect_stones_to_remove(
                        r, c, stone, visited, stones_to_remove
                    )

    def remove_stones(self, row, col):
        stone = self.grid[row][col]
        if stone == ".":
            return
        visited = set()
        stones_to_remove = []
        self._collect_stones_to_remove(row, col, stone, visited, stones_to_remove)

        # Remove all collected stones
        for r, c in stones_to_remove:
            self.grid[r][c] = "."
