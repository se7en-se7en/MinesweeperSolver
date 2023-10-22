from game import Minesweeper
from queue import PriorityQueue
import threading
import time
import random

class Solver:

    def __init__(self, game):
        self.game = game

    def playGame(self):
        while not self.game.game_over:
            r, c, action = self.decide_move()
            self.makeMove(r, c, action)
            #time.sleep(1)  # sleep

        if not self.game.game_over:
            self.game.play()

        print("Game Over")

    @staticmethod
    def heuristic(cell, game):

        row, col = cell
        total_distance = 0

        # Loop over rows
        for r in range(game.rows):

            # Loop over cols
            for c in range(game.cols):

                # Check cell n its value is a digit
                if game.revealed[r][c] and game.board[r][c].isdigit():
                    # Calculate the distance between current cell and the given cell
                    distance = abs(row - r) + abs(col - c)

                    # Update the total distance by adding the value in the current cell
                    # divided by the distance
                    value_in_cell = int(game.board[r][c])
                    total_distance += value_in_cell / (1 + distance)

        # Return the negative total distance
        return -total_distance

    def decide_move(self):
        # first move is always top corner
        if all(not any(row) for row in self.game.revealed):
            return 0,0,"u"
        #loop through the current board and check the neighbors, seeing if there are any definite mines
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if not self.game.revealed[r][c]:
                    continue

                if not self.game.board[r][c].isdigit():
                    continue

                num = int(self.game.board[r][c])
                neighbors = []
                for i in range(max(0, r - 1), min(self.game.rows, r + 2)):
                    for j in range(max(0, c - 1), min(self.game.cols, c + 2)):
                        if i != r or j != c:
                            neighbor = (i, j)
                            neighbors.append(neighbor)

                unrevealed_neighbors = []
                for i, j in neighbors:
                    if not self.game.revealed[i][j] and not self.game.flagged[i][j]:
                        unrevealed = (i, j)
                        unrevealed_neighbors.append(unrevealed)


                flagged_neighbors = []
                for coordinate in neighbors:
                    i = coordinate[0]
                    j = coordinate[1]
                    if self.game.flagged[i][j]:
                        flagged = (i, j)
                        flagged_neighbors.append(flagged)

                num_of_flagged_neighbors = len(flagged_neighbors)
                num_of_unrevealed_neighbors = len(unrevealed_neighbors)

                if num == num_of_flagged_neighbors:  # mines are flagged unveil the rest
                    for coordinate in unrevealed_neighbors:
                        i = coordinate[0]
                        j = coordinate[1]
                        return (i, j, "u")

                if num == num_of_unrevealed_neighbors + num_of_flagged_neighbors:  # flag the mines
                    for coordinate in unrevealed_neighbors:
                        i = coordinate[0]
                        j = coordinate[1]
                        return (i, j, "f")

        # # if no definiteve move found, use a*
        # Create  priority queue to store cells based on their heuristic values.
        queue = PriorityQueue()

        # Loop through all the rows of the game board
        for row in range(self.game.rows):

            # Loop through all the columns for the current row
            for col in range(self.game.cols):

                # Check if the cell is revealed or flagged
                if not self.game.revealed[row][col] and not self.game.flagged[row][col]:
                    # Calculate the heuristic value for the cell
                    h = self.heuristic((row, col), self.game)

                    # Add the cell with its heuristic value to the priority queue
                    queue.put((h, (row, col, "u")))

        # After checking all cells if the queue is not empty
        # get the cell with the highest priority or lowest heuristic value
        if not queue.empty():
            return queue.get()[1]


            # If no a* based move found, find cell with lowest probability
        min_prob = float('inf')
        best_move = None
        for row in range(self.game.rows):
            for col in range(self.game.cols):

                # Check if the cell is already revealed or flagged
                if self.game.revealed[row][col] or self.game.flagged[row][col]:
                    continue

                # Find the neighbors of the current cell
                neighbors = []
                for i in range(max(0, row - 1), min(self.game.rows, row + 2)):
                    for j in range(max(0, col - 1), min(self.game.cols, col + 2)):
                        if i != row or j != col:
                            neighbor = (i, j)
                            neighbors.append(neighbor)

                # Count the number of unvieled neighbors
                unrevealed_count = 0
                for i, j in neighbors:
                    if not self.game.revealed[i][j]:
                        unrevealed_count += 1

                # If the count is less than current minimum probability, update best move
                if unrevealed_count < min_prob:
                    min_prob = unrevealed_count
                    best_move = (row, col, "u")

        return best_move


    def makeMove(self, row, col, action):
        self.game.external_move(row, col, action)

    def gameCallback(self, game_instance):  #callback
        game_instance.display_board()

    def make_random_move(self):
        row = random.randint(0, self.game.rows - 1)
        col = random.randint(0, self.game.cols - 1)
        action = "u"
        return row, col, action



if __name__ == "__main__":
    NUM_GAMES = 10000
    wins = 0

    for _ in range(NUM_GAMES):
        solver = Solver(None)  # Init solver
        game = Minesweeper(8, 8, 10, callback=solver.gameCallback)
        solver.game = game

        game_thread = threading.Thread(target=solver.playGame)
        game_thread.start()
        game_thread.join()

        # Check if the game was won
        if game.game_won:
            wins += 1

    # Calculate the win percentage
    win_percentage = (wins / NUM_GAMES) * 100
    print(f"After {NUM_GAMES} games, the robot won {wins} times, with a win percentage of {win_percentage:.2f}%.")
