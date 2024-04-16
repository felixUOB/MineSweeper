import pygame

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
        print(self.sprite)

    def reveal(self):
        self.revealed = True
        if(self.mine == True):
            self.sprite = "mine"
        elif(self.num > 0):
            self.sprite = str(self.num)
        else:
            self.sprite = "bg"

        print(self.sprite)

    


def printBoard(screen, board):
    pygame.display.set_caption('Minesweeper')
    # tile = pygame.image.load("sprites/tile.png").convert_alpha()



    # for x in range(BOARDWIDTH):
    #     for y in range(BOARDHEIGHT):
    #         screen.blit( tile, (x*32, y*32))

    

    for i in range(BOARDHEIGHT):
        row = []
        for j in range(BOARDWIDTH):
            row.append(Tile(j, i))
            row[j].drawSprite(screen)
        board.append(row)

    

    # tile = Tile(0, 0)
    # tile.drawSprite(screen)

    pygame.display.flip()

def main():
    board=[]
    screen = pygame.display.set_mode((BOARDWIDTH*32, BOARDHEIGHT*32))
    printBoard(screen, board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[1]//32
                y = pygame.mouse.get_pos()[0]//32
                board[x][y].reveal()
                board[x][y].drawSprite(screen)
                pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()