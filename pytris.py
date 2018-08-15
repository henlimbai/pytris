#import the pygame module, and the
#sys module for exiting the window we create
import pygame, sys

#allows us to use random numbers
import random

#import some usefil constants
from pygame.locals import *

#useful game dimensions
COLS = 10;
ROWS = 20;
TILESIZE = 40
HEADER_SPACE = 40

#a list representing our tilemap
tilemap = [ [0 for x in range(COLS)] for x in range(ROWS) ]

#constants representing colours
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BROWN = (153,  76,   0)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
DARK_RED   = (190,   0,   0)
DARK_GREEN = (  0, 190,   0)
DARK_BLUE  = (  0,   0, 190)
DARK_BROWN = (113,  46,   0)

#a dictionary linking tiles to colours
colours = {
    0 : BLACK,
    1 : RED,
    2 : BLUE,
    3 : GREEN,
    4 : BROWN,
    5 : DARK_RED,
    6 : DARK_BLUE,
    7 : DARK_GREEN,
    8 : DARK_BROWN,
}

#a dictionary linking colours to dark_colours
dark_colours = {
    0 : 0,
    1 : 5,
    2 : 6,
    3 : 7,
    4 : 8,
}

#game pieces
pieces = [
    [[1, 1, 1, 1]],
    [[0,2],[0,2],[2,2]],
    [[2,0],[2,0],[2,2]],
    [[0,3,0],[3,3,3]],
    [[4,4,0],[0,4,4]],
    [[0,4,4],[4,4,0]],
    [[2,2],[2,2]]
]

#define how to rotate a piece from the game
def rotate(piece):
    "rotates a piece of the game"
    new_piece = [
        [
            piece[len(piece)-1-x][y]
            for x in range(len(piece))
        ]
        for y in range(len(piece[0]))
    ]
    return new_piece

def overlap(piece, position_row, position_column):
    "returns true if the piece overlap a non empty square"
    global tilemap
    #loop through each row of the piece
    for row in range(len(piece)):
        #loop through each column in the row
        for column in range(len(piece[0])):
            #calculate the position of the piece's square
            tilemap_row = row + position_row
            tilemap_column = column + position_column
            #calculate if the overlapping occurs
            flag = tilemap[tilemap_row][tilemap_column] != 0
            flag = flag and (piece[row][column] != 0)
            #if the overlap occurs return true
            if flag: return True
    #if no overlap is found return false
    return False

def insert_piece_in_tilemap(piece, position_row, position_column):
    "insert the piece in the tilemap"
    global tilemap
    #loop through each row of the piece
    for row in range(len(piece)):
        #loop through each column in the row
        for column in range(len(piece[0])):
            #if there is a piece's square in the position
            if piece[row][column] != 0:
                #calculate the position of the piece's square
                tilemap_row = row + position_row
                tilemap_column = column + position_column
                #inserts the piece in the tilemap
                value = piece[row][column]
                tilemap[tilemap_row][tilemap_column] = dark_colours[value]

def check_row(row):
    "check if the row is filled"
    global tilemap
    for column in range(len(tilemap[0])):
        if tilemap[row][column] == 0:
            return False
    return True

def remove_row(row):
    "removes the row from the tilemap"
    global tilemap
    #loop from bottom up through each row above the informed one
    for upper_row in range(row - 1, 0, -1):
        #loop through each column in the row
        for column in range(len(tilemap[0])):
            tilemap[upper_row + 1][column] = tilemap[upper_row][column]
            tilemap[upper_row][column] = 0

def clean_filled_rows():
    "removes the lines completely filled"
    global tilemap, removed_rows
    global user_points
    points = 100
    #loop through each row of the tilemap
    for row in range(len(tilemap)):
        #check if the row is filled
        if check_row(row):
            remove_row(row)
            user_points += points
            points *= 4
            removed_rows += 1
    if removed_rows > 10:
        removed_rows -= 10
        time_pause = time_pause * 0.8

#initialize the pygame module
pygame.init()

#Create a new drawing surface
DISPLAYSURF = pygame.display.set_mode((COLS*TILESIZE, HEADER_SPACE + ROWS*TILESIZE))

#add a font to our inventory
INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)

#give the window a caption
pygame.display.set_caption('Pytris')

#initializes a clock
fpsClock = pygame.time.Clock()

#initializes the user points 
user_points = 0

#initializes the game speed (in fact, the inverse of the speed)
time_pause = 600

#initializes the time spent after the last down movement of the piece
piece_wait = 0

#initilizes the counter
removed_rows = 0

#choose the first piece
current_piece = pieces[random.randint(0,4)]
for rotation in range(random.randint(0,3)):
    current_piece = rotate(current_piece)
piece_position_row = 0
piece_position_column = 3

def try_move_down():            
    "try to move down the piece"
    global piece_position_row, piece_position_column
    global current_piece
    #check if the piece will be out of the borders
    flag = piece_position_row + len(current_piece) < ROWS
    #check if the piece will overlap another piece
    flag = flag and not overlap (
        current_piece, 
        piece_position_row + 1, 
        piece_position_column
    )
    #if the piece can move down
    if flag:
        #moves the piece down
        piece_position_row += 1

#process the keys pressed
def process_key(key):
    "process a key press"
    global piece_position_row, piece_position_column
    global current_piece
    #if the right arrow is pressed
    if key == K_RIGHT:
        #check if the piece will be out of the right border
        flag = piece_position_column + len(current_piece[0]) < COLS
        #check if the piece will overlap another piece
        flag = flag and not overlap (
            current_piece, 
            piece_position_row, 
            piece_position_column + 1
        )
        #if the piece can move to the right
        if flag:
            #moves the piece to the right
            piece_position_column += 1
    #if the left arrow is pressed
    if key == K_LEFT:
        #check if the piece will be out of the left border
        flag = piece_position_column - 1 >= 0
        #check if the piece will overlap another piece
        flag = flag and not overlap (
            current_piece, 
            piece_position_row, 
            piece_position_column - 1
        )
        #if the piece can move to the left
        if flag:
            #moves the piece to the left
            piece_position_column -= 1
    #if the up arrow is pressed
    if key == K_UP:
        #rotate the piece 
        rotated_piece = rotate(current_piece)
        #check if the piece will be out of the right border
        flag = piece_position_column + len(rotated_piece[0]) -1 < COLS
        #check if the piece will be out of the left border
        flag = flag and piece_position_column >= 0
        #check if the piece will be out of the down border
        flag = flag and piece_position_row + len(rotated_piece) < ROWS
        #check if the piece will overlap another piece
        flag = flag and not overlap (
            rotated_piece, 
            piece_position_row, 
            piece_position_column
        )
        #if the piece can be rotated
        if flag:
            #replace the piece
            current_piece = rotated_piece
    #if the down arrow is pressed
    if key == K_DOWN:
        #try to move down the piece
        try_move_down()

#loop (repeat) forever
while True:

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #end the game and close the window
            pygame.quit()
            sys.exit()
        #if a key is pressed
        elif event.type == KEYDOWN:
            #process the key
            process_key(event.key);

    #create the string with the user points
    textObj = INVFONT.render(str(user_points), True, WHITE, BLACK)
    #draw the user points
    DISPLAYSURF.blit(textObj, (20, 10))

    #loop through each row
    for row in range(ROWS):
        #loop through each column in the row
        for column in range(COLS):
            #draw the resource at that position in the tilemap, using the
            #correct colour
            pygame.draw.rect(
                DISPLAYSURF,
                colours[tilemap[row][column]],
                (column*TILESIZE, HEADER_SPACE + row*TILESIZE, TILESIZE, TILESIZE)
            )

    #draw the piece over the tilemap
    for row in range(len(current_piece)):
        for column in range(len(current_piece[0])):
            if current_piece[row][column] != 0:
                #calculates the correct position of the piece
                position_col = column + piece_position_column
                position_row = row    + piece_position_row
                #draw each square of the piece using the correct colours
                pygame.draw.rect(
                    DISPLAYSURF,
                    colours[current_piece[row][column]],
                    (
                        position_col*TILESIZE,
                        HEADER_SPACE + position_row*TILESIZE,
                        TILESIZE,
                        TILESIZE
                    )
                )

    #check if the piece is already overlapping another piece    
    flag = overlap (
        current_piece, 
        piece_position_row, 
        piece_position_column
    )
    #if the piece is already overlapping another piece
    if flag:
        #create the string with the GAME OVER info
        textObj = INVFONT.render('__GAME_OVER__', True, BLACK, RED)
        #draw the GAME OVER info
        DISPLAYSURF.blit(textObj, (60, 10))

   
    #if the piece touch the bottom, it stops moving
    #check if the piece touched the bottom
    flag = piece_position_row + len(current_piece) >= ROWS
    #check if the piece touched another piece
    flag = flag or overlap (
        current_piece, 
        piece_position_row + 1, 
        piece_position_column
    )
    #if the piece can not move down
    if flag:
        #the piece becomes part of the tilemap
        insert_piece_in_tilemap(
            current_piece, 
            piece_position_row, 
            piece_position_column
        )
        #remove the filled rows
        clean_filled_rows()
        #choose and create a new piece
        current_piece = pieces[random.randint(0,4)]
        for rotation in range(random.randint(0,3)):
            current_piece = rotate(current_piece)
        piece_position_row = 0
        piece_position_column = 3

    #wait for it...
    dt = fpsClock.tick(60)
    piece_wait += dt
    if piece_wait >= time_pause:
        piece_wait -= time_pause
        try_move_down()
        
    #update the display
    pygame.display.update()

