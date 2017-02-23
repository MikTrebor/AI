"""
Extends OthelloCore
"""
import Othello_Core as super
from Othello_Core import *

class OthelloSubCore(super.OthelloCore):
    def is_valid(self, move):
        """Is move a square on the board?"""
        return move in self.squares()

    def opponent(self, player):
        """Get player's opponent piece."""
        if super.PLAYERS[player] == 'Black':
            return super.WHITE  # o
        else:
            return super.BLACK  # @

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        nextIndex = square + direction
        nextMove = board[nextIndex]
        if nextMove == player:
            return None
        while nextMove == self.opponent(player):
            nextIndex += direction
            nextMove = board[nextIndex]
        if nextMove in OUTER or nextMove in EMPTY:
            return None
        else:
            return nextIndex

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        if not (self.is_valid(move)):
            return False
        for dir in super.DIRECTIONS:
            if self.find_bracket(move, player, board, dir) != None:
                if board[move] == super.EMPTY:
                    return True
        return False

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        #print(str(player) + " moves to " + str(move))
        board[move] = player
        for dir in super.DIRECTIONS:
            if (self.find_bracket(move, player, board, dir) != None):
                self.make_flips(move, player, board, dir)
        return board

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        newMove = self.find_bracket(move, player, board, direction)
        if newMove == None:
            return
        newIndex = move + direction
        while not(newMove == newIndex):
            board[newIndex] = player
            newIndex += direction


    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        temp = list()
        for square in self.squares():
            if self.is_legal(square, player, board):
                temp.append(square)
        return temp

    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        return len(self.legal_moves(player, board)) > 0
        # return any(self.is_legal(sq, player, board) for sq in self.squares())

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if self.any_legal_move(self.opponent(prev_player), board):
            return self.opponent(prev_player)
        elif self.any_legal_move(prev_player, board):
            return prev_player
        else:
            return None


    def score(self, player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        pScore = 0
        oScore = 0
        for square in range(len(board)):
            if board[square] == player:
                pScore += 1
            elif board[square] == self.opponent(player):
                oScore += 1
        return pScore - oScore
    def read_board(self, board):
        rep = ''
        for row in range(1, 9):
            begin, end = 10 * row + 1, 10 * row + 9
            for cell in range(begin, end):
                if board[cell] == '.':
                    rep+= ' ' + str(cell)
                else:
                    rep+= '  ' + board[cell]
            rep+='\n'
        return rep
    def count(self, player, board):
        count = 0
        for square in range(len(board)):
            if board[square] == player:
                count += 1
        return count
    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            #return "Cannot move to "
            return '%s cannot move to square %d' % (super.PLAYERS[self.player], self.move)
