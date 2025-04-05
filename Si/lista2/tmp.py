

class Board():
    def __init__(self, n:int,m:int):
        if(n<6):
            n = 5
        if(m<5):
            m = 6
        self.n: int = n
        self.m: int = m
        self.board : list[list[str]] = []

        self.create_board()

    def create_board(self) -> None:    
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
                    
            
if __name__ == "__main__":
    board = Board(6, 5)
    # board.set_board([[" "," "," ","B"," ","W"],
    #                 [" "," "," ","B"," "," "],
    #                 [" "," ","B"," "," ","W"],
    #                 ["B"," "," ","B"," "," "],
    #                 [" ","W","W"," "," ","W"]])

    board.print_board()
    print(board.possible_move())
    
        
