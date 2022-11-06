import chess as ch
import random as rd
import pandas as pd


from Engines.DumbChessEngine import DumbChessEngine
from Engines.MiniMaxClassical import MiniMaxClassical
from Engines.DeepChessEngine import DeepChessEngine

class Puzzle:

    def __init__(self, chess_engine, moves, puzzle_fen):
        self.chess_engine = chess_engine
        self.board = ch.Board(fen=puzzle_fen)
        self.moves = moves
    
    def can_solve_puzzle(self):
        engine_play = True
        self.board.push(ch.Move.from_uci(self.moves[0]))

        for move in self.moves[1:]:
            if engine_play:
                engine_play = not engine_play
                choosed = self.chess_engine.choose_move(self.board, self.board.turn)
                if choosed.uci() != move:
                    return False
                else:
                    self.board.push(ch.Move.from_uci(move))
            else:
                engine_play = not engine_play
                self.board.push(ch.Move.from_uci(move))
        
        return True

df = pd.read_csv('Data\FilteredPuzzles.csv')

num_puzzles = 0
PATH = "Data\DeepChessLichessDepth3.csv"
f = open(PATH, "w")

f.write("PuzzleId,Rating,Themes,OpeningFamily,Solved\n")
for i in range(5000):

    if num_puzzles % 5 == 0:
        print(num_puzzles, (num_puzzles*100/5000))
        f.close()
        f = open(PATH, "a")
    
    num_puzzles += 1

    solved = Puzzle(DeepChessEngine(), df.Moves[i].split(),df.FEN[i]).can_solve_puzzle()

    f.write(f"{df.PuzzleId[i]},{df.Rating[i]},{df.Themes[i]},{df.OpeningFamily[i]},{solved}\n")
f.close()