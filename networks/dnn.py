from sys import *
path.append('D:/NetworkLib/tools')

from functions import *
from activations import *
from time import *
from random import *

class DeepNeuralNetwork:

	def __init__(self, layers, activation):
		#Some basic variables to keep track of what's happening
		self.active_layers = 1 #One hidden layer
		self.layer_structure = layers #Save this for adding layers later on, so we know what the structure is
		self.epochs = 0 #Number of forward passes
		self.biased_range = distributedRange() #Biased range to get weight values from

		#Set activation function using a dictionary that stores the functions themselves as objects
		activation_functions = dict(
    							sigmoid = (sigmoid_normal, sigmoid_derivative),
    							tanh = (tanh_normal, tanh_derivative),
    							linearRELU = (linearRELU_normal, linearRELU_derivative),
    							leakyRELU = (leakyRELU_normal, leakyRELU_derivative),
									)
		self.activation_normal, self.activation_derivative = activation_functions[activation]

		#Layer structure [4, 7, 7, 7, 4] means 4 input nodes, 3 hidden layers each with 7 nodes and 4 output nodes
		self.nodes = []
		self.nodes.append([0 for x in range(layers[0])]) #Input nodes
		self.nodes.append([0 for x in range(layers[1])]) #First hidden layer
		self.nodes.append([0 for x in range(layers[-1])]) #Output nodes

		#Build sums
		self.sums = self.nodes

		#Targets. Operate independently of nodes for forward/back propagation, so not integrated into self.nodes
		self.targets = [0 for x in range(layers[-1])]

		#Create weights. Indexing works as self.weights[layer][from][to]
		self.weights = [[] for layer in range(2)] #Start with 1 hidden layer, so we'll need 2 sets of weights
		self.weights[0] = [[choice(self.biased_range) for node_to in range(layers[1])] for node_from in range(layers[0])]
		self.weights[1] = [[choice(self.biased_range) for node_to in range(layers[-1])] for node_from in range(layers[1])]


	def add_layer(self):
		#Check if we can actually add any more hidden layers, then add the next scheduled layer
		if self.active_layers < len(self.layer_structure)-2:
			#Add another hidden layer just before the end layer
			self.nodes.insert(-1, [0 for x in range(self.layer_structure[self.active_layers+1])])

			#Generate weights for the new layers, and destroy the previous last-layer weights as they are now useless
			self.weights.insert(-1, [[choice(self.biased_range) 
						for node_to in range(len(self.nodes[-2]))] for node_from in range(len(self.nodes[-3]))])
			self.weights[-1] = [[choice(self.biased_range) 
						for node_to in range(len(self.nodes[-1]))] for node_from in range(len(self.nodes[-2]))]

			#Increment hidden layer counter by 1
			self.active_layers += 1

		#Otherwise tell the user that that's a bad idea
		else:
			return 'ERROR: all hidden layers already applied'


	def cost_normal(self, index):
		#Returns the cost of a specific node using (actual-target)^2
		return (self.nodes[-1][index]-self.targets[index])**2

	def cost_slope(self, index):
		#Returns the _derivative (slope) of the cost for backpropagation
		return (self.nodes[-1][index]-self.targets[index])*2

	def set_inputs(self, inputs):
		#Set input nodes to the input data provided
		self.nodes[0] = inputs

	def set_targets(self, targets):
		#Set target for backpropagation
		self.targets = targets

	def forward_feed(self):
		#Run a try-except so the whole program doesn't stop if there's a piece of missing data
		try:

			#Repeat for every layer except the first one
			for layer in range(1, len(self.nodes)):

				#And for every node in that layer
				for node_to in range(len(self.nodes[layer])):

					#Set node sum to sum of previous nodes*weights-linking-them
					self.sums[layer][node_to] = round(sum([
						self.nodes[layer-1][node_from] * self.weights[layer-1][node_from][node_to] 
						for node_from in range(len(self.nodes[layer-1]))
						]), 4)

				#Map each node sum through the activation function
				self.nodes[layer] = list(map(self.activation_normal, self.sums[layer]))

		except Exception as error:

			#Notify the user of the error
			print(error)
			return 'ERROR: data missing or corrupted'


	def back_propagate(self, learning_rate):
		#Create gradient list and insert initial gradient at output nodes to work from
		slope = [[self.cost_slope(x) for x in range(len(self.nodes[-1]))]]
		layer_length = len(self.nodes) #Cached to speed up process time

		#Repeat for every layer
		for layer in range(1, len(self.nodes)):

			#Create new nested list for that layer's slopes
			slope.append([])

			#For every node in the previous layer
			for node_from in range(len(self.nodes[-(layer+1)])):

				#For every node in the next layer
				for node_to in range(len(self.nodes[-layer])):

					#Calculate the delta for every weight in the layer
					self.weights[-layer][node_from][node_to] -= (slope[layer-1][node_to] * 
																self.activation_derivative(self.sums[-layer][node_to]) * 
																self.nodes[-(layer+1)][node_from] * learning_rate)
				
				if layer != layer_length:
					#Calculate the new slope for the next layer we're going to backpropagate on
					slope[layer].append((sum(slope[layer-1][n] * 
											self.activation_derivative(self.sums[-layer][n]) * 
											self.weights[-layer][node_from][n] 
											for n in range(len(self.sums[-layer])))))