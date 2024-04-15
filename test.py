import pygame

def main():
    background_colour = (234, 212, 252)

    screen = pygame.display.set_mode((300, 300))

    pygame.display.set_caption('Test')

    screen.fill(background_colour)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
    pygame.quit()