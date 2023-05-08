import random

# Create a blank 9x9 grid
grid = [[0 for x in range(9)] for y in range(9)]

# Populate the grid with valid numbers
def fill_grid(grid):
    for row in range(9):
        for col in range(9):
            while True:
                num = random.randint(1,9)
                if is_valid(grid, row, col, num):
                    grid[row][col] = num
                    break

# Check if a given move is valid
def is_valid(grid, row, col, num):
    # Check if the number exists in the same row
    for i in range(9):
        if grid[row][i] == num:
            return False
    # Check if the number exists in the same column
    for i in range(9):
        if grid[i][col] == num:
            return False
    # Check if the number exists in the same 3x3 sub-grid
    sub_row = (row // 3) * 3
    sub_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[sub_row+i][sub_col+j] == num:
                return False
    # If the number doesn't violate any of the rules, it's valid
    return True

# Print the Sudoku board
def print_board(grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")

# Prompt the user for input and validate it
def prompt_user(grid):
    while True:
        row = int(input("Enter row (1-9): "))
        col = int(input("Enter column (1-9): "))
        val = int(input("Enter value (1-9): "))
        if row not in range(1,10) or col not in range(1,10) or val not in range(1,10):
            print("Invalid input, please try again")
            continue
        elif not is_valid(grid, row-1, col-1, val):
            print("Invalid move, please try again")
            continue
        else:
            grid[row-1][col-1] = val
            print_board(grid)
            break

# Main game loop
def play_game():
    fill_grid(grid)
    print_board(grid)
    while True:
        if all([all(row) for row in grid]):
            if is_sudoku_solved(grid):
                print("Congratulations, you solved the Sudoku puzzle!")
            else:
                print("Sorry, the solution you entered is incorrect.")
            break
        prompt_user(grid)

# Check if the Sudoku board is solved
def is_sudoku_solved(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return False
            if not is_valid(grid, i, j, grid[i][j]):
                return False
    return True

# Start the game
play_game()
