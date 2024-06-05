import math
import copy

X = "X"
O = "O"
EMPTY = None
X_turn = True

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]],
            [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]],
            [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for section in board:
        for row in section:
            for col in row:
                if col == X:
                    x_count += 1
                if col == O:
                    o_count += 1

    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    r = 0
    c = 0
    s = 0
    for section in board:
        for row in section:
            for col in row:
                if col == EMPTY:
                    action.add((s, r, c))
                c += 1
            r += 1
            c = 0
        s += 1
        r = 0
    if len(action) == 0:
        return None
    else:
        return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    i, j, k = action

    if action in actions(board):
        new_board[i][j][k] = player(new_board)
        return new_board
    else:
        raise Exception("Cannot place marker in that spot")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking all combos of 3 in a row from the front 9 to back 9 slots
    b = 0
    for a in range(3):
        for c in range(3):
            if board[a][b][c] == EMPTY:
                continue
            if c == 0:
                if board[a][b][c + 1] == board[a][b][c] and board[a][b][c + 2] == board[a][b][c]:
                    return board[a][b][c]
                if board[a][b + 1][c + 1] == board[a][b][c] and board[a][b + 2][c + 2] == board[a][b][c]:
                    return board[a][b][c]
            elif c == 2:
                if board[a][b + 1][c - 1] == board[a][b][c] and board[a][b + 2][c - 2] == board[a][b][c]:
                    return board[a][b][c]

            if board[a][b + 1][c] == board[a][b][c] and board[a][b + 2][c] == board[a][b][c]:
                return board[a][b][c]

    f = 0
    for d in range(3):
        for e in range(1, 3):
            if board[d][e][f] == EMPTY:
                continue
            if board[d][e][f + 1] == board[d][e][f] and board[d][e][f + 2] == board[d][e][f]:
                return board[d][e][f]

    # Checking all combos of 3 in a row from side-to-side (where we see three of each of the panels at a time)
    # Can avoid going from top row to bottom row straight line check since already done in previous checks
    j = 0
    for k in range(2, -1, -1):
        for i in range(3):
            if board[i][j][k] == EMPTY:
                continue
            if i == 0:
                if board[i + 1][j][k] == board[i][j][k] and board[i + 2][j][k] == board[i][j][k]:
                    return board[a][b][c]
                if board[i + 1][j + 1][k] == board[i][j][k] and board[i + 2][j + 2][k] == board[i][j][k]:
                    return board[a][b][c]
            if i == 2:
                if board[i - 1][j + 1][k] == board[i][j][k] and board[i - 2][j + 2][k] == board[i][j][k]:
                    return board[i][j][k]

    m = 0
    for o in range(2, -1, -1):
        for n in range(1, 3):
            if board[m][n][o] == EMPTY:
                continue
            if board[m + 1][n][o] == board[m][n][o] and board[m + 2][n][o] == board[m][n][o]:
                return board[m][n][o]

    # Checking all diagonals through all 3 three panels
    for v in range(4):
        x = y = z = 0
        if v == 0:
            if board[x + 1][y + 1][z + 1] == board[x][y][z] and board[x + 1][y + 1][z + 1] == board[x][y][z]:
                return board[x][y][z]
        elif v == 1:
            z = 2
            if board[x + 1][y + 1][z - 1] == board[x][y][z] and board[x + 2][y + 2][z - 2] == board[x][y][z]:
                return board[x][y][z]
        elif v == 2:
            x = 2
            z = 2
            if board[x - 1][y + 1][z - 1] == board[x][y][z] and board[x - 2][y + 2][z - 2] == board[x][y][z]:
                return board[x][y][z]
        else:
            x = 2
            if board[x - 1][y + 1][z + 1] == board[x][y][z] and board[x - 2][y + 2][z + 2] == board[x][y][z]:
                return board[x][y][z]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or actions(board) is None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    cur_player = player(board)
    if cur_player == X:
        val, act = maxvalue(board)
    else:
        val, act = minvalue(board)

    print(val)
    return act


'#TO UPDATE !!'
def maxvalue(board):
    if terminal(board):
        return utility(board), None

    printboard(board)

    val = -math.inf
    moves = actions(board)
    next_action = (0, 0, 0)
    for action in moves:
        new_val, act = minvalue(result(board, action))
        act = action
        prev_val = val
        val = max(val, new_val)
        if prev_val != val:
            next_action = act

    return val, next_action

'#TO UPDATE !!'
def minvalue(board):
    if terminal(board):
        return utility(board), None

    val = math.inf
    moves = actions(board)
    next_action = (0, 0, 0)
    for action in moves:
        new_val, act = maxvalue(result(board, action))
        act = action
        prev_val = val
        val = min(val, new_val)
        if prev_val != val:
            next_action = act

    return val, next_action


board = initial_state()

board[0][0][0] = EMPTY
board[0][0][1] = EMPTY
board[0][0][2] = EMPTY
board[0][1][0] = EMPTY
board[0][1][1] = EMPTY
board[0][1][2] = EMPTY
board[0][2][0] = EMPTY
board[0][2][1] = EMPTY
board[0][2][2] = EMPTY

board[1][0][0] = EMPTY
board[1][0][1] = EMPTY
board[1][0][2] = EMPTY
board[1][1][0] = EMPTY
board[1][1][1] = X
board[1][1][2] = EMPTY
board[1][2][0] = EMPTY
board[1][2][1] = EMPTY
board[1][2][2] = EMPTY

board[2][0][0] = EMPTY
board[2][0][1] = EMPTY
board[2][0][2] = EMPTY
board[2][1][0] = EMPTY
board[2][1][1] = EMPTY
board[2][1][2] = EMPTY
board[2][2][0] = EMPTY
board[2][2][1] = EMPTY
board[2][2][2] = EMPTY

# PRINTING BOARD:
def printboard(board):
    cnt = 0
    for i in board:
        if cnt == 0:
            print("Front: ")
        elif cnt == 1:
            print("Middle: ")
        else:
            print("Back: ")

        for j in i:
            print(j)

        print()
        cnt += 1

print(player(board) + "'s turn")
print("Next Move: " + str(minimax(board)))
if terminal(board):
    print("Winner is: " + str(winner(board)))