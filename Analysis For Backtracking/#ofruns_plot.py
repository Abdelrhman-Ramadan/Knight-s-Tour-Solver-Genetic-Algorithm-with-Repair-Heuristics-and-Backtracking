import threading
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

number_of_solutions = 0
TotalRuns = 0

def displayChessBoard(chessBoard):
    print("//////////////////////////////")
    global number_of_solutions
    number_of_solutions += 1
    print("Solution number:", number_of_solutions)
    print("Total runs:", TotalRuns)
    # Printing every possible solution
    for i in range(len(chessBoard)):
        for j in range(len(chessBoard)):
            print(chessBoard[i][j], end=" ")
        print()
  
    
# End of displayChessBoard function

# Row and column starting number = 0
def printKnightsTourSolutions(chessBoard, n, row, col, upcomingMove, timeout_flag):
    global TotalRuns
    TotalRuns += 1

    # Checking that passed row and column are valid
    if row < 0 or col < 0 or row >= n or col >= n or chessBoard[row][col] != 0:
        return

    if upcomingMove == n * n:
        chessBoard[row][col] = upcomingMove
        displayChessBoard(chessBoard)
        chessBoard[row][col] = 0
        return 

    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    chessBoard[row][col] = upcomingMove

    next_moves = []
    for i in range(8):
        next_x = row + move_x[i]
        next_y = col + move_y[i]
        if next_x >= 0 and next_x < n and next_y >= 0 and next_y < n and chessBoard[next_x][next_y] == 0:
            count = 0
            for j in range(8):
                if next_x + move_x[j] >= 0 and next_x + move_x[j] < n and next_y + move_y[j] >= 0 and next_y + move_y[j] < n and chessBoard[next_x + move_x[j]][next_y + move_y[j]] == 0:
                    count += 1
            next_moves.append((next_x, next_y, count))

    # Sort the next moves based on the number of accessible squares(counts) for this move
    next_moves.sort(key=lambda x: x[2])

    for move in next_moves:
        if not timeout_flag.is_set():
            printKnightsTourSolutions(chessBoard, n, move[0], move[1], upcomingMove + 1, timeout_flag)  # move[0] is the rows, move[1] is the columns
        else:
            break

    chessBoard[row][col] = 0

# End of printKnightsTourSolutions function

def main():
    
    row = int(input("Enter the starting row: "))
    col = int(input("Enter the starting column: "))      
    
    global TotalRuns
    global number_of_solutions
    n_values = []
    runs_count = []

    for n in range(4, 9):
        chess_board = [[0 for _ in range(n)] for _ in range(n)]
        number_of_solutions = 0 
        TotalRuns = 0
        timeout_flag = threading.Event()
        timeout_flag.clear()  # Initially, the flag is not set

        knight_thread = threading.Thread(target=printKnightsTourSolutions, args=(chess_board, n, row, col, 1, timeout_flag))

        knight_thread.start()
        knight_thread.join(timeout=15)
        timeout_flag.set()

        n_values.append(n)
        runs_count.append(TotalRuns)
        number_of_solutions = 0 
        TotalRuns=0
 
    plt.plot(n_values, runs_count, marker='o')
    plt.xlabel('Chessboard Size (n)')
    plt.ylabel('Total # of runs')
    plt.xticks(np.arange(4, 9, step=1)) 
    plt.yticks(runs_count)
    plt.gca().get_yaxis().set_major_formatter(ScalarFormatter(useMathText=True))
    plt.title('KnightsTour Runs in 15 seconds , Starting state: ' +str(row)+' , '+ str(col))
    plt.show()

main()