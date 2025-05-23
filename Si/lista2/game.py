import heuristics as h
from player import Player
from board import Board
from time import time
from copy import deepcopy


def play_simple_game(n,m,d, heuristics_player_one, heuristics_player_two, advanced, minimax):
    board = Board(n, m)
    player_one = Player(heuristics_player_one, d, 'B', deepcopy(board), advanced)
    player_two = Player(heuristics_player_two, d, 'W', deepcopy(board), advanced)
    rounds = 1

    visited_nodes = 0
    if advanced:
        move = player_one.make_random_move()
        player_two.make_move(move)
        board.make_move(move)
        move = player_two.make_random_move()
        player_one.make_move(move)
        board.make_move(move)
        rounds += 1

    while player_one.possible_move():

        # player_one.print_board()
        # print("Player 1 (B) turn")
        if minimax:
            _,move,tmp = player_one.alpha_beta_minmax(deepcopy(player_one.get_board()), d, -100, 100, True)
        else:
            _,move,tmp = player_one.minimax(deepcopy(player_one.get_board()), d, True)
        visited_nodes += tmp
        # print(move)
        player_one.board.make_move(move)
        player_two.board.make_move(move)

        # player_one.print_board()
        
        if not player_one.possible_move():
            print("Player 1 (B) wins!")
            break

        # print("Player 2 (W) turn")
        if minimax:
            _,move,tmp = player_two.alpha_beta_minmax(deepcopy(player_two.get_board()), d, -100, 100, True)
        else:
            _,move,tmp = player_two.minimax(deepcopy(player_two.get_board()), d, True)
        
        visited_nodes += tmp

        player_one.board.make_move(move)
        player_two.board.make_move(move)
        # print(move)
        
        if not player_one.possible_move():
            print("Player 2 (W) wins!")
            break
        rounds += 1

    player_one.print_board()
    print("Time taken: ", time() - timer)
    print("Rounds: ", rounds)
    print("Visited nodes: ", visited_nodes)


if __name__ == "__main__":
    d = 6 # depth

    n = 15 # number of rows
    m = 15 # number of columns
    
    timer = time()

    heuristics_player_one = [h.heuristics_central_vs_edges ,h.heuristics_safe_pawns, h.heuristics_pawns_moves]
    heuristics_player_two = [h.heuristics_inaccessible_pawns, h.heuristics_paws_on_board, h.heuristics_pawns_moves]

    play_simple_game(
        n=n, 
        m=m, 
        d=d, 
        heuristics_player_one=heuristics_player_one, 
        heuristics_player_two=heuristics_player_one, 
        advanced=False, 
        minimax=False
    )

    