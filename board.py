
class Board:
    def __init__(self) -> None:
        self.board = [[0 for i in range(3)] for i in range(3)]
        self.next_move = 1
        self.winner = 0
        self.symbles = [" ", "x", "o"]
        self.finished = False

    def move(self, position):
        if type(position) is not tuple:
            raise TypeError("Position is a tuple")
        if len(position) != 2:
            raise ValueError("Board has only two coordinates")
        if self.board[position[0]][position[1]] != 0:
            raise ValueError("Position already occupied")
        
        self.board[position[0]][position[1]] += self.next_move

        self.next_move = -self.next_move
    
    
    def is_finished(self):
        if self.finished:
            return True
        for i in range(3):
            if abs(sum(self.board[i])) == 3:
                self.winner = self.board[i][0]
                self.finished = True
                return True
            if abs(sum([self.board[j][i] for j in range(3)])) == 3:
                self.winner = self.board[0][i]
                self.finished = True
                return True
        if abs(sum([self.board[i][i] for i in range(3)])) ==3 or \
           abs(sum([self.board[i][2-i] for i in range(3)])) ==3:
            self.winner = self.board[1][1]
            self.finished = True
            return True
        return False

    def plot(self):
        rows = [[f"{self.symbles[i]}" for i in j] for j in self.board]
        for row in rows:
            print(f"{row[0]}|{row[1]}|{row[2]}")
    
if __name__=="__main__":
    print("Starting the game")
    instance=Board()
    instance.plot()
    while not instance.finished:
        a = int(input("Which row [0/1/2]? "))
        b = int(input("Which column [0/1/2]? "))
        position = tuple([a,b])
        instance.move(position)
        instance.is_finished()
        instance.plot()
    
    print(f"Player {instance.symbles[instance.winner]} won!")