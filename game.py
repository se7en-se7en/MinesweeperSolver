import random


class Minesweeper:
    def __init__(self, rows=8, cols=8, mines=4, callback=None):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.generate_board()
        self.game_over = False
        self.game_won = False
        self.callback = callback

    def external_move(self, row, col, action):

        if self.game_over:  # Game is already over
            return

        if action == 'f':
            self.flagged[row][col] = not self.flagged[row][col]
        elif action == 'u':
            if self.board[row][col] == 'M':
                print("Boom! You hit a mine.")
                self.game_over = True
                return
            else:
                self.reveal(row, col)

            if all(self.board[r][c] == 'M' or self.revealed[r][c] for r in range(self.rows) for c in range(self.cols)):
                print("Congratulations! The robot has cleared the minefield!")
                self.game_over = True
                self.game_won = True

        if self.callback:  # Check if a callback exists
            self.callback(self)

    def generate_board(self):
        for _ in range(self.mines):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'M'
                    break
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 'M':
                    continue
                count = sum(1 for i in range(max(0, row - 1), min(self.rows, row + 2))
                            for j in range(max(0, col - 1), min(self.cols, col + 2))
                            if self.board[i][j] == 'M')
                self.board[row][col] = str(count) if count > 0 else ' '

    def display_board(self):
        print('   ' + ' '.join(str(i) for i in range(self.cols)))
        print('  ' + '-' * (2 * self.cols))
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.flagged[i][j]:
                    row.append('F')
                elif self.revealed[i][j]:
                    row.append(self.board[i][j])
                else:
                    row.append('#')
            print(f"{i} |" + ' '.join(row))

    def play(self):
        while True:
            self.display_board()
            try:
                move = input("Enter your move (row col action), action can be 'u' to unveil or 'f' to flag: ")
                row, col, action = move.split()
                row, col = int(row), int(col)
                if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                    raise ValueError("Invalid row or column number.")
            except ValueError as e:
                print(e)
                print("Invalid input, please enter row col action, for example, '1 2 u'.")
                continue

            if action not in ('u', 'f'):
                print("Invalid action, please enter 'u' to unveil or 'f' to flag.")
                continue

            if action == 'f':
                self.flagged[row][col] = not self.flagged[row][col]
                continue

            if self.board[row][col] == 'M':
                print("Boom! You hit a mine.")
                return
            else:
                self.reveal(row, col)

            if all(self.board[row][col] == 'M' or self.revealed[row][col]
                   for row in range(self.rows) for col in range(self.cols)):
                self.display_board()
                print("Congratulations! You have cleared the minefield!")
                return
            if self.callback:  # Check if a callback exists
                self.callback(self)

    def reveal(self, row, col):
        if self.revealed[row][col] or self.flagged[row][col] or self.board[row][col] == 'M':
            return
        self.revealed[row][col] = True
        if self.board[row][col] == ' ':
            for i in range(max(0, row - 1), min(self.rows, row + 2)):
                for j in range(max(0, col - 1), min(self.cols, col + 2)):
                    self.reveal(i, j)

    def current_board(self):
        board_repr = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.flagged[i][j]:
                    row.append('F')
                elif self.revealed[i][j]:
                    row.append(str(self.board[i][j]))
                else:
                    row.append('#')
            board_repr.append(' '.join(row))
        return board_repr
