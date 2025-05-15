from board import Board
from random import choice
from heuristics import heuristics_endgame
class Player():
    def __init__(self,heuristics: list, depth: int, player: str, advanced: bool = False) -> None:
        self.heuristics = heuristics 
        self.selected_heuristic = heuristics[0]
        self.depth = depth if depth > 0 and depth <=10 else 3 
        self.player = player
        self.enemy = 'B' if player == 'W' else 'W'
        self.cached_moves = {}
        self.advanced = advanced
        self.end_game_heuristics = heuristics_endgame

    def calculate_moves(self, board: Board, on_move: str) -> list[tuple[int,int]]:
        moves = []
        for n in range(board.n):
            for m in range(board.m):
                if board.board[n][m] == on_move:
                    if n-1 >= 0 and board.board[n-1][m] == ' ':
                        moves.append((n-1, m))
                    if m+1 < board.m and board.board[n][m+1] == ' ':
                        moves.append((n, m+1))
                    if m-1 >= 0 and board.board[n][m-1] == ' ':
                        moves.append((n, m-1))
                    if n+1 < board.n and board.board[n+1][m] == ' ':
                        moves.append((n+1, m))
        return moves
        
    # TODO think about chaching moves
    def minimax(self, board: Board, depth: int, maximizing_player: bool) -> tuple[int, tuple[int,int]]:
        if depth == 0 or not board.possible_move():
            if self.advanced:
                return self.evaluate(board, maximizing_player), None
            return self.selected_heuristic(board, self.player if maximizing_player else self.enemy), None

        if self.player == 'W':
            maximizing_moves = board.get_all_moves_white()
            minimizing_moves = board.get_all_moves_black()
        else:
            maximizing_moves = board.get_all_moves_black()
            minimizing_moves = board.get_all_moves_white()
            
        if maximizing_player:
            max_eval = float('-inf')


            best_move = None
            best_moves_advanced = {}
            # TODO draw random move if there are multiple moves

            for move in maximizing_moves:
                board.make_move(move)
                eval = self.minimax(board, depth - 1, False)[0]
                board.undo_move()

                if eval >= max_eval:
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                        best_moves_advanced = {eval: [move]}
                    elif eval == max_eval:
                        best_moves_advanced[eval].append(move)

            if self.advanced:
                if max_eval in best_moves_advanced:
                    best_move = choice(best_moves_advanced[max_eval])
                else:
                    best_move = choice(maximizing_moves)
                    
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            best_move = None
            for move in minimizing_moves:
                board.make_move(move)
                eval = self.minimax(board, depth - 1, True)[0]
                board.undo_move()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
        
    def evaluate(self, board: Board,maximizing_player: bool) -> int:
        score = 0
        for heuristic in self.heuristics:
            score += heuristic(board, self.player if maximizing_player else self.enemy)
            if self.board.pawns_with_moves() <= (self.board.n * self.board.m) // 3:
                score += self.end_game_heuristics(board, self.player if maximizing_player else self.enemy)
        return score
    
    def alpha_beta_minmax(self, board: Board, depth, alpha, beta, maximizing_player):
        if depth == 0 or not board.possible_move():
            if self.advanced:
                return self.evaluate(board, maximizing_player), None
            return self.selected_heuristic(board, self.player if maximizing_player else self.enemy), None

        if self.player == 'W':
            maximizing_moves = board.get_all_moves_white()
            minimizing_moves = board.get_all_moves_black()
        else:
            maximizing_moves = board.get_all_moves_black()
            minimizing_moves = board.get_all_moves_white()

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            best_moves_advanced = {}

            for move in maximizing_moves:
                board.make_move(move)
                eval = self.alpha_beta_minmax(board, depth - 1, alpha, beta, False)[0]
                board.undo_move()

                if eval >= max_eval:
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                        best_moves_advanced = {eval: [move]}
                    elif eval == max_eval:
                        best_moves_advanced.setdefault(eval, []).append(move)

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            if self.advanced and max_eval in best_moves_advanced:
                best_move = choice(best_moves_advanced[max_eval])
            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_moves_advanced = {}

            for move in minimizing_moves:
                board.make_move(move)
                eval = self.alpha_beta_minmax(board, depth - 1, alpha, beta, True)[0]
                board.undo_move()

                if eval <= min_eval:
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                        best_moves_advanced = {eval: [move]}
                    elif eval == min_eval:
                        best_moves_advanced.setdefault(eval, []).append(move)

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            if self.advanced and min_eval in best_moves_advanced:
                best_move = choice(best_moves_advanced[min_eval])
            return min_eval, best_move
        
    def move_alfa_beta(self, board: Board) -> tuple[int, int]:
        _, move = self.alpha_beta_minmax(board, self.depth, float('-inf'), float('inf'), True)
        return move
    
    def move_mini_max(self, board: Board) -> tuple[int, int]:
        _, move = self.minimax(board, self.depth, True)
        return move
    
    def set_board(self, board: Board) -> None:
        self.board = board
        self.cached_moves = {}
