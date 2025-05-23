from board import Board

def heuristics_paws_on_board(board: Board, on_move: str) -> int:
    
    
    enemy = 'B' if on_move == 'W' else 'W'
    score = 0
    return sum(count == on_move for row in board.board for count in row) - sum(count == enemy for row in board.board for count in row)

def heuristics_central_vs_edges(board: Board, on_move: str) -> int:

    enemy = 'B' if on_move == 'W' else 'W'
    score = 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for n in range(board.n):
        for m in range(board.m):
            if n == 0 or n == board.n - 1 or m == 0 or m == board.m - 1:
                if board.board[n][m] == on_move:
                    score += 1

                    for dn, dm in directions:
                        adj_n, adj_m = n + dn, m + dm
                        if 0 <= adj_n < board.n and 0 <= adj_m < board.m:
                            if board.board[adj_n][adj_m] == enemy:
                                score += 1

                    if n == 0 and m == 0:
                        score += 3

            elif board.board[n][m] == enemy:
                score += 1

    return score

def heuristics_inaccessible_pawns(board: Board, on_move: str) -> int:


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
    
    