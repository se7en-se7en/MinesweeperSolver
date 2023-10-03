from game import Minesweeper
import threading
import time

class Solver:

    def __init__(self, game):
        self.game = game

    def playGame(self):
        while not self.game.game_over:
            self.makeMove(0, 0, "u")
            time.sleep(1)  # sleep

        if not self.game.game_over:
            self.game.play()

        print("Game Over")

    #def decide_move(self):
        #we need to figure out how to decide what move to make


    def makeMove(self, row, col, action):
        self.game.external_move(row, col, action)

    def gameCallback(self, game_instance):  #callback
        game_instance.display_board()


if __name__ == "__main__":
    solver = Solver(None)  # Initialize solver
    game = Minesweeper(8, 8, 4, callback=solver.gameCallback)
    solver.game = game


    game_thread = threading.Thread(target=solver.playGame)
    game_thread.start()

    game_thread.join()
