

class Board():
    def __init__(self, n:int,m:int):
        if(n<6):
            n = 5
        if(m<5):
            m = 6
        self.n: int = n
        self.m: int = m
        self.board : list[list[str]] = []

        self._create_board()
        self.moves = 0
        self.last_move = None


    def _create_board(self) -> None:    
        for n in range(self.n):
            self.board.append([])
            for m in range(self.m):
                if((n+m) % 2 == 0):
                    self.board[n].append('B')
                else:
                    self.board[n].append('W')

        self.board.reverse()
        

    def print_board(self) -> None:
        for n in range(self.n):
            for m in range(self.m):
                print(self.board[n][m], end = ' ')
            print()


    def set_board(self, board_input: list[list[str]]) -> None:
        if len(board_input) != self.n or len(board_input[0]) != self.m:
            raise ValueError("Input board dimensions do not match the initialized board dimensions.")
        self.board = board_input

    def get_board(self) -> list[list[str]]:
        return self.board
    
    def possible_move(self) -> bool:
        for n in range(self.n):
            for m in range(self.m):
                if self.board[n][m] == ' ':
                    continue
                else:
                    if self.check_move(n, m, self.board[n][m]):
                        return True
        return False

    def check_move(self,x:int,y:int,on_move:str) -> bool:
        if x>self.m or y>self.n:
            return False
        
        if on_move == 'W':
            enemy = 'B'
        elif on_move == 'B':
            enemy = 'W'
        else:
            raise ValueError("Invalid move type. Expected 'W' or 'B'.")
        
        if self.board[x][y] == on_move:
            if x-1>=0:
                if self.board[x-1][y] == enemy:
                    return True
            if y+1 < self.m:
                if self.board[x][y+1] == enemy:
                    return True
            if y-1 >= 0:
                if self.board[x][y-1] == enemy:
                    return True
            if x+1 < self.n:
                return self.board[x+1][y] == enemy
        
        return False
    
    def check_move_black(self) -> bool:
        for n in range(self.n):
            for m in range(self.m):
                if self.board[n][m] == 'B':
                    if self.check_move(n, m, 'B'):
                        return True
        return False
    
    def check_move_white(self) -> bool:
        for n in range(self.n):
            for m in range(self.m):
                if self.board[n][m] == 'W':
                    if self.check_move(n, m, 'W'):
                        return True
        return False
    
    def get_all_moves_black(self) -> list[tuple[tuple[int,int]]]:
        return self._get_all_possible_moves('B')
    
    def get_all_moves_white(self) -> list[tuple[tuple[int,int]]]:
        return self._get_all_possible_moves('W')

    def _get_all_possible_moves(self, on_move:str) -> list[tuple[tuple[int,int]]]:
        moves = []
        for n in range(self.n):
            for m in range(self.m):
                if self.board[n][m] == on_move:
                    enemy = 'B' if on_move == 'W' else 'W'

                    if n-1 >= 0 and self.board[n-1][m] == enemy:
                        moves.append(((n,m),(n-1, m)))
                    if m+1 < self.m and self.board[n][m+1] == enemy:
                        moves.append(((n,m),(n, m+1)))
                    if m-1 >= 0 and self.board[n][m-1] == enemy:
                        moves.append(((n,m),(n, m-1)))
                    if n+1 < self.n and self.board[n+1][m] == enemy:
                        moves.append(((n,m),(n+1, m)))
        return moves     

    def make_move(self, move: tuple[tuple[int,int]]) -> bool:
        start_move, end_move = move
        start_x, start_y = start_move
        end_x, end_y = end_move
        
        
        if self.board[start_x][start_y] == ' ':
            return False
        if self.board[end_x][end_y] == ' ':
            return False
        
        if self.check_move(start_x, start_y, self.board[start_x][start_y]):
            self.board[end_x][end_y] = self.board[start_x][start_y]
            self.board[start_x][start_y] = ' '
            self.moves += 1
            self.last_move = move
            return True

        return False

    def undo_move(self) -> bool:
        if self.last_move is None:
            return False

        start_move, end_move = self.last_move
        start_x, start_y = start_move
        end_x, end_y = end_move

        enemy = 'B' if self.board[end_x][end_y] == 'W' else 'W'
        if self.board[end_x][end_y] != enemy:
            return False

        self.board[start_x][start_y] = self.board[end_x][end_y]
        self.board[end_x][end_y] = enemy
        self.moves -= 1
        self.last_move = None
        return True

    def pawns_with_moves(self) -> int:
        count = 0
        for n in range(self.n):
            for m in range(self.m):
                    if self.check_move(n, m, 'W') or self.check_move(n, m, 'B') :
                        count += 1
        return count
    
            
if __name__ == "__main__":
    board = Board(6, 5)
    # board.set_board([[" "," "," ","B"," ","W"],
    #                 [" "," "," ","B"," "," "],
    #                 [" "," ","B"," "," ","W"],
    #                 ["B"," "," ","B"," "," "],
    #                 [" ","W","W"," "," ","W"]])

    board.print_board()
    print(board.possible_move())
    
        
