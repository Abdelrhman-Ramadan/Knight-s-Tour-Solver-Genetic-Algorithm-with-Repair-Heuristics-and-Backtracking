import random
import sys

sys.setrecursionlimit(10 ** 6)


class KnightsTour_1:
    def __init__(self, n):
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

            # Sort the moves based on the number of next moves in ascending order
            next_moves.sort(key=lambda x: x[2])

        # Use Warnsdorff's rule to prioritize moves with the fewest possible next moves
        if len(next_moves) > 0:
            min_next_moves = next_moves[0][2]
            random_moves = [move for move in next_moves if move[2] == min_next_moves]
            if len(random_moves) > 0:
                random_l = self.Create_random_list(random_moves, len(random_moves))
                return random_l
        return next_moves

    def Create_random_list(self, next_moves, num_tuples):
        random_list = []
        for _ in range(num_tuples):
            random_tuple = random.choice(next_moves)  # No Duplicates
            random_list.append(random_tuple)

        return random_list

    def solve(self, x, y):
        start_x, start_y = x, y
        move_num = 0
        self.board[start_x][start_y] = move_num
        self.solPath.append((start_x, start_y))
        if self.solve_util(start_x, start_y, move_num + 1):
            self.print_solution()
        else:
            print("No solution exists")

    def solve_util(self, x, y, move_num):
        if move_num == self.n ** 2:
            return True

        for next_x, next_y, _ in self.get_next_moves(x, y):
            self.board[next_x][next_y] = move_num
            self.solPath.append((next_x, next_y))
            if self.solve_util(next_x, next_y, move_num + 1):
                return True
            self.board[next_x][next_y] = -1
            self.solPath.pop()

        return False

    def print_solution(self):
        return self.solPath
