import pygame

# Neural Net Class
# - activation function
# - constructor with nodes and layers and learning rate
# - predict function (feed forward)
# - train function (feed forward and back propagation)

# MAIN WILL RUN A TEST PROGRAM THAT PASSES THE XOR PROBLEM THROUGH THE NETWORK
# After this library has been created we need to edit for cnn for the minesweeper application

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