import pygame
import numpy as np

LEFTCLICK = 1
RIGHTCLICK = 3

# Constants for the board size and mine number
BOARDWIDTH = 30
BOARDHEIGHT = 20
MINES = 70


# Current bugs:
#  - holding down a number tile with correct number of flags but in wrong positions crashes the game
#  - holding down a number tile and then moving the cursor without lifting will activate the reveal surrounding function
#    desired behaviour is it will only activate around the tile of which the cursor is released over


# Tile object stores all data about a tile
# and the funtions they need to perform
class Tile():

    # Instantiator class
    def __init__(self, x, y):
        self.revealed = False
        self.sprite = "tile"
        self.mine = False
        self.num = 0
        self.flag = False
        self.pressed = False
        self.x = x
        self.y = y
    
    # If tile isn't revealed it will place or remove a flag
    def placeFlag(self):
        if(self.flag == True):
            self.flag = False
            self.sprite = "tile"
        elif(self.flag == False and self.pressed == False and self.revealed == False):    
            self.flag = True
            self.sprite = "flag"

    # Set tile clicked to true
    def press(self):
        self.pressed = True
        self.sprite = "bg"

    # Set tile clicked to false
    def release(self):
        self.pressed = False
        self.sprite = "tile"

    # Set the tile to being a mine
    def makeMine(self):
        self.mine = True

    # Increment the number representing the surrounding mines
    def incrementNum(self):
        self.num += 1
    
    # Draw the tiles current sprite to the screen buffer
    def drawSprite(self, screen):
        img = pygame.image.load("sprites/" + self.sprite + ".png").convert_alpha()
        screen.blit( img, (self.x*32, self.y*32))

    # Change sprite to what is 'under' the tile
    def reveal(self):
        self.revealed = True
        if(self.mine == True):
            self.sprite = "mine"
        elif(self.num > 0):
            self.sprite = str(self.num)
        else:
            self.sprite = "bg"

    

# Create the board
def generateBoard(screen, board):
    pygame.display.set_caption('Minesweeper')

    # Create a 2D array of tile objects
    for i in range(BOARDWIDTH):
        column = []
        for j in range(BOARDHEIGHT):
            column.append(Tile(i, j))
            column[j].drawSprite(screen)
        board.append(column)

    pygame.display.flip()


# reveals all tiles on the board
def revealAll(board, screen):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y].reveal()
            board[x][y].drawSprite(screen)
        
    

# Generates mines in all spots that are not (startx, starty)
def generateMines(board, mines, startx, starty):

    # Place mines randomly, if there is already a mine try again until all mines are placed
    while(mines > 0):
        x = np.random.randint(0,BOARDWIDTH)
        y = np.random.randint(0,BOARDHEIGHT)

        # Check there is no mine, and it is not on the starting point
        if (board[x][y].mine == False and (x != startx or y != starty)):

            # Increment the num value of all surrounding tiles
            for xs in range(x - 1, x + 2):
                for ys in range(y - 1, y + 2):
                    if(xs != x or ys != y):
                        if((xs >= 0 and xs < BOARDWIDTH) and (ys >= 0 and ys < BOARDHEIGHT)):
                            board[xs][ys].incrementNum()
                    
                    
            board[x][y].makeMine()
            mines -= 1
        
# Recursive function that reveals all adjacent empty tiles
def floodFill(screen, board, x, y):

    # check for edge cases
    if(x < 0 or x >= BOARDWIDTH or y < 0 or y >= BOARDHEIGHT):
        return
    # if tile has been revealed already return
    if(board[x][y].revealed == True):
        return
    
    board[x][y].reveal()
    board[x][y].drawSprite(screen)
    
    # if the current tile is a number then it is an edge of the flood fill so return
    if(board[x][y].num > 0):
        return
    
    # repeat the function on the 8 surrounding tiles
    for i in range(-1, 2):
        for j in range(-1, 2):
            if(i != 0 or j != 0):
                floodFill(screen, board, x + i, y + j)


# press the tiles surrounding x, y
def pressSurrounding(screen, board, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):

            # Check edge of board
            if(x + i >= 0 and x + i < BOARDWIDTH and y + j >= 0 and y + j < BOARDHEIGHT):

                # only press if tile is not already revealed or flagged
                if(board[x+i][y+j].revealed == False and board[x+i][y+j].flag == False):
                    board[x+i][y+j].press()
                    board[x+i][y+j].drawSprite(screen)

# will reveal tiles surrounding x, y if the no. of surrounding flags matches the no. on x, y
# returns true when the game is over and false when it is not
def releaseSurrounding(screen, board, x, y):

    # count the number of flags
    flags = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if(x + i >= 0 and x + i < BOARDWIDTH and y + j >= 0 and y + j < BOARDHEIGHT):
                if(board[x+i][y+j].flag == True):
                    flags += 1

    # if flags match the number on the tile then perform floodfill on the surrounding tiles
    if(flags == board[x][y].num):

        #######################
        ### SOURCE OF A BUG ###
        #######################
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(x + i >= 0 and x + i < BOARDWIDTH and y + j >= 0 and y + j < BOARDHEIGHT):
                    if(board[x+i][y+j].revealed == False and board[x+i][y+j].flag == False):
                        if(board[x+i][y+j].mine == True):
                            revealAll(screen, board)
                            return True
                        else:
                            floodFill(screen, board, x+i, y+j)
                            board[x+i][y+j].drawSprite(screen)

    # else release all the tiles
    else:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(x + i >= 0 and x + i < BOARDWIDTH and y + j >= 0 and y + j < BOARDHEIGHT):
                    if(board[x+i][y+j].revealed == False and board[x+i][y+j].flag == False):
                        board[x+i][y+j].release()
                        board[x+i][y+j].drawSprite(screen)
    return False
    
# Main function
def main():
    board=[]
    screen = pygame.display.set_mode((BOARDWIDTH*32, BOARDHEIGHT*32))
    generateBoard(screen, board)

    # Clock allows the ability to cap fps 
    clock = pygame.time.Clock()

    firstMoveMade = False

    running = True
    gameOver = False
    clicked = False
    prevx = 0
    prevy = 0

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
            # While player has not hit a mine
            if (gameOver == False):

                # calculations when mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]//32
                    y = pygame.mouse.get_pos()[1]//32

                    if(event.button == LEFTCLICK):
                        clicked = True
                        if(board[x][y].revealed == False):
                            if(board[x][y].flag == False):
                                board[x][y].press()
                                board[x][y].drawSprite(screen)
                        else:
                            pressSurrounding(screen, board, x, y)
                    prevx = x
                    prevy = y
                
                    
                # when mouse is moved (these if statements could be swapped to optimise)
                if event.type == pygame.MOUSEMOTION:
                    if(clicked == True):
                        x = pygame.mouse.get_pos()[0]//32
                        y = pygame.mouse.get_pos()[1]//32

                        # release the old tile if it has not yet been revealed
                        if(board[prevx][prevy].revealed == False):
                            if(board[prevx][prevy].flag == False):
                                board[prevx][prevy].release()
                                board[prevx][prevy].drawSprite(screen)

                        # release surrounding if tile has already been revealed
                        else:

                            #######################
                            ### SOURCE OF A BUG ###
                            #######################
                            releaseSurrounding(screen, board, prevx, prevy)
                            
                        # press the new tile
                        if(board[x][y].revealed == False):
                            if(board[x][y].flag == False):
                                board[x][y].press()
                                board[x][y].drawSprite(screen)
                        else:
                            pressSurrounding(screen, board, x, y)
                        
                        prevx = x
                        prevy = y

                # perform the actual actions on mouseup
                if event.type == pygame.MOUSEBUTTONUP:
                    x = pygame.mouse.get_pos()[0]//32
                    y = pygame.mouse.get_pos()[1]//32

                    if(event.button == LEFTCLICK): 
                        clicked = False    
                        if (not firstMoveMade): 
                            generateMines(board, MINES, x, y)
                            firstMoveMade = True
                        if (board[x][y].mine == True and board[x][y].flag == False):
                            revealAll(board, screen)
                            gameOver = True
                        elif (board[x][y].revealed == True):
                            releaseSurrounding(screen, board, x, y)

                        elif (board[x][y].flag == False):
                            floodFill(screen, board, x, y)

                    if(event.button == RIGHTCLICK):
                        board[x][y].placeFlag()
                        board[x][y].drawSprite(screen)

                # Print display buffer to display         
                pygame.display.flip()

        #caps game to 60fps for consistency
        clock.tick(60)

                

                
# if run as the main program (not a library)
if __name__ == "__main__":
    main()
    pygame.quit()