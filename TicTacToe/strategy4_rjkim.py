#Robert Kim, December 2016

#from core import *
import random

#def get_move(self):
#    move = self.minimax(self.myBoard, self.myPlayer, self.maxDepth) #
#    #update board
#    #update player
#    return move

def eval(board):
    maxOnes, minOnes = one_count(board)
    maxTwos, minTwos = two_count(board)
    return ((3*maxTwos) + (1*maxOnes)) - ((3*minTwos) + (1*minOnes))


    #if terminal_test(board) == MAX:
     #   return 9001
    #elif terminal_test(board) == MIN:
    #    return -9001
    #else:
    #    return 0
def human():
    def strategy(board, player):
        print_board(board)
        print("Choose a number 0-8: ")
        spot = int(input())
        while spot > 8:
            print("Try another number: ")
            spot = int(input())
        board = (board[:spot] + player + board[spot+1:])
        print("Moved. ")
        return spot

    return strategy

def randAI():
    def strategy(board, player):
        return actions(board)[0]

    return strategy


def minimax_strategy(max_depth):
    """ Takes a max_depth parameter and returns a new function/closure for strategy """
    def strategy(board, player):
        return minimax(board, player, max_depth)
    return strategy

def minimax(board, player, max_depth):
    """ Takes a current board and player and max_depth and returns a best move
     This is the top level mini-max function. Note depth is ignored. We
     always search to the end of the game."""

    if player == MAX:
        move= max_dfs(board, player, max_depth, 0)[1]
    if player == MIN:
        move= min_dfs(board, player, max_depth, 0)[1]
    move= min_dfs(board, player, max_depth, 0)[1]
    return move

def max_dfs(board, player, max_d, current_d=0):
    #if not(terminal_test(board) == False):
    if(terminal_test(board)):
        if terminal_test(board) == MAX:
            return 1, None
        else:
            return -1, None
    if current_d == max_d:
        return eval(board), None
    v = -9001
    move = -1
    for m in actions(board):
        new_board = assign(board, m, player)
        if (new_board, player) in minimax_dict.keys():
            new_value = minimax_dict[(new_board, player)]
        else:
            new_value = min_dfs(new_board, toggle(player), max_d, current_d+1)[0]
            minimax_dict[(new_board, player)] = new_value

        #new_value = min_dfs(assign(board, m , player), toggle(player), max_d, current_d+1)[0]
        if new_value == 9001:
            return new_value, m
        if new_value > v:
            v = new_value
            move = m
    return v, move

def min_dfs(board, player, max_d, current_d=0):
   #if not(terminal_test(board) == False):
    if(terminal_test(board)):
        if terminal_test(board) == MAX:
            return 1, None
        else:
            return -1, None
    if current_d == max_d:
        return eval(board), None
    v = 9001
    move = -1
    for m in actions(board):
        new_board = assign(board, m, player)
        if (new_board, player) in minimax_dict.keys():
            new_value = minimax_dict[(new_board, player)]
        else:
            new_value = max_dfs(new_board, toggle(player), max_d, current_d+1)[0]
            minimax_dict[(new_board, player)] = new_value

        if new_value == -9001:
            return new_value, m

        #new_value = max_dfs(assign(board, m , player), toggle(player), max_d, current_d+1)[0]
        if new_value < v:
            v = new_value
            move = m
    return v, move

def assign(board, m, player):
    return make_move(board, player, m)


####################   core.py   ####################
import random

######################################################################
# core.py
#
# Implements core functionality for a tic-tac-toe AI game
#
# Imported by: strategy.py
# Imported by: mini-shell.py
#
# Imports: random.py
#
# This implementation has no local or global state
# All functions operate on an immutable board parameter
# And return results to the caller
# (except for the old DFS routine to count boards)
#
# There are some redundancies that crept in as the code evolved
# So it could be cleaned up a bit
#
# This version works on N x N boards
#
# Patrick White Dec 2016
# Modified by Robert Kim Dec 2016
######################################################################

# constants
N = 3
start_state = "."*(N**2)
minimax_dict = dict()
MAX = "X"
MIN = "O"
TIE = "TIE"
endings = (MAX, MIN, TIE)
rows = [[N*i+j for j in range(N)] for i in range(N)]
cols = [[N*j+i for j in range(N)] for i in range(N)]
diags = [list(range(0,N*N,N+1)), list(range(N-1,N*N-2,N-1))]
units = rows + cols + diags
evaluate = {MAX:1, MIN:-1, ".":0, TIE:0}

# globals only used for DFS, not in game play
count = 0
terminal_count = 0
all_boards = []

def print_board(board):
    """ print a tic-tac-toe board as a 2D array"""
    print("                    Key")
    print(   ((" %s | %s | %s ") % (board[0], board[1], board[2]) + "  |  " + ((" %s | %s | %s ") % ("0", "1", "2"))))
    print("---+---+---  |  ---+---+---")
    print(   ((" %s | %s | %s ") % (board[3], board[4], board[5]) + "  |  " + ((" %s | %s | %s ") % ("3", "4", "5"))))
    print("---+---+---  |  ---+---+---")
    print(   ((" %s | %s | %s ") % (board[6], board[7], board[8]) + "  |  " + ((" %s | %s | %s ") % ("6", "7", "8"))))
    #for i in range(N):
    #    print(board[N * i: N * i + N])
    print()


def terminal_test(board):
    """ test is the game board is over, return False if not, else the winner/tie """
    win = winner(board)
    if win is not None: return win
    if not "." in board: return TIE
    else: return False

def two_count(board): #returns number of units in which only one X or O is needed for a solution
    maxPairs = 0
    minPairs = 0
    for group in units:
        maxCount = 0
        minCount = 0
        for spot in group:
            if evaluate[board[spot]] == 1:
                maxCount += 1
            if evaluate[board[spot]] == -1:
                minCount += 1
        if maxCount > 0:
            maxPairs += 1
        if minCount > 0:
            minPairs += 1
    return maxPairs, minPairs

def one_count(board):
    return board.count(MAX), board.count(MIN)


def goal_test(board):
    """ return True iff there are N in a row/col/diag """
    return any(  abs(  sum(  [evaluate[  board[j] ] for j in s]  )  ) == N for s in units  )



def winner(board):
    """ return the winner of winning board, or None if no winner """
    if any(sum([evaluate[board[j]] for j in s]) == N for s in units):
        return MAX
    if any(sum([evaluate[board[j]] for j in s]) == -N for s in units):
        return MIN
    return None


def result(board, player, var):
    """ assigns var to player on board and returns new board, player tuple """
    assert board[var] == ".", "%s is not empty" % str(var)
    new_board = board[:var] + player + board[var + 1:]
    return new_board, toggle(player)


def make_move(board, player, move):
    """ assigns var to player on board and returns new board """
    if board[move] != ".":
        raise IllegalMoveError(board, player, move)
    new_board = board[:move] + player + board[move + 1:]
    return new_board


def next_player(board, player):
    """ returns the next player if board is not finished """
    if terminal_test(board):
        return None
    else:
        return toggle(player)


def actions(board):
    """ returns a list of open squares in board (i.e. string indices) """
    open_squares = [i for (i,c) in enumerate(board) if c == "."]
    random.shuffle(open_squares)
    # use symmetry on first move
    if N==3 and len(open_squares)==9:
        return [0,1,4]
    elif N==4 and len(open_squares)==16:
        return [0,1,5]
    return open_squares


def toggle(player):
    """ returns the opposite of player """
    if player==MAX:
        return MIN
    else:
        return MAX


def dfs(board, player, depth):
    """ simple dfs to generate all game states """
    global count, terminal_count, all_boards

    if depth>4 and terminal_test(board):
        terminal_count+=1
        all_boards.append(board)
        return None

    for a in actions(board):
        dfs(*result(board, player, a), depth + 1)
        count+=1


class IllegalMoveError(Exception):
    def __init__(self, board, player, move ):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return 'Forfeit! %s cannot move to square %d' % (self.player, self.move)

