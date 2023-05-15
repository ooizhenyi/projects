import random
import time

# Define the board as a 9x9 grid of zeros
board = [[0 for x in range(9)] for y in range(9)]

# Define a function to check if a given number is allowed in a given position
def is_valid_move(board, row, col, num):
    # Check if the number is already in the same row or column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check if the number is already in the same 3x3 square
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3
    for i in range(square_row, square_row + 3):
        for j in range(square_col, square_col + 3):
            if board[i][j] == num:
                return False
    # If the number is allowed in this position
    return True

# Define a function to recursively fill in the board
def fill_board(board, row, col):
    # If we have filled in all cells, we are done
    if row == 9:
        return True
    # If we have filled in all cells in the current row, move to the next row
    if col == 9:
        return fill_board(board, row + 1, 0)
    # If the current cell is already filled in, move to the next cell
    if board[row][col] != 0:
        return fill_board(board, row, col + 1)
    # Display the board and ask the user for input, trying each input number recursively
    while True:
        print_board(board, time.time() - start_time)
        try:
            choice = input(f"Enter 'r' to choose row, 'c' to choose column, or 'v' to choose value: ")
            if choice == 'r':
                row = int(input("Enter the row number (1-9): ")) - 1
            elif choice == 'c':
                col = int(input("Enter the column number (1-9): ")) - 1
            elif choice == 'v':
                num = int(input("Enter a number between 1 and 9: "))
                if is_valid_move(board, row, col, num):
                    board[row][col] = num
                    if fill_board(board, row, col + 1):
                        return True
                    board[row][col] = 0
                else:
                    print("Invalid move. Please try again.")
            else:
                print("Invalid choice. Please enter 'r', 'c', or 'v'.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
    # If no number worked, backtrack to the previous cell
    return False

# Define a function to display the board
def print_board(board, elapsed_time):
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

# Fill the board with some random initial values
for row in range(9):
    for col in range(9):
        if random.random() < 0.5:
            num = random.randint(1, 9)
            if is_valid_move(board, row, col, num):
                board[row][col] = num

# Start the timer
start_time = time.time()

# Ask the user to input values for the remaining cells
if fill_board(board, 0, 0):
    # Display the final board and elapsed time
    print_board(board, time.time() - start_time)
    print("Congratulations! You completed the Sudoku puzzle.")
else:
    print("Sorry, the puzzle is incomplete.")