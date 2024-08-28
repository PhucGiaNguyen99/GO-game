class Board:
    def __init__(self, size=5):
        self.size = 5
        self.grid = [["." for _ in range(size)] for _ in range(size)]
        self.current_player = None  # Keep track the current player
        self.previous_states = set()

    def save_state(self):
        # Create a tuple representing the board's current state
        state = tuple(tuple(row) for row in self.grid)
        self.previous_states.add(state)

    def is_ko_move(self):
        state = tuple(tuple(row) for row in self.grid)
        return state in self.previous_states

    def set_current_player(self, player):
        self.current_player = player

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
            # Temporarily place the stone
            self.grid[row][col] = stone

            # Check if the move violates the Ko rule
            if self.is_ko_move():
                print("Ko rule violated! You cannot repeat the previous board state.")
                self.grid[row][col] = "."
                return False

            # Save the state after a valid move
            self.save_state()

            # After placing the stone, check and handle captures
            opponent_stone = "W" if stone == "B" else "B"
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.grid[r][c] == opponent_stone:
                        print("self.get_liberties: ", self.get_liberties(r, c))
                        if self.get_liberties(r, c) == 0:
                            print("call remove stones!!!!!!!")
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
        # Update the player's captured stones
        for r, c in stones_to_remove:
            self.grid[r][c] = "."
        print("current_player: ", self.current_player)
        if self.current_player:
            print("Stones to remove: ", stones_to_remove)
            self.current_player.capture_stones(len(stones_to_remove))

    def _explore_territory(self, row, col, visited, current_player):
        # Identify and calculate the areas of empty spaces on the board that are completely surrounded by a single player's stones

        # A list used for implementing the flood-fill algorithm
        # It starts with the initial position and expands to include all connected empty points
        queue = [(row, col)]

        # A set that stores all the coordinates of the empty points that are part of the territory being explored
        territory = set()

        # A boolean that tracks whether the territory is fully surrounded by the current player's stones
        surrounded_by_player = True

        # The color of the stones that are surroounding the territory
        # It starts with 'None' and is set once the first surrounding stone is found
        stone_color = None

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.pop(0)

            if (r, c) in visited:
                continue

            visited.add((r, c))

            territory.add((r, c))

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    # Append all the surrounding points of the current point which is empty
                    if self.grid[nr][nc] == ".":
                        queue.append((nr, nc))
                    # Mark the color for the first surrounding point of the current point
                    elif self.grid[nr][nc] != "." and stone_color is None:
                        stone_color = self.grid[nr][nc]
                    # If there is 2 color points surrounding the current point
                    elif self.grid[nr][nc] != "." and self.grid[nr][nc] != stone_color:
                        surrounded_by_player = False

        return (
            territory,
            surrounded_by_player and stone_color == current_player.color,
        )

    def calculate_territory(self, player):
        visited = set()
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == "." and (r, c) not in visited:
                    territory, surrounded_by_player = self._explore_territory(
                        r, c, visited, player
                    )
                    if surrounded_by_player:
                        player.add_territory(len(territory))

    def end_game(board, player_black, player_white):
        board.calculate_territory(player_black)
        board.calculate_territory(player_white)

        black_score = player_black.score()
        white_score = player_white.score()

        print(f"Final Score - Black: {black_score}, White: {white_score}")
        if black_score > white_score:
            print("Black wins!")
        elif white_score > black_score:
            print("White wins!")
        else:
            print("It's a tie!")
