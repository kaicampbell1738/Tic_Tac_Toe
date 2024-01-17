import pygame as py
import numpy as num
import random
import sys
import asyncio

async def main():

    #local variables
    person = 0
    playing = True
    width = 600
    height = width
    lineWidth = 15
    boardR = 3
    boardC = 3
    squareSize = width // boardC
    circleR = squareSize // 3
    circleW = 15
    crossW = 15
    space = squareSize // 4

    red = (255, 0, 0)
    blue = (17, 94, 217)
    grey_blue = (9, 50, 115)
    black = (0, 0, 0)
    white = (255, 255, 255)

    #build platform
    py.init()
    screen = py.display.set_mode((width, height))
    py.display.set_caption('TIC TAC TOE')
    screen.fill( white )
    board = num.zeros((boardR, boardC))

    def make_menu():
        screen.fill( white )
        font = py.font.Font('freesansbold.ttf', 32)
        font2 = py.font.SysFont('timesnewroman', 20)
        text = font.render('Click Either Mouse Button to Start', True, black, white)
        text2 = font2.render('Click ESC to Return to Menu', True, black, white)
        text3 = font2.render('Click R to Restart', True, black, white)
        textRect = text.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()
        textRect.center = (width // 2, (height // 2) - 50)
        textRect2.center = (width // 2, (height // 2))
        textRect3.center = (width // 2, (height // 2) + 50)
        screen.blit(text, textRect)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)

    make_menu()
    #build lines
    def make_lines():
        #horizontal 
        py.draw.line(screen, grey_blue, (0,squareSize), (width,squareSize), lineWidth)
        py.draw.line(screen, grey_blue, (0,2*squareSize), (width,2*squareSize), lineWidth)

        #vertical
        py.draw.line(screen, grey_blue, (squareSize,0), (squareSize,width), lineWidth)
        py.draw.line(screen, grey_blue, (2*squareSize,0), (2*squareSize,width), lineWidth)

    def set_board():
        screen.fill( blue )
        board = num.zeros((boardR, boardC))

    #place square
    def place_square(person, row, column):
        board[row][column] = person

    #draw X and O
    def draw_objects():
        for i in range(boardR):
            for j in range(boardC): 
                if board[i][j] == 1:
                    py.draw.circle( screen, black, (int( j * squareSize + squareSize // 2), int( i * squareSize + squareSize // 2 )), circleR, circleW)
                elif board[i][j] == 2:
                    py.draw.line( screen, white, (j * squareSize + space, i * squareSize + squareSize - space), (j * squareSize + squareSize - space, i * squareSize + space), crossW)
                    py.draw.line( screen, white, (j * squareSize + space, i * squareSize + space), (j * squareSize + squareSize - space, i * squareSize + squareSize - space), crossW)

    #checks if unoccupied
    def unoccupied_square(row, column):
        if board[row][column] == 0:
            return True
        else:
            return False

    #checks if board is full
    def board_full():
        for i in range(boardR):
            for j in range(boardC):
                if board[i][j] == 0:
                    return False
        return True

    #checks if won
    def check_win(person):
        for i in range(boardR):
            if board[i][0] == person and board[i][1] == person and board[i][2] == person:
                draw_horizontal_win(i, person)
                return True

        for j in range(boardC):
            if board[0][j] == person and board[1][j] == person and board[2][j] == person:
                draw_vertical_win(j, person)
                return True

        if board[2][0] == person and board[1][1] == person and board[0][2] == person:
            draw_diagonal_desc(person)
            return True

        if board[2][2] == person and board[1][1] == person and board[0][0] == person:
            draw_diagonal_asc(person)
            return True

        return False

    #checks if reset is requested
    def reset():
        screen.fill(blue)
        make_lines()
        person = 1
        for i in range(boardR):
            for j in range(boardC):
                board[i][j] = 0

    #draws winning lines
    def draw_horizontal_win(row, person):
        linePos = row * squareSize + squareSize // 2
        py.draw.line(screen, grey_blue, (20, linePos), (width - 20, linePos), lineWidth)

    def draw_vertical_win(column, person):
        linePos = column * squareSize + squareSize // 2
        py.draw.line(screen, grey_blue, (linePos, 20), (linePos , width - 20), lineWidth)

    def draw_diagonal_desc(person):
        py.draw.line(screen, grey_blue, (20, width - 20), (width - 20, 20), lineWidth)

    def draw_diagonal_asc(person):
        py.draw.line(screen, grey_blue, (20, 20), (width - 20, width - 20), lineWidth)

    #game loop
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN and playing:
                set_board()
                make_lines()

                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clickedRow = int(mouseY // squareSize)
                clickedColumn = int(mouseX // squareSize)

                if unoccupied_square(clickedRow, clickedColumn):
                    if person == 1:
                        place_square(1, clickedRow, clickedColumn)
                        if check_win(person):
                            playing = False
                        person = 2

                    draw_objects()
                if person == 0:
                    person = 1

            if playing:
                if person == 2:
                    randR = random.randint(0, boardR- 1)
                    randC = random.randint(0, boardC- 1)
                    while unoccupied_square(randR, randC) != True:
                        randR = random.randint(0, boardR- 1)
                        randC = random.randint(0, boardC- 1)
                    place_square(2, randR, randC)
                    if check_win(person):
                        playing = False
                    person = 1

                draw_objects()

            if event.type == py.KEYDOWN:
                if event.key == py.K_r and person != 0:
                    playing = True
                    reset()

                if event.key == py.K_ESCAPE:
                    playing = True
                    reset()
                    make_menu()
                    person = 0
                    

        py.display.update()
        await asyncio.sleep(0)


asyncio.run(main())