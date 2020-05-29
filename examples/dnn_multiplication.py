#A simple demonstration for a multiplied output I often use to check the main algorithms are working somewhat correctly

from sys import *
path.append('D:/NetworkLib/tools')
path.append('D:/NetworkLib/networks')

from functions import *
from dnn import *
from random import *
from time import sleep

#Create variables and dataset
dataset_in = [x for x in range(100)]
dataset_out = [5*x for x in range(100)]

training_in = []
training_out = []

testing_in = []
testing_out = []

#Split dataset into 75% training 25% testing
for i in range(75):
	index = randint(0, len(dataset_in)-1)

	training_in.append(dataset_in[index])
	training_out.append(dataset_out[index])

	dataset_in.pop(index)
	dataset_out.pop(index)

testing_in = dataset_in
testing_out = dataset_out

costs = []

#Initialize network
n = DeepNeuralNetwork([1, 1, 1], 'leakyRELU')

#Training
for x in range(20000):
	index = randint(0, len(training_in)-1)
	n.set_inputs([training_in[index]])
	n.set_targets([training_out[index]])
	n.forward_feed()
	n.back_propagate(0.000001)

#Testing
for i in range(25):
	n.set_inputs([training_in[i]])
	n.set_targets([training_out[i]])
	n.forward_feed()
	n.back_propagate(0.000001)
	costs.append(n.cost_normal(0))

#Print final cost
print('AVERAGE COST:', sum(costs)/25)