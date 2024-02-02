def choose_position():
    indexes = set([0, 1, 2])
    done = False

    while not done:
        a = input("Which row [0/1/2]? ")
        try:
            a = int(a)
        except ValueError:
            print("Invalid input. Please pick a valid row.")
            continue
            
        if a not in indexes:
            print("Please pick a valid row.")
            continue

        b = input("Which column [0/1/2]? ")
        try:
            b = int(b)
        except ValueError:
            print("Invalid input. Please pick a valid column.")
            continue
        
        if b not in indexes:
            print("Please pick a valid column")
            continue
        done = True
    print(type(a))
    return tuple([a,b])

class Board:
    def __init__(self) -> None:
        self.board = [[0 for i in range(3)] for i in range(3)]
        self.winner = 0
        self.symbols = [" ", "x", "o"]
        self.finished = False
        self.won = False

    def move(self, position, player):
        if type(position) is not tuple:
            raise TypeError("Position is a tuple")
        if len(position) != 2:
            raise ValueError("Board has only two coordinates")
        if self.board[position[0]][position[1]] != 0:
            raise ValueError("Position already occupied")
        
        self.board[position[0]][position[1]] += player

    def is_won(self):
        if self.won:
            return True
        for i in range(3):
            if abs(sum(self.board[i])) == 3:
                self.winner = self.board[i][0]
                self.won = True
                return True
            if abs(sum([self.board[j][i] for j in range(3)])) == 3:
                self.winner = self.board[0][i]
                self.won = True
                return True
        if abs(sum([self.board[i][i] for i in range(3)])) ==3 or \
           abs(sum([self.board[i][2-i] for i in range(3)])) ==3:
            self.winner = self.board[1][1]
            self.won = True
            return True
        return False
    
    def is_finished(self):
        if self.finished:
            return True
        for i in range(3):
            if 0 in self.board[1]:
                return False

        self.finished = True
        return True

    # def plot(self, one_line=False):
    #     rows = [[f"{self.symbols[i]}" for i in j] for j in self.board]
    #     if one_line:
    #         return [f"{row[0]}|{row[1]}|{row[2]}" for row in rows]
        
    #     for row in rows:
    #         print(f"{row[0]}|{row[1]}|{row[2]}")

class Game:
    def __init__(self) -> None:
        self.game = [[Board() for i in range(3)] for i in range(3)]
        self.moves = []
        self.free_move = True
        self.winner = 0

    def update(self, board, position, player):
        active = self.game[board[0]][board[1]]
        active.move(position, player)
        self.moves.append([board, position, player])
        active.is_won()
        active.is_finished()
        self.free_move = self.game[position[0]][position[1]].finished
        self.is_won()
        self.is_finished()
        return 

    def move(self):
        if not self.free_move:
            board = self.moves[-1][1]
            player = - self.moves[-1][2]
        
        else:
            if self.moves:
                player = - self.moves[-1][2]
            else:
                player = 1

            print("Choose the board on which to play!")
            while self.free_move:
                board = choose_position()
                if self.game[board[0]][board[1]].finished:
                    print("Board is already full! Please choose a different one.")
                    continue
                self.free_move = False
        
        print(f"Choose your move (active board: row {board[0]}, col {board[1]}).")
        position = choose_position()
        self.update(board, position, player)
        return

    def is_won(self):
        if self.winner:
            return True
        for i in range(3):
            if abs(sum([self.game[i][j].winner for j in range(3)]))== 3:
                self.winner = self.game[i][0].winner
                return True
            if abs(sum([self.game[j][i].winner for j in range(3)])) == 3:
                self.winner = self.game[0][i].winner
                return True
            
        if abs(sum([self.game[i][i].winner for i in range(3)])) ==3 or \
           abs(sum([self.game[i][2-i].winner for i in range(3)])) ==3:
            self.winner = self.game[1][1].winner
            return True
        return False

    def is_finished(self):
        if self.winner:
            return True
        return all([all([self.game[i][j].finished for j in range(3)]) for i in range(3)])

    def plot(self, show=True):
        long_rows = []
        for i in range(3):
            for k in range(3):
                rows = []
                for j in range(3):
                    active = self.game[i][j]
                    row = "|".join([f"{active.symbols[player]}" for player in active.board[k]])
                    rows.append(row)
                long_row = " | ".join(rows)
                long_rows.append(long_row)
            long_rows.append("-"*len(long_rows[0]))

        res = "\n".join(long_rows[:-1])
        if show:
            print(res)
        return res
    

if __name__=="__main__":
    instance = Game()
    symb = [" ", "x", "o"]

    while not instance.is_finished():
        instance.move()
        instance.plot()

    
    if instance.winner:
        print(f"Player {symb[instance.winner]} won!")
    else:
        print("It's a tie!")