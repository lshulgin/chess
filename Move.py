from Constants import PIECE


# Simple class, used to displaying chess moves in algebraic notation
class Move:
    def __init__(self, board, orig, dest):
        self.orig = orig
        self.dest = dest

        piece_orig, piece_dest = map(board.get_piece, [orig, dest])
        self.capture = piece_dest.piece_type != PIECE.EMPTY
        self.orig_string = str(piece_orig).upper() if piece_orig.piece_type != PIECE.PAWN else (
            str(orig)[0] if self.capture else '')

    # TO-DO: Deal with ambiguous moves, i.e. if both knights can go to a square
    def __repr__(self):
        return '%s%s%s' % (self.orig_string, 'x' if self.capture else '', self.dest)
