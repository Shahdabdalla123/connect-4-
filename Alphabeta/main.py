import sys
import math
import random
from board import *
from threading import Timer
import tkinter as tk
Row_Num = 6
Colum_Num = 7
Computer_TURN = 0
AI_TURN = 1
Computer_PIECE = 1
AI_PIECE = 2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def Empty_Colum(board, col):
    return board[0][col] == 0


def Top_Row_Empty(board, col):
    for x in range(Row_Num - 1, -1, -1):
        if board[x][col] == 0:
            return x

def Win(board, piece):
    # checking horizontal
    for x in range(Colum_Num - 3):
        for y in range(Row_Num):
            if board[y][x] == piece and board[y][x + 1] == piece and board[y][x + 2] == piece and board[y][x + 3] == piece:
                return True

    # checking vertical
    for x in range(Colum_Num):
        for y in range(Row_Num - 3):
            if board[y][x] == piece and board[y + 1][x] == piece and board[y + 2][x] == piece and board[y + 3][x] == piece:
                return True

    # checking positively  diagonals
    for x in range(Colum_Num - 3):
        for y in range(3, Row_Num):
            if board[y][x] == piece and board[y- 1][x + 1] == piece and board[y - 2][x + 2] == piece and board[y - 3][x + 3] == piece:
                return True

    # checking negatively  diagonals
    for x in range(3, Colum_Num):
        for y in range(3, Row_Num):
            if board[y][x] == piece and board[y - 1][x - 1] == piece and board[y - 2][x - 2] == piece and board[y - 3][x - 3] == piece:
                return True


def calculate_window(screen, piece):

    against = Computer_PIECE
    if piece == Computer_PIECE:
        against = AI_PIECE

    point = 0

    if screen.count(piece) == 4:
        point += 100
    elif screen.count(piece) == 3 and screen.count(0) == 1:
        point += 10
    elif screen.count(piece) == 2 and screen.count(0) == 2:
        point += 2

    if screen.count(against) == 3 and screen.count(0) == 1:
        point -= 8

    return point

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
    
    
    
board = initial_board()
game_over = False
not_over = True
turn = random.randint(Computer_TURN, AI_TURN)
pygame.init()
my_font = pygame.font.SysFont("monospace", 75)

make_Gui_Board(board)
pygame.display.update()


def start_game_with_alpha(depth):
    global turn, not_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if turn == Computer_TURN and not game_over and not_over:
            col, _ = Alphabeta(board, depth, -math.inf, math.inf, False)

            if Empty_Colum(board, col):
                pygame.time.wait(500)
                row =Top_Row_Empty(board, col)
                put_piece(board, row, col, Computer_PIECE)
                if Win(board, Computer_PIECE):
                    print("Computer WINS!")
                    label = my_font.render("Computer WINS!", 1, RED)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, Game_Over)
                    t.start()

            make_Gui_Board(board)
            turn += 1
            turn = turn % 2

        if turn == AI_TURN and not game_over and not_over:
            col, _ = Alphabeta(board, depth, -math.inf, math.inf, True)

            if Empty_Colum(board, col):
                pygame.time.wait(500)
                row = Top_Row_Empty(board, col)
                put_piece(board, row, col, AI_PIECE)
                if Win(board, AI_PIECE):
                    print("Agent WINS!")
                    label = my_font.render("Agent WINS!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, Game_Over)
                    t.start()

            make_Gui_Board(board)
            turn += 1
            turn = turn % 2
