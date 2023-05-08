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
    # Try each number from 1 to 9 in the current cell, recursively filling in the rest of the board
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if fill_board(board, row, col + 1):
                return True
            board[row][col] = 0
    # If no number worked, backtrack to the previous cell
    return False

# Fill in the board recursively
fill_board(board, 0, 0)

# Display the board
for row in board:
    print(row)
