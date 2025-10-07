import numpy as np
import math
import random

# -------------------------------
# Game Setup
# -------------------------------
ROWS = 6
COLS = 7
PLAYER = 1       # Human player
AI = 2           # Computer
EMPTY = 0
WINDOW_LENGTH = 4

# -------------------------------
# Helper Functions
# -------------------------------
def create_board():
    """Initialize the Connect 4 board."""
    return np.zeros((ROWS, COLS), dtype=int)

def is_valid_location(board, col):
    """Check if a column is not full."""
    return board[ROWS - 1][col] == 0

def get_available_moves(board):
    """Return list of columns that are available for a move."""
    return [col for col in range(COLS) if is_valid_location(board, col)]

def get_next_open_row(board, col):
    """Return the next available row in the chosen column."""
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def make_move(board, col, piece):
    """Drop the piece into the board."""
    row = get_next_open_row(board, col)
    board[row][col] = piece

def undo_move(board, col):
    """Remove the topmost piece from a column (for backtracking)."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] != 0:
            board[r][col] = 0
            break

def print_board(board):
    """Print board in readable orientation."""
    print(np.flip(board, 0))

# -------------------------------
# Win Check
# -------------------------------
def winning_move(board, piece):
    """Check if the given piece has a winning condition."""
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative diagonal
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_game_over(board):
    """Return True if game is over (win or draw)."""
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_available_moves(board)) == 0

# -------------------------------
# Evaluation Function
# -------------------------------
def evaluate_window(window, piece):
    """Score a segment (window) of four cells."""
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 4

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 8

    return score

def evaluate_board(board, piece):
    """Evaluate the board position for a given player."""
    score = 0

    # Center column preference
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negative diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# -------------------------------
# Minimax with Alpha-Beta Pruning
# -------------------------------
node_counter = 0  # For instrumentation

def minimax(board, depth, alpha, beta, maximizingPlayer):
    """Minimax algorithm with Alpha-Beta Pruning."""
    global node_counter
    node_counter += 1

    valid_moves = get_available_moves(board)
    is_terminal = is_game_over(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI):
                return (None, 1e9)
            elif winning_move(board, PLAYER):
                return (None, -1e9)
            else:
                return (None, 0)  # Draw
        else:
            return (None, evaluate_board(board, AI))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            make_move(board, col, AI)
            new_score = minimax(board, depth-1, alpha, beta, False)[1]
            undo_move(board, col)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:  # Prune
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            make_move(board, col, PLAYER)
            new_score = minimax(board, depth-1, alpha, beta, True)[1]
            undo_move(board, col)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:  # Prune
                break
        return best_col, value

# -------------------------------
# Main Game Loop
# -------------------------------
def play_game():
    global node_counter
    board = create_board()
    game_over = False
    turn = random.choice([PLAYER, AI])

    print_board(board)
    print("Game start! You are Player 1 (Piece = 1)")

    while not game_over:
        if turn == PLAYER:
            col = int(input("Enter column (0-6): "))
            if col in get_available_moves(board):
                make_move(board, col, PLAYER)
                if winning_move(board, PLAYER):
                    print_board(board)
                    print("🎉 You win!")
                    game_over = True
            else:
                print("Invalid move.")
        else:
            print("\nAI is thinking...")
            node_counter = 0
            col, score = minimax(board, 4, -math.inf, math.inf, True)
            print(f"Nodes evaluated: {node_counter}")
            make_move(board, col, AI)
            if winning_move(board, AI):
                print_board(board)
                print("💻 AI wins!")
                game_over = True

        print_board(board)

        if not game_over and len(get_available_moves(board)) == 0:
            print("It's a draw!")
            break

        turn = PLAYER if turn == AI else AI

# -------------------------------
# Run the Game
# -------------------------------
if __name__ == "__main__":
    play_game()