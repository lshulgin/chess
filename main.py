from Board import Board
from Game import Game
import random

num_moves = 10
b = Board.default()

print("Generating a random chess game with %d moves" % num_moves)
print("Still some work to do -- no castling, en passant, or enforcing checks/mates/king captures")
print("")
print("Initial position:")
print(b)

moves = []
for i in range(2 * num_moves):
    legal_moves = b.legal_moves()

    if not len(legal_moves):
        break

    move_index = random.randint(0, len(legal_moves) - 1)
    move = legal_moves[move_index]
    moves.append(move)

    b.make_move(move)

game = Game(moves)

print("")
print("Moves: %s" % game)

print("")
print("Final position:")
print(b)
