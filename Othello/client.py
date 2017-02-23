import os
import random
import signal
import time
from multiprocessing import Process, Value

import Othello_strategy as ai
import Othello_sub_core as core
from Othello_sub_core import *
#import OthelloStrategy as kzou
#############################################################
# client.py
# a simple othello client
# plays 2 strategies against each other and keeps score
# imports strategies from "Othello_strategy.py" as ai
# rest of functionality is stored in Othello_sub_core.py
#
# Robert Kim: January 2017
############################################################
strategies = ai.Strategy()
#B_STRATEGY = strategies.human()
#B_STRATEGY = kzou.mcts
B_STRATEGY = strategies.rand
#B_STRATEGY = strategies.best_strategy
# B_STRATEGY = ai.ab(2, ai.eval)
#W_STRATEGY = strategies.best_strategy
W_STRATEGY = strategies.ab(3)
# W_STRATEGY = ai.rand
ROUNDS = 1
SILENT = False


# see core.py for constants: MAX, MIN, TIE

def play(strategy_w, strategy_b, first=WHITE, silent=True):
    game = OthelloSubCore()
    board = game.initial_board()
    player = first
    current_strategy = {WHITE: strategy_w, BLACK: strategy_b}
    while player is not None:
        if(current_strategy[player] == strategies.best_strategy):
            move = get_move(board, player)
        else:
            move = current_strategy[player](player, board)
        if game.is_legal(move, player, board):
            board = game.make_move(move, player, board)
            print(game.read_board(board))
            print("Black: " + str(game.count(BLACK, board)))
            print("White: " + str(game.count(WHITE, board)))
            player = game.next_player(board, player)
        else:
            print(game.IllegalMoveError(player, move, board))

    if not (game.any_legal_move(WHITE, board)):
        if not (game.any_legal_move(BLACK, board)):
            if game.score(WHITE, board) > game.score(BLACK, board):
                return WHITE
            else:
                return BLACK


def main():
    """
    Plays ROUNDS othello games and keeps a count of
    wins/ties. Uses strategies defined as global constants above.
    Selects a random starting player
    """
    j = []
    start = time.time()
    for i in range(ROUNDS):
        try:
            game_result = play(W_STRATEGY, B_STRATEGY,
                               first=random.choice([WHITE, BLACK]),
                               silent=SILENT)
            j.append(game_result)
            # print("Winner: ", game_result)
        except OthelloSubCore.IllegalMoveError as e:
            print(e)
            j.append("FORFEIT")
    end = time.time()
    print("\nResults\n" + "%4s %6s" % (core.PLAYERS[WHITE], core.PLAYERS[BLACK]))
    print("-" * 12)
    print("%3i %6i" % (j.count(WHITE), j.count(BLACK)))
    run_time = end - start
    # print("Time: " + str(run_time))
    print("Game time: " + str(round(run_time / 60)) + " minutes and " + str(round((run_time % 60))) + " seconds")


time_limit = 3
time_extra = 2

def get_move(board, player):
    best_move = Value("i", 0)
    running = Value("i", 1)
    p = Process(target=strategies.best_strategy, args=(board, player, best_move, running))
    p.start()
    t1 = time.time()
    print("Starting move for " + core.PLAYERS[player])
    p.join(time_limit)
    if p.is_alive():
        print(str(time_limit) + " seconds elapsed...")
        time.sleep(time_extra)
        running.value = 0
        time.sleep(0.1)
        p.terminate()
        time.sleep(0.1)
        print(str(time_limit + time_extra) + " seconds elapsed...")
    if p.is_alive():
        print("Force killed.")
        os.kill(p.pid, signal.SIGKILL)
    time.time()
    return best_move.value


if __name__ == "__main__":
    main()
