import numpy.matlib
import pygame
import numpy
import random

# Need a matrix library

# Neural Net Class
# - activation function
# - constructor with nodes and layers and learning rate
# - predict function (feed forward)
# - train function (feed forward and back propagation)

# MAIN WILL RUN A TEST PROGRAM THAT PASSES THE XOR PROBLEM THROUGH THE NETWORK
# After this library has been created we need to edit for cnn for the minesweeper application

WIDTH = 400
HEIGHT = 400

def sigmoid(x):
    return 1.0/(1.0 + numpy.exp(-x))
    
def dsigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))

training_data = [{
    "inputs": [0, 0],
    "outputs": [0]
  },
  {
    "inputs": [0, 1],
    "outputs": [1]
  },
  {
    "inputs": [1, 0],
    "outputs": [1]
  },
  {
    "inputs": [1, 1],
    "outputs": [0]
  }
  
]

class NeuralNet:

    #need to establish no. of layers and make an array for each of those, and then weights and bias matrices for each connection between layers
    def __init__(self, *args):
        self.learningRate = 0.1
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
        print("INPUTS:")
        print([d['inputs'] for d in training_data])
        print()
        print("OUTPUTS:")
        print([d['outputs'] for d in training_data])
        print()

    # pass inputs through the network and return the outputs
    def forward(self, inputs):
        self.input = numpy.matrix(inputs).T
        # print("Layer 1")
        # print(self.input)
        # print()
        for i in range(0, self.layers - 1):
            if i == 0:
                nextLayerIn = self.input
            currentLayer = self.bias[i] + self.weights[i] @ nextLayerIn
            nextLayerIn = sigmoid(currentLayer)
            if(i < self.layers - 2):
                self.middleLayers[i] = nextLayerIn
            # print("Layer ", i + 2)
            # print(nextLayerIn)
            # print()

        # print("Middle layers: ")
        # for l in self.middleLayers:
            # print(l)
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
    def train(self, inputs, targets):

        for i in range(0, len(inputs)):

            # dC/dW = previousLayer * (currLayer * (1 - currLayer)) * (targets - output)
            # dC/dB =                 (currLayer * (1 - currLayer)) * (targets - output)

            
                # get the error (targets - output)
                outputs = self.forward(inputs[i])

                outputErrors = targets[i] - outputs
                hiddenError = outputErrors

                # (currLayer * (1 - currLayer)) * (targets - output) * learningRate
                outputGradient = numpy.multiply(( numpy.multiply(outputs , (1 - outputs)) ) , outputErrors)
                outputGradient = numpy.multiply(outputGradient, self.learningRate)

                # weights += previousLayer * (currLayer * (1 - currLayer)) * (targets - output) * learningRate
                self.weights[self.layers - 2] += outputGradient @ self.middleLayers[self.layers - 3].T
                # bias += (currLayer * (1 - currLayer)) * (targets - output) * learningRate
                self.bias[self.layers - 2] += outputGradient


                # Middle layers
                for j in range( self.layers - 3, 0, -1):
                    # pass back to get hidden layer errors
                    hiddenError = self.weights[j+1].T @ hiddenError

                    # same formula for gradient
                    hiddenGradient = numpy.multiply(( numpy.multiply(self.middleLayers[j] , (1 - self.middleLayers[j])) ) , hiddenError)
                    hiddenGradient = numpy.multiply(hiddenGradient, self.learningRate)

                    # same method for incrementing weights and biases
                    self.weights[j] += hiddenGradient @ self.middleLayers[j-1].T
                    self.bias[j] += hiddenGradient


                # Final hidden layer calculation

                # pass back to get hidden layer errors
                hiddenError = self.weights[1].T @ hiddenError

                # same formula for gradient
                hiddenGradient = numpy.multiply(( numpy.multiply(self.middleLayers[0] , (1 - self.middleLayers[0])) ) , hiddenError)
                hiddenGradient = numpy.multiply(hiddenGradient, self.learningRate)

                # same method for incrementing weights and biases
                self.weights[0] += hiddenGradient @ self.input.T
                self.bias[0] += hiddenGradient


# Can make some more generic training functions here, e.g train epoch, test etc.

def main():
    background_colour = (234, 212, 252)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption('Test')

    screen.fill(background_colour)

    pygame.display.flip()

    nn = NeuralNet(2, 25, 30, 40, 1)
    nn.printNetwork()
    inputs = [0, 0]
    # nn.forward(inputs)
    
    # for i in range(0, 100000):
    #     random.shuffle(training_data)
    #     nn.train([d['inputs'] for d in training_data], [d['outputs'] for d in training_data])

    # print()
    # print(nn.forward([0,0]))
    # print(nn.forward([0,1]))
    # print(nn.forward([1,0]))
    # print(nn.forward([1,1]))
    # print()
    # nn.printNetwork()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for i in range(0, 50):
            random.shuffle(training_data)
            nn.train([d['inputs'] for d in training_data], [d['outputs'] for d in training_data])

        for x in range(0,WIDTH//10):
            for y in range(0,HEIGHT//10):
                colour = nn.forward([(x*10)/WIDTH, (y*10)/HEIGHT])[0][0]*255
                pygame.draw.rect(screen, (colour, colour, colour), pygame.Rect(x*10,y*10,(x+1)*10,(y+1)*10))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()