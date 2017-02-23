import random
import time

import Othello_sub_core as core


class Strategy(core.OthelloSubCore):
    SQUARE_WEIGHTS = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
        0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
        0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
        0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
        0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
        0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
        0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
        0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

    inf_temp = 0
    for num in SQUARE_WEIGHTS:
        inf_temp += abs(num)
    POS_INF = inf_temp
    NEG_INF = -POS_INF

    def rand(self, player, board):
        return random.choice(self.legal_moves(player, board))


    def human(self): #works with parallel_client.py
        def strategy(player, board):
            print(self.read_board(board))
            print(core.PLAYERS[player] + ", choose a number: ")
            print("Legal moves: " + str(self.legal_moves(player, board)))
            spot = int(input())
            return spot

        return strategy

    #def human(self): #works with client.py
    #    def strategy(player, board):
    #        print(self.read_board(board))
    #        print(core.PLAYERS[player] + ", choose a number: ")
    #        print("Legal moves: " + str(self.legal_moves(player, board)))
    #        spot = int(input())
    #        return spot
    #    return strategy

    def eval(self, player, board):
        temp = 0
        for spot in self.squares():
            if board[spot] == player:
                temp += self.SQUARE_WEIGHTS[spot]
            elif board[spot] == self.opponent(player):
                 temp -= self.SQUARE_WEIGHTS[spot]
        return temp

    def final_value(self, player, board):
        diff = self.score(player, board)
        if diff < 0:
            return self.NEG_INF
        elif diff > 0:
            return self.POS_INF
        return diff

    def ab_search(self, player, board, lower, upper, depth):
        if depth == 0:
            return self.eval(player, board), None

        moves = self.legal_moves(player, board)
        if not moves:
            if not self.any_legal_move(self.opponent(player), board):
                return self.final_value(player, board), None
            return self.ab_search(self.opponent(player), board, upper*-1, lower*-1, depth - 1)[0]*-1, None
        best_move = moves[0]
        for move in moves:
            val = self.ab_search(self.opponent(player), board, upper*-1, -lower*-1, depth -1)[0]*-1
            if val > lower:
                lower = val
                best_move = move
        return lower, best_move

    def ab(self, depth): #helper method for ab_search
        def strategy(player, board):
            return self.ab_search(player, board, self.NEG_INF, self.POS_INF, depth)[1]
        return strategy

    def best_strategy(self, board, player, best_move, still_running): #works with parallel_client.py
        best_move.value = self.legal_moves(player, board)[0]
        while still_running.value > 0 and best_move.value < 1000:
            print(self.read_board(board))
            time.sleep(1)
            best_move.value = self.ab(4)(player, board)

    #def best_strategy(self, board, player, best_move, still_running): #works with client.py
    #    while still_running.value > 0 and best_move.value < 1000:
    #        time.sleep(1)
    #        best_move.value = self.ab(4)(player, board)
