import numpy.matlib
import pygame
import numpy

# Need a matrix library

# Neural Net Class
# - activation function
# - constructor with nodes and layers and learning rate
# - predict function (feed forward)
# - train function (feed forward and back propagation)

# MAIN WILL RUN A TEST PROGRAM THAT PASSES THE XOR PROBLEM THROUGH THE NETWORK
# After this library has been created we need to edit for cnn for the minesweeper application

def sigmoid(x):
    return 1.0/(1.0 + numpy.exp(-x))
    
def dsigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


class NeuralNet:

    #need to establish no. of layers and make an array for each of those, and then weights and bias matrices for each connection between layers
    def __init__(self, *args):
        self.layers = len(args)
        self.input = [0] * args[0]
        self.output = [0] * args[self.layers - 1]
        self.middleLayers = []
        self.bias = []
        self.weights = [] 
        for i in range(1, self.layers - 1):
            self.weights.append(numpy.random.uniform(-0.5, 0.5, (args[i], args[i - 1])))
            self.bias.append(numpy.zeros((args[i], 1)))            
            self.middleLayers.append([0] * args[i])
        self.bias.append(numpy.zeros((args[self.layers - 1], 1)))
        self.weights.append(numpy.random.uniform(-0.5, 0.5, (args[self.layers - 1], args[self.layers - 2])))
        
    
    # prints the nodes of the network input - middle layers - output then biases and weights
    def printNetwork(self):
        print(self.input)
        print()
        for i in range(0, self.layers - 2):
            print(self.middleLayers[i])
        print()
        print(self.output)
        print()
        print("Biases:")
        for i in range(0, self.layers - 1):
            print(self.bias[i])
        print()
        print("Weights:")
        for i in range(0, self.layers - 1):
            print(self.weights[i])
        print()

    # pass inputs through the network and return the outputs
    def forward(self, inputs):
        self.input = numpy.matrix(inputs).T
        for i in range(0, self.layers - 1):
            if i == 0:
                nextLayerIn = self.input
            currentLayer = self.bias[i] + self.weights[i] @ nextLayerIn
            nextLayerIn = sigmoid(currentLayer)
            print(nextLayerIn)
        return nextLayerIn

        # print(self.input)
        # layer2 = self.bias[0] + self.weights[0] @ self.input
        # layer2 = sigmoid(layer2)
        # print(layer2)
        # layer3 = self.bias[1] + self.weights[1] @ layer2
        # layer3 = sigmoid(layer3)
        # print(layer3)
        # layer4 = self.bias[2] + self.weights[2] @ layer3
        # layer4 = sigmoid(layer4)
        # print(layer4)
        # layer5 = self.bias[3] + self.weights[3] @ layer4
        # layer5 = sigmoid(layer5)

        # return layer5

    # back propogation on a given set of training datas
    def train(self):
        print("Implement me!")
        
# Can make some more generic training functions here, e.g train epoch, test etc.

def main():
    background_colour = (234, 212, 252)

    screen = pygame.display.set_mode((300, 300))

    pygame.display.set_caption('Test')

    screen.fill(background_colour)

    pygame.display.flip()

    nn = NeuralNet(3, 3, 5, 5, 1)
    nn.printNetwork()
    print(sigmoid(0.0))
    inputs = [1, 2, 3]
    print(nn.forward(inputs))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
    pygame.quit()