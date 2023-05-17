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




