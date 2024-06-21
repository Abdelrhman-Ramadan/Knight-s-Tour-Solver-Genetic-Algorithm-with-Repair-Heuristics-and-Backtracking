# import matplotlib.pyplot as plt

# state = [
#     [0, 0, 0, 1, 1, 5, 5, 0],
#     [1, 2, 0, 4, 2, 5, 6, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 2, 3, 5, 0, 3, 6],
#     [0, 0, 0, 0, 0, 5, 1, 3],
#     [9, 0, 0, 0, 0, 0, 0, 0],
#     [3, 1, 0, 0, 2, 1, 2, 0]
# ]

# plt.imshow(state, cmap='viridis', interpolation='nearest')
# plt.colorbar()
# plt.show()



import threading
import matplotlib.pyplot as plt
import numpy as np

number_of_solutions = 0
TotalRuns = 0

def displayChessBoard(chessBoard):
    print("//////////////////////////////")
    global number_of_solutions
    number_of_solutions += 1
    print("Solution number:", number_of_solutions)
    #Printing every possible solution
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
  
    global number_of_solutions
    state = []
    solution_counts = []
    n = 5
    for row in range(n):
       for col in range(n): 
          chess_board = [[0 for _ in range(n)] for _ in range(n)]
          number_of_solutions = 0
          timeout_flag = threading.Event()
          timeout_flag.clear()  # Initially, the flag is not set

          knight_thread = threading.Thread(target = printKnightsTourSolutions, args=(chess_board, n, row, col, 1, timeout_flag))

          knight_thread.start()
          knight_thread.join(timeout=15)
          timeout_flag.set()
          print(number_of_solutions)

          state.append((row, col , number_of_solutions))
          print("number of solutions for state:( " +str(row)+' , '+str(col) +') = ' + str(number_of_solutions))
          print("#"*40)
          number_of_solutions=0

    solution_counts = [t[2] for t in state]
    x = np.arange(n)
    y = np.arange(n)
    grid = np.outer(x, y)  # Creating a grid using outer product of x and y
    m = 0  
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    for i in range(n):
      for j in range(n):
        plt.text( i , j , solution_counts[m] , ha='center', va='center', color='black')
        m +=1
    plt.title('KnightsTour Solutions found for n = ' +str(n)+' in 15 seconds')
    plt.colorbar()
    plt.show()

main()
