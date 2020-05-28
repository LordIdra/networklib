from math import exp, tanh
from functions import timer

'''Logistic function'''
#RANGE: 0 to -1
#ADVANTAGES: smooth gradient, _normalises values, clear prediction ability
#DISADVANTAGES: prone to vanishing gradient problem, computationally expensive
def sigmoid_normal(x):
	return (exp(x)/(exp(x)+1))

def sigmoid_derivative(x):
	return sigmoid_normal(x) * (1-sigmoid_normal(x))


'''Tan-h'''
#RANGE: -1 to 1
#ADVANTAGES: zero-centred as opposed to sigmoid, smooth gradient, _normalises values, clear prediction ability
#DISADVANTAGES: prone to vanishing gradient problem, computationally expensive
def tanh_normal(x):
	return tanh(x)

def tanh_derivative(x):
	return 1-(tanh(x)**2)


#Linear Rectifier
#RANGE: 0 to ∞
#ADVANTAGES: computationally efficient, non-linear
#DISADVANTAGES: prone to dying relu problem (nodes stuck on 0)
def linearRELU_normal(x):
	if x > 1:
		return x
	else:
		return 0

def linearRELU_derivative(x):
	if x > 1:
		return 1
	else:
		return 0


'''Leaky rectifier'''
#RANGE: -∞ to ∞
#ADVANTAGES: prevents dying relu problem, computationally efficient, non-linear
#DISADANTAGES: inconsistent with negatives
def leakyRELU_normal(x):
	if x > 1:
		return x
	else:
		return 0.1*x
		
def leakyRELU_derivative(x):
	if x > 1:
		return 1
	else:
		return 0.1

i = 0

def run_benchmark(t = 5000000, x = 5):

	print('SIGMOID')
	t_sigmoid1 = timer()
	t_sigmoid1.start()
	for x in range(t):
		i = sigmoid_normal(10)
	print(t_sigmoid1.stop())
	t_sigmoid2 = timer()
	t_sigmoid2.start()
	for x in range(t):
		i = sigmoid_derivative(10)
	print(t_sigmoid2.stop())

	print('TANH')
	t_tan1 = timer()
	t_tan1.start()
	for x in range(t):
		i = tanh_normal(10)
	print(t_tan1.stop())
	t_tan2 = timer()
	t_tan2.start()
	for x in range(t):
		i = tanh_derivative(10)
	print(t_tan2.stop())

	print('LINEAR-RELU')
	t_lr1 = timer()
	t_lr1.start()
	for x in range(t):
		i = linearRELU_normal(10)
	print(t_lr1.stop())
	t_lr2 = timer()
	t_lr2.start()
	for x in range(t):
		i = linearRELU_derivative(10)
	print(t_lr2.stop())

	print('LEAKY-RELU')
	t_er1 = timer()
	t_er1.start()
	for x in range(t):
		i = leakyRELU_normal(10)
	print(t_er1.stop())
	t_er2 = timer()
	t_er2.start()
	for x in range(t):
		i = leakyRELU_derivative(10)
	print(t_er2.stop())
