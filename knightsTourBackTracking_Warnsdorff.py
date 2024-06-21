import sys

sys.setrecursionlimit(10 ** 6)  # Set the recursion limit to a large value

print("Printing 1 solution for a starting state that is optimized by Warnsdorff's rule ")


class KnightsTour:
    def __init__(self, n):  # initilize board , all squares to -1 as unvisited
        self.n = n
        self.board = [[-1] * n for _ in range(n)]
        self.moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        self.solPath = []

    def is_valid_move(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == -1

    def get_next_moves(self, x, y):
        next_moves = []
        for move in self.moves:
            next_x, next_y = x + move[0], y + move[1]
            if self.is_valid_move(next_x, next_y):
                count = 0
                for m in self.moves:
                    if self.is_valid_move(next_x + m[0], next_y + m[1]):
                        count += 1
                next_moves.append((next_x, next_y, count))
        return sorted(next_moves, key=lambda x: x[2])

    def solve(self, row, col):
        self.board[row][col] = 0
        self.solPath.append((row, col))
        if not self.solve_util(row, col, 1):
            print("No solution exists")
        else:
            self.print_solution()

    def solve_util(self, x, y, move_num):
        if move_num == self.n ** 2:  # board is full
            return True

        for next_x, next_y, _ in self.get_next_moves(x, y):
            self.board[next_x][next_y] = move_num
            self.solPath.append((next_x, next_y))
            if self.solve_util(next_x, next_y, move_num + 1):
                return True
            self.board[next_x][next_y] = -1
            self.solPath.pop()

        return False
        # end of solve_util function

    def print_solution(self):
        return self.solPath
