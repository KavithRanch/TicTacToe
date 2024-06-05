
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
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
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
    for row in board:
        for col in row:
            if col == EMPTY:
                action.add((r, c))
            c += 1
        r += 1
        c = 0
    if len(action) == 0:
        return None
    else:
        return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    i, j = action

    if action in actions(board):
        new_board[i][j] = player(new_board)
        return new_board
    else:
        raise Exception("Cannot place marker in that spot")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    i = 0
    for j in range(3):
        if board[i][j] == EMPTY:
            continue
        if j == 0:
            if board[i][j + 1] == board[i][j] and board[i][j + 2] == board[i][j]:
                return board[i][j]
            if board[i + 1][j + 1] == board[i][j] and board[i + 2][j + 2] == board[i][j]:
                return board[i][j]
        elif j == 2:
            if board[i + 1][j - 1] == board[i][j] and board[i + 2][j - 2] == board[i][j]:
                return board[i][j]

        if board[i + 1][j] == board[i][j] and board[i + 2][j] == board[i][j]:
            return board[i][j]

    y = 0
    for x in range(1, 3):
        if board[x][y] == EMPTY:
            continue
        if board[x][y + 1] == board[x][y] and board[x][y + 2] == board[x][y]:
            return board[x][y]

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


def maxvalue(board):
    if terminal(board):
        return utility(board), None

    val = -math.inf
    moves = actions(board)
    next_action = (0, 0)
    for action in moves:
        new_val, act = minvalue(result(board, action))
        act = action
        prev_val = val
        val = max(val, new_val)
        if prev_val != val:
            next_action = act

    return val, next_action


def minvalue(board):
    if terminal(board):
        return utility(board), None

    val = math.inf
    moves = actions(board)
    next_action = (0, 0)
    for action in moves:
        new_val, act = maxvalue(result(board, action))
        act = action
        prev_val = val
        val = min(val, new_val)
        if prev_val != val:
            next_action = act

    return val, next_action

board = initial_state()
board[0][0] = O
board[0][1] = X
board[0][2] = X
board[1][0] = X
board[1][1] = X
board[1][2] = O
board[2][0] = O
board[2][1] = X
board[2][2] = O

for i in board:
    print(i)


print(player(board) + "'s turn")
print("Next Move: " + str(minimax(board)))
if terminal(board):
    print("Winner is: " + str(winner(board)))