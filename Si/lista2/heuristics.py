from board import Board

def heuristics_paws_on_board(board: Board, on_move: str) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic is computed as the difference between the number of pieces of the player and the number of pieces of the opponent.
    """
    
    enemy = 'B' if on_move == 'W' else 'W'
    score = 0
    return sum(count == on_move for row in board.board for count in row) - sum(count == enemy for row in board.board for count in row)
    # for n in range(board.n):
    #     for m in range(board.m):
    #         if board.board[n][m] == on_move:
    #             score += 1
    #         elif board.board[n][m] == enemy:
    #             score -= 1
    #             # punish for enemy pieces around
    #             # if n-1 >= 0 and board.board[n-1][m] == enemy:
    #             #     score -= 1
    #             # if m+1 < board.m and board.board[n][m+1] == enemy:
    #             #     score -= 1
    #             # if m-1 >= 0 and board.board[n][m-1] == enemy:
    #             #     score -= 1
    #             # if n+1 < board.n and board.board[n+1][m] == enemy:
    #             #     score -= 1
    # return score

def heuristics_central_vs_edges(board: Board, on_move: str) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic base on the position of the pieces on the board.
    """

    enemy = 'B' if on_move == 'W' else 'W'
    score = 0

    for n in range(board.n):
        for m in range(board.m):
            if n == 0 or n == board.n-1 or m == 0 or m == board.m-1:
                if n == 0 and m == 0:
                    if board.board[n][m] == on_move:
                        score += 2 

                if board.board[n][m] == on_move:
                    score += 1

                    # extra points for corners
                    # if n == 0:
                    #     if m == 0:
                    #         score += 1
                    #     elif m == board.m-1:
                    #         score += 1
                    # if n == board.n-1:
                    #     if m == 0:
                    #         score += 1
                    #     elif m == board.m-1:
                    #         score += 1

                # punisch for enemy pieces on the edges
                # elif board.board[n][m] == enemy:
                #     score -= 1
    return score

def heuristics_inaccessible_pawns(board: Board, on_move: str) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic is calculated based on the number of pawns that are not accessible to the enemy.
    """

    enemy = 'B' if on_move == 'W' else 'W'
    score = 0

    for n in range(board.n):
        for m in range(board.m):
            if board.board[n][m] == on_move:
                tmp_score = 1
                if n-1 >= 0 and board.board[n-1][m] == enemy:
                    tmp_score = 0
                if m+1 < board.m and board.board[n][m+1] == enemy:
                    tmp_score = 0
                if m-1 >= 0 and board.board[n][m-1] == enemy:
                    tmp_score = 0
                if n+1 < board.n and board.board[n+1][m] == enemy:
                    tmp_score = 0
                
                score += tmp_score
    return score

def heuristics_safe_pawns(board: Board, on_move: str) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic is calculated based on the number of pawns that are not accessible to the enemy.
    """
    enemy = 'B' if on_move == 'W' else 'W'
    score = 0

    for n in range(board.n):
        for m in range(board.m):
            if board.board[n][m] == on_move:
                tmp_score = 1
                if n-1 >= 0 and board.board[n-1][m] != enemy:
                    tmp_score += 1
                if m+1 < board.m and board.board[n][m+1]  != enemy:
                    tmp_score += 1
                if m-1 >= 0 and board.board[n][m-1]  != enemy:
                    tmp_score += 1
                if n+1 < board.n and board.board[n+1][m]  != enemy:
                    tmp_score += 1
                
                score += tmp_score
    return score

def heuristics_pawns_moves(board: Board, on_move: str) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic is computed based on the number of possible moves for the player.
    """
    enemy = 'B' if on_move == 'W' else 'W'
    score = 0

    for n in range(board.n):
        for m in range(board.m):
            if board.board[n][m] == on_move:
                tmp_score = 0
                if n-1 >= 0 and board.board[n-1][m] == enemy:
                    tmp_score += 1
                if m+1 < board.m and board.board[n][m+1] == enemy:
                    tmp_score += 1
                if m-1 >= 0 and board.board[n][m-1] == enemy:
                    tmp_score += 1
                if n+1 < board.n and board.board[n+1][m] == enemy:
                    tmp_score += 1
                
                score += tmp_score
    return score

def heuristics_endgame(board: Board, on_move: str) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic is computed based on the number of possible moves for the player.
    """
    enemy = 'B' if on_move == 'W' else 'W'
    score = 0

    for n in range(board.n):
        for m in range(board.m):
            if board.board[n][m] == on_move:
                enemy_points = 0
                ally_points = 0

                if n-1 >= 0 and board.board[n-1][m] == enemy:
                    tmp = more_allays_or_enemies(board, (n-1, m))
                    if tmp > 0:
                        ally_points += 3
                    else:
                        enemy_points += 1

                if m+1 < board.m and board.board[n][m+1] == enemy:
                    tmp = more_allays_or_enemies(board, (n, m+1))
                    if tmp > 0:
                        ally_points += 3
                    else:
                        enemy_points += 1

                if m-1 >= 0 and board.board[n][m-1] == enemy:
                    tmp = more_allays_or_enemies(board, (n, m-1))
                    if tmp > 0:
                        ally_points += 3
                    else:
                        enemy_points += 1

                if n+1 < board.n and board.board[n+1][m] == enemy:
                    tmp = more_allays_or_enemies(board, (n+1, m))
                    if tmp > 0:
                        ally_points += 3
                    else:
                        enemy_points += 1
                
                score += ally_points - enemy_points
    return score

def more_allays_or_enemies(board: Board,position: tuple[int,int]) -> int:
    """
    Heuristic function to evaluate the board state for the given player.
    The heuristic is computed based on the number of possible moves for the player.
    """
    enemy = board.board[position[0]][position[1]]
    on_move = 'B' if enemy == 'W' else 'W'

    enemy_pawns = 0
    ally_pawns = 0

    n, m = position

    if n-1 >= 0:
        if board.board[n-1][m] == enemy:
            enemy_pawns += 1
        elif board.board[n-1][m] == on_move:
            ally_pawns += 1

    if m+1 < board.m:
        if board.board[n][m+1] == enemy:
            enemy_pawns += 1
        elif board.board[n][m+1] == on_move:
            ally_pawns += 1

    if m-1 >= 0:
        if board.board[n][m-1] == enemy:
            enemy_pawns += 1
        elif board.board[n][m-1] == on_move:
            ally_pawns += 1

    if n+1 < board.n:
        if board.board[n+1][m] == enemy:
            enemy_pawns += 1
        elif board.board[n+1][m] == on_move:
            ally_pawns += 1
    
    return ally_pawns - enemy_pawns
    
    