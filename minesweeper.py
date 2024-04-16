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
        sprite = pygame.image.load("sprites/" + self.sprite + ".png").convert_alpha()
        screen.blit( sprite, (self.x*32, self.y*32))

    def reveal(self):
        self.revealed = True
        if(self.mine == True):
            self.sprite = "mine"
        elif(self.num > 0):
            self.sprite = str(self.num)
        else:
            self.sprite = "bg"

    


def printBoard(screen):
    pygame.display.set_caption('Minesweeper')
    # tile = pygame.image.load("sprites/tile.png").convert_alpha()



    # for x in range(BOARDWIDTH):
    #     for y in range(BOARDHEIGHT):
    #         screen.blit( tile, (x*32, y*32))

    tile = Tile(0, 0)
    tile.drawSprite(screen)

    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((BOARDWIDTH*32, BOARDHEIGHT*32))
    printBoard(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

if __name__ == "__main__":
    main()
    pygame.quit()