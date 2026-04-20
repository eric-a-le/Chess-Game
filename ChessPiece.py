"""
Piece class to represent each piece.
"""

from abc import ABC, abstractmethod

class ChessPiece(ABC):
    """
    Abstract representation of the pieces.

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """

    def __init__(self, color):
        self._color = color
        self._has_moved = False # need this for pawns and castling

    @property
    def color(self):
        """
        Property method that returns the color of the piece.
        """
        return self._color
    
    @property
    def has_moved(self):
        """
        Property method that returns whether the piece has moved.
        """
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        self._has_moved = value

    @abstractmethod
    def valid_moves(self, col, row, board):
        """
        Check the board for all squares the piece can geometrically move to.
        
        Args:
            col: An int representing the current file position of the piece
            row: An int representing current rank position of the piece
            board: A board instance representing the chessboard

        Returns:
            A list of tuples that represent possible coordinates
            the piece can move to.
        """
        pass


    def _slide(self, col, row, directions, board):
        """
        Helper to check candidate moves for sliding pieces (rook bishop queen).
        Walks in each direction until blocked or out of bounds.

        Args:
            col: An int representing the current file position of the piece
            row: An int representing current rank position of the piece
            directions: A list of tuples representing direction vectors
            board: A board instance representing the chessboard

        Returns:
            A list of tuples that represent possible coordinates
            the sliding piece can move to.
        """
        moves = []
        for dc, dr in directions:
            c, r = col + dc, row + dr
            while 0 <= c <= 7 and 0 <= r <= 7: # walk until piece encounters edge of board
                target = board.get_piece(c, r)
                if target is None:
                    moves.append((c, r))
                elif target.color != self.color:
                    moves.append((c, r)) # capture, then stop
                    break
                else:
                    break # blocked by own piece
                c += dc
                r += dr
        return moves


class Knight(ChessPiece):
    """
    Implementation of move rules for the Knight.

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """
    
    def valid_moves(self, col, row, board):        
        candidates = [
            (col + 2, row + 1), (col + 2, row - 1),
            (col - 2, row + 1), (col - 2, row - 1),
            (col + 1, row + 2), (col + 1, row - 2),
            (col - 1, row + 2), (col - 1, row - 2),
        ]
        
        return [
            (c, r) for c, r in candidates
            if 0 <= c <= 7 and 0 <= r <= 7
            and (board.get_piece(c, r) is None
                 or board.get_piece(c, r).color != self.color)
        ]



class Bishop(ChessPiece):
    """
    Implementation of move rules for the Bishop.

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """

    def valid_moves(self, col, row, board):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._slide(col, row, directions, board)



class Rook(ChessPiece):
    """
    Implementation of move rules for the Rook.

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """

    def valid_moves(self, col, row, board):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._slide(col, row, directions, board)
    


class Queen(ChessPiece):
    """
    Implementation of move rules for the Queen.

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """

    def valid_moves(self, col, row, board):
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1), # rook directions
            (1, 1), (1, -1), (-1, 1), (-1, -1) # bishop directions
        ]
        return self._slide(col, row, directions, board)
    


class King(ChessPiece):
    """
    Partial implementation of move rules for the King.
    Note: King-is-checked logic not implemented here.

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """

    def valid_moves(self, col, row, board):
        candidates = [
            (col, row + 1), (col, row - 1),
            (col + 1, row), (col - 1, row),
            (col + 1, row + 1), (col + 1, row - 1),
            (col - 1, row + 1), (col - 1, row - 1),
        ]
        
        moves = [
            (c, r) for c, r in candidates
            if 0 <= c <= 7 and 0 <= r <= 7
            and (board.get_piece(c, r) is None
                 or board.get_piece(c, r).color != self.color)
        ]

        moves += self._castling_moves(col, row, board)
        return moves
    

    def _castling_moves(self, col, row, board):
        """
        Helper to determine kingside and queenside castling.
        Checks that king hasn't moved, rook hasn't moved, & squares between are empty.
        TODO: Check if king is in or passes through check in ChessController

        Args:
            col: An int representing the current file position of the piece
            row: An int representing current rank position of the piece
            board: A board instance representing the chessboard

        Returns:
            A list of tuples that represent possible coordinates
            the king can castle to.
        """
        moves = []
        if self.has_moved:
            return moves

        # kingside
        rook = board.get_piece(7, row)

        if (isinstance(rook, Rook) and not rook.has_moved
                and board.get_piece(5, row) is None
                and board.get_piece(6, row) is None):
            moves.append((6, row))

        # queenside
        rook = board.get_piece(0, row)

        if (isinstance(rook, Rook) and not rook.has_moved
                and board.get_piece(1, row) is None
                and board.get_piece(2, row) is None
                and board.get_piece(3, row) is None):
            moves.append((2, row))

        return moves



class Pawn(ChessPiece):
    """
    Partial mplementation of move rules for the Pawn.
    Includes: One step, two step, diagonal capture.
    TODO: Implement en passant & promotion in ChessController

    Attributes:
        _color: A string representing the color of the piece
        _has_moved: A boolean representing whether the piece has moved
    """

    def valid_moves(self, col, row, board):
        moves = []

        direction = 1 if self.color == "w" else -1

        # move single square
        if board.get_piece(col, row + direction) is None:
            moves.append((col, row + direction))

            # move two squares (if on starting rank)
            start_row = 1 if self.color == "w" else 6
            if row == start_row and board.get_piece(col, row + 2 * direction) is None:
                moves.append((col, row + 2 * direction))

        # captures: diagonal square immediately in front
        for dc in [-1, 1]:
            target = board.get_piece(col + dc, row + direction)
            if (target is not None
                    and target.color != self.color
                    and 0 <= col + dc <= 7):
                moves.append((col + dc, row + direction))

        return moves