import numpy as np
import pygame

Row_Num = 6
Colum_Num = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100

width = Colum_Num * SQUARESIZE
height = (Row_Num + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE / 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

def initial_board():
    board = np.zeros((Row_Num, Colum_Num))
    return board
def put_piece(board, row, col, piece):
    board[row][col] = piece

def make_Gui_Board(board):
    for c in range(Colum_Num):
        for r in range(Row_Num):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   circle_radius)
            else:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   circle_radius)

    pygame.display.update()

def Calculate_score_position(board, piece):

    Point = 0
    center_array = [int(i) for i in list(board[:, Colum_Num // 2])] #Colum in center
    center_count = center_array.count(piece)
    Point += center_count * 6

    for x in range(Row_Num):
        row_array = [int(i) for i in list(board[x, :])]
        for y in range(Colum_Num - 3):
            window = row_array[y:y + 4]
            Point += calculate_window(window, piece)

    # score vertical
    for x in range(Colum_Num):
        col_array = [int(i) for i in list(board[:, x])]
        for y in range(Row_Num - 3):
            window = col_array[y:y + 4]
            Point += calculate_window(window, piece)

    # score positively sloped diagonals
    for x in range(3, Row_Num):
        for y in range(Colum_Num - 3):
            window = [board[x - i][y + i] for i in range(4)]
            Point += calculate_window(window, piece)

    # score negatively sloped diagonals
    for x in range(3, Row_Num):
        for y in range(3, Colum_Num):
            window = [board[x - i][y - i] for i in range(4)]
            Point += calculate_window(window, piece)

    return Point


def Terminal_Test(board):
    return Win(board, AI_PIECE) or Win(board, Computer_PIECE) or len(get_valid_Colums(board)) == 0


def Alphabeta(board, depth, alpha, beta, MaxFlag):
    # all valid Colums on the board
    Valid_Colum = get_valid_Colums(board)
    Terminal = Terminal_Test(board)


    if depth == 0 or Terminal:
        if Terminal:  # winning move
            if Win(board, Computer_PIECE):
                 return (None, -10000000)
            elif Win(board, AI_PIECE):
                return (None, 10000000)
            else:
                return (None, 0)

        else:  # depth is zero
            return (None, Calculate_score_position(board, AI_PIECE))


    if MaxFlag:


        value = -math.inf
        column = random.choice(Valid_Colum)

        for col in Valid_Colum:
            row = Top_Row_Empty(board, col)
            b_copy = board.copy()
            put_piece(b_copy, row, col, AI_PIECE)
            new_score = Alphabeta(b_copy, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col

            alpha = max(value, alpha)

            if alpha >= beta:
                break

        return column, value


    else:  # for thte minimizing player
        value = math.inf
        column = random.choice(Valid_Colum)
        for col in Valid_Colum:
            row = Top_Row_Empty(board, col)
            b_copy = board.copy()
            put_piece(b_copy, row, col, Computer_PIECE)
            new_score = Alphabeta(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value


# get all columns where a piece can be
def get_valid_Colums(board):
    valid_locations = []

    for column in range(Colum_Num):
        if Empty_Colum(board, column):
            valid_locations.append(column)

    return valid_locations



def Game_Over():
    global game_over
    game_over = True
    print(game_over)


