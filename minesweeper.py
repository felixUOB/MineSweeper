import pygame
import numpy as np

# Constants for the board size and mine number
BOARDWIDTH = 20
BOARDHEIGHT = 20
MINES = 20



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
        elif(self.flag == False):    
            self.flag = True
            self.sprite = "flag"

    # Set tile clicked to true
    def press(self):
        self.pressed = True
        self.sprite = "bg"

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
    for i in range(BOARDHEIGHT):
        row = []
        for j in range(BOARDWIDTH):
            row.append(Tile(i, j))
            row[j].drawSprite(screen)
        board.append(row)

    pygame.display.flip()

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
    if(x < 0 or x >= BOARDWIDTH or y < 0 or y >= BOARDHEIGHT):
        return
    if(board[x][y].revealed == True):
        return
    board[x][y].reveal()
    board[x][y].drawSprite(screen)
    if(board[x][y].num > 0):
        return
    for i in range(-1, 2):
        for j in range(-1, 2):
            if(i != 0 or j != 0):
                floodFill(screen, board, x + i, y + j)


    
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]//32
                    y = pygame.mouse.get_pos()[1]//32
                    if(event.button == 1):
                        clicked = True
                        if(board[x][y].revealed == False):
                            board[x][y].press()
                            board[x][y].drawSprite(screen)
                    prevx = x
                    prevy = y
                
                    
                
                if event.type == pygame.MOUSEMOTION:
                    if(clicked == True):
                        x = pygame.mouse.get_pos()[0]//32
                        y = pygame.mouse.get_pos()[1]//32
                        if(board[prevx][prevy].revealed == False):
                            board[prevx][prevy].release()
                            board[prevx][prevy].drawSprite(screen)
                        if(board[x][y].revealed == False):
                            board[x][y].press()
                            board[x][y].drawSprite(screen)
                        prevx = x
                        prevy = y

                    
                if event.type == pygame.MOUSEBUTTONUP:
                    x = pygame.mouse.get_pos()[0]//32
                    y = pygame.mouse.get_pos()[1]//32
                    if(event.button == 1): 
                        clicked = False    
                        if (not firstMoveMade): 
                            generateMines(board, MINES, x, y)
                            firstMoveMade = True
                        if (board[x][y].mine == True):
                            revealAll(board, screen)
                            gameOver = True
                        else:
                            floodFill(screen, board, x, y)
                    if(event.button == 3):
                        board[x][y].placeFlag()
                        board[x][y].drawSprite(screen)

                # Print display buffer to display         
                pygame.display.flip()
        clock.tick(60)

                

                
# 
if __name__ == "__main__":
    main()
    pygame.quit()