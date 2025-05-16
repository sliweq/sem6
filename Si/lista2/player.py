from board import Board
from random import choice, random
from heuristics import heuristics_endgame


class Player():
    def __init__(self,heuristics: list, depth: int, player: str, board:Board, advanced: bool = False) -> None:
        self.heuristics = heuristics 
        self.selected_heuristic = heuristics[0]
        self.depth = depth if depth > 0 and depth <=10 else 3 
        self.player = player
        self.enemy = 'B' if player == 'W' else 'W'
        self.advanced = advanced
        self.end_game_heuristics = heuristics_endgame
        self.board = board

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
        
    def minimax(self, board: Board, depth: int, maximizing_player: bool, visited_notes:int = 0) -> tuple[int, tuple[int,int], int]:
        if depth == 0 or not board.possible_move():
            if self.advanced:
                return self.evaluate(board, maximizing_player), None, visited_notes
            return self.selected_heuristic(board, self.player if maximizing_player else self.enemy), None, visited_notes
        
        visited_notes += 1

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

            for move in maximizing_moves:
                board.make_move(move)
                eval,_,nodes = self.minimax(board, depth - 1, False, visited_notes)
                board.undo_move()
                visited_notes += nodes
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

            if self.advanced and  random() < 0.05:
                best_move = choice(maximizing_moves)
                
            return max_eval, best_move, visited_notes
        
        else:
            min_eval = float('inf')
            best_move = None
            for move in minimizing_moves:
                board.make_move(move)
                eval,_,nodes = self.minimax(board, depth - 1, True, visited_notes)
                visited_notes += nodes
                board.undo_move()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

            if self.advanced and random() < 0.05:
                best_move = choice(maximizing_moves)

            return min_eval, best_move, visited_notes
        
    def evaluate(self, board: Board,maximizing_player: bool) -> int:
        score = 0
        score = (
            1 * self.heuristics[0](board, self.player if maximizing_player else self.enemy) +
            1 * self.heuristics[1](board, self.player if maximizing_player else self.enemy) +
            self.heuristics[2](board, self.player if maximizing_player else self.enemy) 
        )
        if self.advanced and self.board.pawns_with_moves() <= (self.board.n * self.board.m) // 3:
            score += self.end_game_heuristics(board, self.player if maximizing_player else self.enemy)

        return score
    
    def alpha_beta_minmax(self, board: Board, depth, alpha, beta, maximizing_player, visited_notes:int = 0) -> tuple[int, tuple[int,int], int]:
        if depth == 0 or not board.possible_move():
            if self.advanced:
                return self.evaluate(board, maximizing_player), None, visited_notes
            return self.selected_heuristic(board, self.player if maximizing_player else self.enemy), None, visited_notes
        
        visited_notes += 1

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
                eval,_,nodes = self.alpha_beta_minmax(board, depth - 1, alpha, beta, False, visited_notes)
                visited_notes += nodes
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
            
            if self.advanced and random() < 0.05:
                best_move = choice(maximizing_moves)

            return max_eval, best_move, visited_notes

        else:
            min_eval = float('inf')
            best_moves_advanced = {}

            for move in minimizing_moves:
                board.make_move(move)
                eval,_,nodes = self.alpha_beta_minmax(board, depth - 1, alpha, beta, True)
                visited_notes += nodes
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

            if self.advanced and random() < 0.05:
                best_move = choice(maximizing_moves)

            return min_eval, best_move, visited_notes
        
    def move_alfa_beta(self, board: Board) -> tuple[int, int]:
        _, move = self.alpha_beta_minmax(board, self.depth, float('-inf'), float('inf'), True)
        return move
    
    def move_mini_max(self, board: Board) -> tuple[int, int]:
        _, move = self.minimax(board, self.depth, True)
        return move
    
    def set_board(self, board: Board) -> None:
        self.board = board
        self.cached_moves = {}

    def make_move(self, move: tuple[int,int]) -> bool:
        return self.board.make_move(move)
    
    def possible_move(self) -> bool:
        return self.board.possible_move()
    
    def print_board(self) -> None:
        self.board.print_board()    

    def get_board(self) -> Board:
        return self.board
    
    def make_random_move(self) -> tuple[int,int] | None:
        moves = self.board.get_all_moves_white() if self.player == 'W' else self.board.get_all_moves_black()
        move = choice(moves) if moves else None
        if move:
            self.board.make_move(move)
            return move
        else:
            print("No possible moves")
            return None
        