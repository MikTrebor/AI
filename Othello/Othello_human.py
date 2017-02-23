import Othello_sub_core as core

class Strategy(core.OthelloSubCore):
    def best_strategy(self, board, player, best_move, still_running):
        while still_running.value > 0 and best_move.value < 1000:
            for num in self.legal_moves(player, board):
                best_move.value = num
