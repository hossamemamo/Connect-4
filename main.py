import numpy as np #the structure used for storing the board is an np array
import pygame
import sys
import math
import time
from anytree import Node, RenderTree
from anytree.exporter import DotExporter #used to graph the MIN-MAX tree
from random import shuffle
import os
deptho = 2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
hueristic_array=np.array([[0.25,0.5,1,2,1,0.5,0.25],[0.5,1,2,3,2,1,0.5],[1,1.5,2.5,4,2.5,1.5,1],[1,1.5,2.5,4,2.5,1.5,1],[0.5,1,2,3,2,1,0.5],[0.25,0.5,1,2,1,0.5,0.25]])
PLAYER_PIECE=1
AI_PIECE=2

AI = 1
PLAYER = 0

algorithmChoice=0 #either min max or min max with prunning
counter=0
leafs = 0
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT)) #initializaing an empty array
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT): #starting from 0 to the row count we check for and empty row of the chosen column
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def winning_score(board, piece):
    score=0
    #Horizontal win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                score+=1

    # Vertical win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                score+=1

    # right digonal win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                score+=1

    # left digonal win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                score+=1
    return score


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (255, 255, 255), (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

#RED is 1
#yellow is 2
# AI FUNCTIONS

def get_Children(board): #get the children of the current board (vary from 0 to 7 ) and check if the child is valid
    children=[]
    for col in range(COLUMN_COUNT):
        if(is_valid_location(board,col)):
            children.append(col)

    return children

def is_terminal_node(board):
    return np.count_nonzero(board) == 42 #if the board has no empty places then the game is over (terminal node)


def min_max_pruning(board,depth,maximizingPlayer,alpha,beta,root):
    global counter #counter to differentiate between nodes and each others
    global leafs
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal: #if the depth is zero or we have reached a full board then we must return the score of the board
                                #this is a leaf node
        return (None, hurestic(board, AI_PIECE)-hurestic(board,PLAYER_PIECE))#calculate the score wrt the AI (maximizing player)
                                                                            #and player score (minimizing player)
    shuffled_neigboors=get_Children(board)
    shuffle(shuffled_neigboors)
    column=shuffled_neigboors[0]
    if maximizingPlayer == AI:
        best=-math.inf
        for col in shuffled_neigboors:
            row=get_next_open_row(board,col)
            board_copy=board.copy()
            drop_piece(board_copy,row,col,AI_PIECE)
            child = Node(board_copy, parent=root)
            new_score = min_max_pruning(board_copy, depth - 1, PLAYER, alpha, beta, child)[1]
            if depth == 1:#if it's a leaf node we print the board and it's score for tracing the minmax algorithm in the graph
                child.name=str(new_score) + "\n" + str(np.flip(board_copy, 0)) + "\n" + str(counter)
                leafs+=1
            else: #else it's a minimizing or a maximizing node then we should just add the score
                counter = counter + 1
                child.name =str(counter) + "\n" + str(new_score)


            if new_score > best:
                best = new_score
                column = col

            if algorithmChoice==0: #if we are using alpha beta pruning we assign the value of beta and alpha
                alpha=max(alpha,best)
                if beta <= alpha :
                    break
    else:
        best=math.inf
        for col in shuffled_neigboors:
            row=get_next_open_row(board,col)
            board_copy=board.copy()
            drop_piece(board_copy,row,col,PLAYER_PIECE)
            child = Node(board_copy, parent=root)
            new_score = min_max_pruning(board_copy, depth - 1, AI, alpha, beta, child)[1]
            if depth == 1:
                leafs += 1
                child.name=str(new_score) + "\n" + str(np.flip(board_copy, 0)) + "\n" + str(counter)
            else:
                counter = counter + 1
                child.name =str(counter) + "\n" + str(new_score)
            if new_score < best:
                best = new_score
                column = col
            if algorithmChoice==0:
                beta = min(beta, best)
                if beta <= alpha :
                    break

    return column,best



def scores(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100 #win
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10 #empty place and 3 in a row
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 3 #2 in a row and 2 empty places

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 5 #opponent win

    return score


def hurestic(board,piece):

    copy_board = board.copy()

    score=0
    # To favor playing the middle places we multiply the current board with the heuristic array to get a score
    #note that playing in the middle should be favored because it provides more opportunity for a win
    if piece == AI_PIECE :
         copy_board[copy_board == PLAYER_PIECE] = 0
         copy_board[copy_board == AI_PIECE]=1
         score+=np.sum(np.multiply(copy_board,hueristic_array))
    else:
         copy_board[copy_board == AI_PIECE] = 0
         score+=np.sum(np.multiply(copy_board,hueristic_array))

    # print("constant array")
    # print_board(hueristic_array)
    # print("this is the hurestic 2 board for = "+str(piece))
    # print_board(copy_board)
    # print("score of hurstic 2 is "+str(score))


    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4] #assign the row to a window for score calculation later
            score += scores(window, piece) #send the list (window) for score evaluation

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += scores(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += scores(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += scores(window, piece)

    #print("hurstec after feature score "+str(score))

    return score


turn = 0

#This function is called by the menu where the game starts playing
def star():
    global turn
    board = create_board()
    print_board(board)
    game_over = False
    PLAYER = 0
    AI = 1
    global leafs
    global counter
    AI_SCORE=0
    PLAYER_SCORE=0

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    #pygame.display.flip()
    myfont = pygame.font.SysFont("monospace", 75)
    while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # to clear previous circles
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()



                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    # Ask for Player 1 Input
                    if turn == PLAYER:

                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, PLAYER_PIECE)
                            turn += 1
                            turn = turn % 2

                        if is_terminal_node(board):
                            AI_SCORE += winning_score(board, AI_PIECE)
                            PLAYER_SCORE += winning_score(board, PLAYER_PIECE)
                            game_over = True

                    draw_board(board)

            if turn == AI and not game_over:
                if is_terminal_node(board):
                    AI_SCORE += winning_score(board, AI_PIECE)
                    PLAYER_SCORE += winning_score(board, PLAYER_PIECE)
                    game_over = True

                global deptho
                root = Node(board)
                start_time = time.time()
                col, minimax_scorecore = min_max_pruning(board,deptho,AI,-math.inf,math.inf,root)
                end_time = time.time()
                print("time taken = "+str(end_time-start_time)) #calculate time taked and display it in console

                # for i, list in enumerate(mins):
                #     print("entry number " + str(i))
                #     for branchindex, value in enumerate(list):
                #         print("mins score = " + str((mins_scores[i])[branchindex]))
                #         print("min number =" + str(branchindex))
                #         print_board(value)
                #
                #
                # for i, list in enumerate(maxs):
                #     print("entry number " + str(i))
                #     for branchindex, value in enumerate(list):
                #         print("max score = " + str((maxs_scores[i])[branchindex]))
                #         print("max number =" + str(branchindex))
                #         print_board(value)


                if is_valid_location(board, col):
                    # pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    draw_board(board)
                    root.name=str(minimax_scorecore) + "\n" + str(np.flip(board, 0))
                    DotExporter(root).to_picture("udo.svg") #comment this line when we attempt depth more than 4
                    os.system('udo.svg')
                    print("Nodes explored " + str(leafs))
                    counter=0
                    leafs=0
                    turn += 1
                    turn = turn % 2

    print("AI score is = "+str(AI_SCORE))
    print("Player score is = "+str(PLAYER_SCORE))
    time.sleep(5)
    exit()
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)