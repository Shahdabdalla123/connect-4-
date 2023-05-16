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


