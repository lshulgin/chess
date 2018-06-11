from Constants import COLOR, PIECE
from Move import Move
from Piece import Piece
from Square import Square


# An arbitrarily-sized chess board, keeping track of pieces
# Allows setting the starting position, applying moves and checking whether a given move is legal
class Board:
    def __init__(self, n, whose_move=COLOR.WHITE):
        self.n = n
        self.pieces = None
        self.squares = None
        self.whose_move = whose_move

    @staticmethod
    def create(string):
        rows = string.split('\n')
        n = len(rows)
        assert all(len(row) == n for row in rows)
        board = Board(n)
        board.pieces = [[Piece.create(x) for x in row] for row in rows]
        board.squares = [[Square(x, y) for x in range(n)] for y in range(n)]

        return board

    @staticmethod
    def empty(n):
        return Board.create('\n'.join([' ' * n] * n))

    @staticmethod
    def default(n=8):
        if n != 8:
            raise Exception("Can't handle board sizes other than 8x8 yet!")

        first_row = 'RNBQKBNR'
        second_row = 'P' * n
        empty_row = ' ' * n
        string = '\n'.join([first_row, second_row] + [empty_row] * (n - 4) + [second_row.lower(), first_row.lower()])

        return Board.create(string)

    # Is this move legal?
    def is_legal_move(self, orig, dest):
        piece = self.get_piece(orig)
        piece_dest = self.get_piece(dest)

        if piece.piece_type == PIECE.EMPTY:
            return False

        if self.whose_move != piece.color:
            return False

        if piece_dest.piece_type != PIECE.EMPTY and (piece.color == piece_dest.color or
                                                     not piece.can_capture(orig, dest)):
            return False

        if piece_dest.piece_type == PIECE.EMPTY and not piece.can_move(orig, dest):
            return False

        # Path must be clear
        if any([self.get_piece(s).piece_type != PIECE.EMPTY for s in piece.traversed_squares(orig, dest)]):
            return False

        # TO-DO: Deal with castling, en passant
        return True

    # Return all legal moves from a square
    def legal_moves_from_square(self, orig):
        return [Move(self, orig, x) for y in self.squares for x in y if x != orig and self.is_legal_move(orig, x)]

    # All legal moves
    def legal_moves(self):
        squares = [x for y in self.squares for x in y]
        for s in squares:
            self.legal_moves_from_square(s)
        return [x for s in squares for x in self.legal_moves_from_square(s)]

    def get_piece(self, square):
        return self.pieces[square.y][square.x]

    def make_move(self, move):
        orig, dest = move.orig, move.dest
        self.pieces[dest.y][dest.x] = self.pieces[orig.y][orig.x]
        self.pieces[orig.y][orig.x] = Piece.create(' ')
        self.whose_move = [x for x in COLOR.COLORS if x != self.whose_move][0]

    # This one is invertible with Board.from_string
    def _repr_simple(self):
        # Draw upside-down
        return '\n'.join([''.join([str(x) for x in row]) for row in reversed(self.pieces)])

    def __repr__(self):
        rows_pieces = self._repr_simple()
        rows_pieces = [''.join(row) for row in rows_pieces.split('\n')]
        separator = '-' * len(rows_pieces[0])
        rows = [separator] + rows_pieces + [separator]
        rows = ['|%s|' % row for row in rows]

        return '\n'.join(rows)
