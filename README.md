# NetworkLib
This is a WIP/in-development library for training basic neural networks, including dataset handling and importing from .txt files. As of writing this, the library can run a basic fully-connected deep neural network simulation with the ability to procedurally add layers and set custom network structure. The algorithm used is backpropagation, however matrices are not used (I plan to eventually add support for this). I will add more information here as the library grows, but for now this serves as a good place to log changes and save code.

# HOW TO USE/API
I will write this section once I have more of the library built. 

# CHANGELOG

`0.0.1`
+ Added functions.py including all external/utility functions needed for the dnn library
+ Added basic dnn library using forward feed/backpropagate for weight adjustments (biases soon)
+ Added 1-1-1 multiplication example for checking the main algorithm is working
+ Added 4 basic activation functions: sigmoid, tanh, linearRELU and leakyRELU
+ Added benchmark for activation functions
