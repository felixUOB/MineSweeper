import pygame
import numpy as np

BOARDWIDTH = 20
BOARDHEIGHT = 20

class Tile():
    def __init__(self, x, y):
        self.revealed = False
        self.sprite = "tile"
        self.mine = False
        self.num = 0
        self.x = x
        self.y = y
    
    def makeMine(self):
        self.mine = True

    def incrementNum(self):
        self.num += 1
    
    def changeSprite(self, new):
        self.sprite = new

    def drawSprite(self, screen):
        img = pygame.image.load("sprites/" + self.sprite + ".png").convert_alpha()
        screen.blit( img, (self.x*32, self.y*32))

    def reveal(self):
        self.revealed = True
        if(self.mine == True):
            self.sprite = "mine"
        elif(self.num > 0):
            self.sprite = str(self.num)
        else:
            self.sprite = "bg"

    


def printBoard(screen, board):
    pygame.display.set_caption('Minesweeper')

    for i in range(BOARDHEIGHT):
        row = []
        for j in range(BOARDWIDTH):
            row.append(Tile(i, j))
            row[j].drawSprite(screen)
        board.append(row)

    pygame.display.flip()

def updateScreen(screen, board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y].drawSprite(screen)
            
#def revealAll(board):
    
def generateMines(board, mines):
    while(mines > 0):
        x = np.random.randint(0,BOARDWIDTH)
        y = np.random.randint(0,BOARDHEIGHT)

        if (board[x][y].revealed == False and board[x][y].mine == False):
            for xs in range(x - 1, x + 2):
                for ys in range(y - 1, y + 2):
                    if(xs != x or ys != y):
                        if((xs >= 0 and xs < BOARDWIDTH) and (ys >= 0 and ys < BOARDHEIGHT)):
                            print(xs, ", ", ys)
                            board[xs][ys].incrementNum()
                    
                    
            board[x][y].makeMine()
            # print(x, ", ", y)
            mines -= 1
        
    

def main():
    board=[]
    screen = pygame.display.set_mode((BOARDWIDTH*32, BOARDHEIGHT*32))
    printBoard(screen, board)

    generateMines(board, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]//32
                y = pygame.mouse.get_pos()[1]//32
                board[x][y].reveal()
                board[x][y].drawSprite(screen)
                pygame.display.flip()
                

if __name__ == "__main__":
    main()
    pygame.quit()