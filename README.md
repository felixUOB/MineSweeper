# Convolutional Neural Network vs Minesweeper
## Aims of the project:
The end goal is to have a convolutional neural network that we will have trained to beat the game Minesweeper. The main point of the project is to understand the underlying maths and algorithms in a neural network, as a result the code will be much less optimised than what we could get from one of the big deep learning libraries. However we want to get more of an understanding of how these libraries work and the optimisations we can make.

## Inspiration:
A lot of the maths for the neural network was taken from the 3Blue1Brown series on neural networks:\
https://youtu.be/aircAruvnKk?si=yxUSZd2SZmCPK8t1 (Episodes 1-4)

## Current Progress:
Currently we have a working neural network library that is able to create and train a network with any amount of layers and nodes. It currently tests this with the XOR problem. We also have a mock version of minesweeper made in python with pygame.



| ![xor](https://github.com/user-attachments/assets/4de2b7f6-6344-49af-bf7f-d5f58f0d31c3) | 
|:--:| 
| *Neural network of shape 2-8-8-1 with learning rate 0.05 solving the xor problem* |

## Next steps:
- Add convolutional layers and test them on the MNIST set
- Create own matrix maths library
