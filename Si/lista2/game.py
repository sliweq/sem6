import heuristics as h
from player import Player
from board import Board
from time import time
from copy import deepcopy



if __name__ == "__main__":
    
    d = 2 # depth

    n = 6 # number of rows
    m = 5 # number of columns
    
    timer = time()

    heuristics_player_one = [h.heuristics_central_vs_edges ,h.heuristics_safe_pawns, h.heuristics_pawns_moves]
    heuristics_player_two = [h.heuristics_paws_on_board, h.heuristics_inaccessible_pawns, h.heuristics_pawns_moves]

    board = Board(n, m)
    
    while board.possible_move():
        board.print_board()
        print("Player 1 (B) turn")
        player_one = Player(heuristics_player_one, d, 'B', True)
        # move = player_one.minimax(deepcopy(board), d, True)[1]
        move = player_one.alpha_beta_minmax(deepcopy(board), d, float('-inf'), float('inf'), True)[1]
        print(move)
        print(board.make_move(move))
        board.print_board()
        
        if not board.possible_move():
            print("Player 1 (B) wins!")
            break

        print("Player 2 (W) turn")
        player_two = Player(heuristics_player_one, d, 'W', True)
        # move = player_two.minimax(deepcopy(board), d, True)[1]
        move = player_two.alpha_beta_minmax(deepcopy(board), d, float('-inf'), float('inf'), True)[1]
        print(board.make_move(move))
        if not board.possible_move():
            print("Player 2 (W) wins!")
            break

    print(board)
    print("Time taken: ", time() - timer)

    