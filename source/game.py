import random


class Board:
    size = 4
    max_space = 4

    def __init__(self):
        self._board = [[0] * self.size for _ in range(self.size)]
        self.generate_random(True)
        self.generate_random(True)
        self._is_winner = False

    def display(self):
        for row in range(self.size):
            cur_row = ''
            for col in range(self.size):
                if self._board[row][col] == 0:
                    cur_row += ' ' * (self.max_space - 1) + '.' + ' '
                else:
                    num = self._board[row][col]
                    cur_row += ' ' * (self.max_space - len(str(num))) + str(num) + ' '
            print(cur_row)

    def shift_left(self, row):
        for _ in range(self.size - 1):
            for col in range(self.size - 1, 0, -1):
                if row[col - 1] == 0:
                    row[col - 1] = row[col]
                    row[col] = 0
        return row

    def move_left(self, row):
        row = self.shift_left(row)
        for col in range(self.size - 1):
            if row[col] == row[col + 1]:
                row[col] *= 2
                row[col + 1] = 0
                if row[col] == 2048:
                    self._is_winner = True
        return self.shift_left(row)

    def move_right(self, row):
        return self.move_left(row[::-1])[::-1]

    def transpose(self):
        board = [[0] * self.size for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                board[row][col] = self._board[col][row]
        self._board = board

    def merge_up(self):
        self.transpose()
        for row in range(self.size):
            self._board[row] = self.move_left(self._board[row])
        self.transpose()

    def merge_down(self):
        self.transpose()
        for row in range(self.size):
            self._board[row] = self.move_right(self._board[row])
        self.transpose()

    def merge_left(self):
        for row in range(self.size):
            self._board[row] = self.move_left(self._board[row])

    def merge_right(self):
        for row in range(self.size):
            self._board[row] = self.move_right(self._board[row])

    def empty_space(self):
        return [(row, col) for col in range(self.size) for row in range(self.size) if self._board[row][col] == 0]

    def generate_random(self, only_tows=False):
        spaces = self.empty_space()
        if spaces:
            space = random.choice(self.empty_space())
            tows = [2] * 10
            if not only_tows:
                fours = [4] * 6
                numbers = tows + fours
            else:
                numbers = tows
            self._board[space[0]][space[1]] = random.choice(numbers)
            return False
        return True

    def play(self):
        self.display()
        while not self._is_winner:
            direction = int(input('Enter Direction: '))
            self.move(direction)
            if self.generate_random():
                print('You lost the game')
                break
            self.display()
        if self._is_winner:
            print('Congratulations')

    def move(self, direction):
        if direction == 0:
            self.merge_left()
        elif direction == 1:
            self.merge_right()
        elif direction == 2:
            self.merge_up()
        elif direction == 3:
            self.merge_down()
        else:
            print('Invalid Direction')


if __name__ == "__main__":
    Board().play()
