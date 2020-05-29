from sys import *
path.append('D:/NetworkLib/tools')
path.append('D:/NetworkLib/networks')

from functions import *
from dnn import *
from handler import *
from random import *
from time import sleep

#Improt and handle our dataset
d = Dataset()
d.data_import('4b_and_gate')
replace = 	{
			'1':1,
			'0':0
			}
d.data_replace(replace)

n = DeepNeuralNetwork([4, 4, 1], 'sigmoid')

for epoch in range(20000):
	n.forward_feed()
	n.back_propagate(0.01)
	print(n.cost_normal(0))