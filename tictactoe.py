"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None
counter = 0


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
    X_count = 0
    O_count = 0
    for row in range(len(board)):
        for cell in range(len(board[row])):
            if board[row][cell] == X:
                X_count += 1
            elif board[row][cell] == O:
                O_count += 1
            else:
                pass
    if X_count == O_count:
        return X
    elif X_count > O_count:
        return O
    else:
        return None

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                possible_actions.append((row, column))
    print(possible_actions)
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    print(action)
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] == X or new_board[action[0]][action[1]] == O:
        raise Exception
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if three_in_a_row(board) == 1:
        return X
    elif three_in_a_row(board) == -1:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]) or three_in_a_row(board) == 1 or three_in_a_row(board) == -1:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return three_in_a_row(board)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        None
    moves = []
    if player(board) == X:
        if board == [[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]:
            return (0,0)
        for action in actions(board):
            moves.append([min_value(result(board,action)),action])
        print(moves)
        return sorted(moves, key =lambda x: x[0], reverse=True)[0][1]
    else:
        for action in actions(board):
            moves.append([max_value(result(board,action)),action])
        print(moves)
        return sorted(moves, key =lambda x: x[0])[0][1]


def max_value(board):
    if terminal(board):
        return utility(board)
    test = -100
    for action in actions(board):
        test = max(test,min_value(result(board,action)))
    return test

def min_value(board):
    if terminal(board):
        return utility(board)
    test = 100
    for action in actions(board):
        test = min(test,max_value(result(board,action)))
    return test


def three_in_a_row(board):
    if board[0] == [X, X, X] or board[1] == [X,X,X] or board[2] == [X,X,X]:
        return 1
    elif (board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return 1
    elif (board[0][0] == X and board[1][0] == X and board[2][0] == X) or (board[0][1] == X and board[1][1] == X and board[2][1] == X) or (board[0][2] == X and board[1][2] == X and board[2][2] == X):
        return 1
    elif board[0] == [O,O,O] or board[1] == [O,O,O] or board[2] == [O,O,O]:
        return -1
    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return -1
    elif (board[0][0] == O and board[1][0] == O and board[2][0] == O) or (board[0][1] == O and board[1][1] == O and board[2][1] == O) or (board[0][2] == O and board[1][2] == O and board[2][2] == O):
        return -1
    elif EMPTY not in board:
        return 0
    

minimax([[EMPTY, X, O], [O, X, EMPTY],[EMPTY, EMPTY, EMPTY]])