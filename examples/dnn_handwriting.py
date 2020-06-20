from sys import *
path.append('D:/NetworkLib/tools')
path.append('D:/NetworkLib/networks')

from tkinter import *
from math import *
from functions import *
from dnn import *
from random import *
from time import sleep
import csv

def convert(r, g, b):
    return "#%02x%02x%02x" % (int(r), int(g), int(b))

class plane:

	def __init__(self, plot_span):

		self.window = Tk()
		self.window.title('Complex Visualisation')

		self.c = Canvas(self.window, width = 500, height = 500, bg = 'black')
		self.c.pack()

		self.queue = []
		self.points = []

		self.plot_span = plot_span

		self.x_lines = [self.c.create_line(50, (x*20)+50, 450, (x*20)+50, fill = convert(100, 100, 100)) for x in range(0, 21)]
		self.y_lines = [self.c.create_line((y*20)+50, 50, (y*20)+50, 450, fill = convert(100, 100, 100)) for y in range(0, 21)]

		self.x_text = [self.c.create_text(250, (x*20)+50, text = int((10*plot_span)-(x*plot_span)), fill = convert(255, 255, 255), font = ('', 7)) for x in range(0, 21)]
		self.y_text = [self.c.create_text((x*20)+50, 250, text = int((x*plot_span)-(10*plot_span)), fill = convert(255, 255, 255), font = ('', 7)) for x in range(0, 21)]


	def plot(self, x, y, shade):

		y -= y*2

		try:
			self.points.append(self.c.create_oval(
				((x*20)/self.plot_span)+246, 
				((y*20)/self.plot_span)+246, 
				((x*20)/self.plot_span)+254, 
				((y*20)/self.plot_span)+254, 
				fill = convert(shade, shade, shade)))
		except:
			pass



image_size = 28 # width and length
no_of_different_labels = 10 #  i.e. 0, 1, 2, 3, ..., 9
image_pixels = image_size * image_size

#train_data = ps.read_csv('../datasets/mnist_test.csv')
test_data = list(csv.reader(open('../datasets/mnist_train.csv')))

p = plane(3)

n = DeepNeuralNetwork([784, 600, 400, 200, 10], 'tanh')

normal_value = 0.99-(1.98/255)

costs = []
percentages = []

for dataset in range(50000):

	if dataset == 1000:
		n.add_layer()
	elif dataset == 3000:
		n.add_layer()
	elif dataset == 8000:
		n.add_layer()

	inputs = []
	targets = [-0.9 for x in range(10)]
	targets[int(test_data[dataset][0])] = 0.9

	for value in range(1, 784):

		x = int(test_data[dataset][value])

		if x != 0:
			p.plot((value%28), 28-(value//28), x)

		inputs.append(x*normal_value)

	n.set_inputs(inputs)
	n.set_targets(targets)

	n.forward_feed()
	n.back_propagate(0.0002)

	cost = sum(n.cost_normal(x) for x in range(10))
	costs.append(cost)

	if len(costs) > 100:
		costs.pop(0)

	if n.nodes[-1].index(max(n.nodes[-1])) == targets.index(max(targets)):
		matched = 1
	else:
		matched = 0

	percentages.append(matched)

	if len(percentages) > 100:
		percentages.pop(0)

	print('RAW: ', n.nodes[-1])
	print('TARGET: ', targets.index(max(targets)))
	print('OUTPUT: ', [n.nodes[-1].index(i) for i in list(reversed(sorted(n.nodes[-1])))])
	print('RATE: ', str((sum(percentages)/len(percentages))*100) + '%')
	print('COST: ', dataset, sum(costs)/len(costs))
	print('')

	p.window.update()
	for x in p.points:
		p.c.delete(x)
	p.points = []

p.window.mainloop()
