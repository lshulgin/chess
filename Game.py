import math


# A group of moves -- just used for display purposes at this point
class Game:
    def __init__(self, moves):
        self.moves = moves

    def __repr__(self):
        move_pairs = [self.moves[i * 2:i * 2 + 2] for i in range(int(math.ceil(len(self.moves) / 2)))]
        move_pairs_formatted = ['%d.%s' % (i + 1, ' '.join([str(x) for x in pair])) for i, pair in
                                enumerate(move_pairs)]
        return ' '.join(move_pairs_formatted)
