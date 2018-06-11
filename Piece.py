from Constants import COLOR, PIECE
from Square import Square


# Implements the moves of all the chess pieces
class Piece:
    def __init__(self, piece_type, color):
        if piece_type not in PIECE.PIECE_TYPES:
            raise Exception("Unsupported piece type '%s'" % piece_type)
        if color not in COLOR.COLORS:
            raise Exception("Unsupported color '%s'" % color)

        self.piece_type = piece_type
        self.color = color

    char_map = {PIECE.KING: 'k', PIECE.QUEEN: 'q', PIECE.BISHOP: 'b', PIECE.KNIGHT: 'n', PIECE.ROOK: 'r',
                PIECE.PAWN: 'p', PIECE.EMPTY: ' '}

    @staticmethod
    def create(string):
        reverse_map = {v: k for k, v in Piece.char_map.items()}
        piece_type = reverse_map.get(string.lower())
        color = COLOR.BLACK if string == string.lower() else COLOR.WHITE
        return Piece(piece_type, color)

    # Returns all indices between start and end, in the appropriate order
    @staticmethod
    def _interpolate(start, end):
        values = list(range(min(start, end), max(start, end) + 1))
        return values if end > start else list(reversed(values))

    def traversed_squares(self, orig, dest):
        return Piece._traversed_squares_internal(self.piece_type, orig, dest)

    # Which squares do we pass on the way, assuming it's a valid destination square?
    @staticmethod
    def _traversed_squares_internal(piece_type, orig, dest):
        squares = [orig, dest]

        if piece_type == PIECE.ROOK:
            if orig.x == dest.x:
                squares = [Square(orig.x, y) for y in Piece._interpolate(orig.y, dest.y)]
            else:
                squares = [Square(x, orig.y) for x in Piece._interpolate(orig.x, dest.x)]
        elif piece_type == PIECE.BISHOP:
            squares = [Square(x, y) for x, y in
                       zip(Piece._interpolate(orig.x, dest.x), Piece._interpolate(orig.y, dest.y))]
        elif piece_type == PIECE.QUEEN:
            return Piece._traversed_squares_internal(PIECE.ROOK, orig, dest) \
                if orig.x == dest.x or orig.y == dest.y else Piece._traversed_squares_internal(PIECE.BISHOP, orig, dest)
        elif piece_type == PIECE.PAWN:
            squares = [Square(orig.x, y) for y in Piece._interpolate(orig.y, dest.y)]
        elif piece_type == PIECE.EMPTY:
            raise Exception("Empty squares can't move...")

        return squares[1:-1]

    # Check if the piece can capture between these two squares (same as can_move except for pawns)
    def can_capture(self, orig, dest):
        if self.piece_type != PIECE.PAWN:
            return self.can_move(orig, dest)

        return abs(dest.x - orig.x) == 1 and (self.color == COLOR.WHITE and dest.y - orig.y == 1 or
                                              self.color == COLOR.BLACK and dest.y - orig.y == -1)

    # Check if the piece can move between these two squares, not taking intervening pieces into account
    def can_move(self, orig, dest):
        return Piece._can_move_internal(self.piece_type, self.color, orig, dest)

    @staticmethod
    def _can_move_internal(piece_type, color, orig, dest):
        # Actual movement is required in chess
        if orig.x == dest.x and orig.y == dest.y:
            return False

        if piece_type == PIECE.KING:
            return abs(dest.x - orig.x) <= 1 and abs(dest.y - orig.y) <= 1
        if piece_type == PIECE.ROOK:
            return dest.x == orig.x or dest.y == orig.y
        if piece_type == PIECE.BISHOP:
            return abs(dest.x - orig.x) == abs(dest.y - orig.y)
        if piece_type == PIECE.KNIGHT:
            return {abs(dest.x - orig.x), abs(dest.y - orig.y)} == {1, 2}
        if piece_type == PIECE.QUEEN:
            return any([Piece._can_move_internal(x, color, orig, dest) for x in [PIECE.ROOK, PIECE.BISHOP]])
        if piece_type == PIECE.PAWN:
            return orig.x == dest.x and \
                   ((color == COLOR.WHITE and (dest.y - orig.y == 1 or orig.y == 1 and dest.y == 3)) or
                    (color == COLOR.BLACK and (dest.y - orig.y == -1 or orig.y == 6 and dest.y == 4)))
        if piece_type == PIECE.EMPTY:
            raise Exception("Empty squares can't move...")

    def __repr__(self):
        char = Piece.char_map.get(self.piece_type)
        return char.upper() if self.color == COLOR.WHITE else char
