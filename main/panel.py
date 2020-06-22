from sys import *
path.append('D:/NetworkLib/tools')
path.append('D:/NetworkLib/networks')

from tkinter import *
from math import *
from functions import *
from dnn import *
from random import *
from time import sleep
from ast import literal_eval

def convert(rgb):
    return "#%02x%02x%02x" % rgb   

class Panel:

	def __init__(self, layers, activation, lr, update_interval = 5, sample_range = 150):

		#Interface/window
		self.window = Tk()
		self.window.title('Network Control')
		self.c = Canvas(self.window, width = 1000, height = 500, bg = 'black')
		self.c.pack()

		#Network
		self.network = DeepNeuralNetwork(layers, activation)

		#Variables
		self.learning_rate = lr
		self.update_interval = update_interval
		self.epochs = 0
		self.sample_range = sample_range
		self.running = False
		self.layers = layers

		#Cost variables
		self.cost_list = [0]
		self.percentage_list = [0]

		#Graph variables
		self.range_multiplier = 200/sample_range
		self.cost_points = []
		self.cost_average = [0]
		self.percentage_points = []
		self.percentage_average = [0]

		#Interface components
		self.epoch_text = self.c.create_text(60, 25, text = 'EPOCH', fill = 'red', font = ('courier new', 20))
		self.epoch_variable = self.c.create_text(60, 55, text = '0', fill = 'white', font = ('courier new', 15))

		self.cost_text = self.c.create_text(160, 25, text = 'COST', fill = 'red', font = ('courier new', 20))
		self.cost_variable = self.c.create_text(160, 55, text = '0', fill = 'white', font = ('courier new', 15))

		self.percentage_text = self.c.create_text(260, 25, text = 'RATE', fill = 'red', font = ('courier new', 20))
		self.percentage_variable = self.c.create_text(260, 55, text = '0%', fill = 'white', font = ('courier new', 15))

		self.run_text = self.c.create_text(360, 25, text = 'RUN', fill = 'red', font = ('courier new', 20))
		self.run_variable = self.c.create_text(360, 55, text = 'False', fill = 'white', font = ('courier new', 15))

		self.lr_text = self.c.create_text(460, 25, text = 'LR', fill = 'red', font = ('courier new', 20))
		self.lr_variable = self.c.create_text(460, 55, text = str(self.learning_rate), fill = 'white', font = ('courier new', 15))

		self.sample_text = self.c.create_text(560, 25, text = 'SAMPLE', fill = 'red', font = ('courier new', 20))
		self.sample_variable = self.c.create_text(560, 55, text = str(self.sample_range), fill = 'white', font = ('courier new', 15))

		#outputs and targets visualisation
		self.output_circles = []
		self.target_circles = []

		if len(self.network.nodes[-1]) <= 20:

			radius_interval = 8
			vertical_interval = 400/len(self.network.nodes[-1])

			for i in range(len(self.network.nodes[-1])):
				self.output_circles.append(self.c.create_oval(300-radius_interval, (i*vertical_interval)+90-radius_interval, 
								   300+radius_interval, (i*vertical_interval)+90+radius_interval, 
								   fill = 'white', outline = 'white'))
				self.target_circles.append(self.c.create_oval(340-radius_interval, (i*vertical_interval)+90-radius_interval, 
								   340+radius_interval, (i*vertical_interval)+90+radius_interval, 
								   fill = 'white', outline = 'white'))

		#cost graph
		self.cost_graph_x = self.c.create_line(60, 180, 260, 180, fill = 'cyan')
		self.cost_graph_y = self.c.create_line(60, 180, 60, 80, fill = 'cyan')

		self.cost_graph_x_text = self.c.create_text(160, 198, fill = 'yellow', text = 'EPOCH', font = ('courier new', 7))
		#self.cost_graph_y_text = self.c.create_text(27, 130, fill = 'yellow', text = 'COST', font = ('courier new', 7), angle = 90)

		self.cost_graph_x_intervals = []
		self.cost_graph_y_intervals = []

		for i in range(3):
			self.cost_graph_x_intervals.append(
				self.c.create_text((i*100)+60, 190, text = round((i*0.5)*sample_range), font = ('courier new', 7), fill = 'white'))
		for i in range(5):
			self.cost_graph_y_intervals.append(
				self.c.create_text(45, 180-((i*25)), text = i/4, font = ('courier new', 7), fill = 'white'))

		#percentage graph
		self.percentage_graph_x = self.c.create_line(60, 320, 260, 320, fill = 'cyan')
		self.percentage_graph_y = self.c.create_line(60, 320, 60, 220, fill = 'cyan')

		self.percentage_graph_x_text = self.c.create_text(160, 338, fill = 'yellow', text = 'EPOCH', font = ('courier new', 7))
		#self.percentage_graph_y_text = self.c.create_text(27, 270, fill = 'yellow', text = 'RATE', font = ('courier new', 7), angle = 90)

		self.percentage_graph_x_intervals = []
		self.percentage_graph_y_intervals = []

		for i in range(3):
			self.percentage_graph_x_intervals.append(
				self.c.create_text((i*100)+60, 330, text = round((i*0.5)*sample_range), font = ('courier new', 7), fill = 'white'))
		for i in range(5):
			self.percentage_graph_y_intervals.append(
				self.c.create_text(45, 320-((i*25)), text = str(int((i/4)*100)) + '%', font = ('courier new', 7), fill = 'white'))

		#buttons and control
		self.run_button = Button(self.window, bg = 'black', fg = 'white', text = 'RUN', font = ('courier new', 10), command = self.set_run)
		self.pause_button = Button(self.window, bg = 'black', fg = 'white', text = 'PAUSE', font = ('courier new', 10), command = self.set_pause)

		self.lr_entry = Entry(self.window, bg = 'black', fg = 'orange')
		self.lr_button = Button(self.window, bg = 'black', fg = 'white', text = 'LR', font = ('courier new', 10), command = self.adjust_lr)
		self.interval_entry = Entry(self.window, bg = 'black', fg = 'orange')
		self.interval_button = Button(self.window, bg = 'black', fg = 'white', text = 'INT', font = ('courier new', 10), command = self.adjust_sample)
		self.layer_button = Button(self.window, bg = 'black', fg = 'white', text = 'ADD LAYER', font = ('courier new', 10), command = self.network.add_layer)

		self.port_entry = Entry(self.window, bg = 'black', fg = 'orange')
		self.save_button = Button(self.window, bg = 'black', fg = 'white', text = 'SAVE', font = ('courier new', 10), command = self.save_network)
		self.load_button = Button(self.window, bg = 'black', fg = 'white', text = 'LOAD', font = ('courier new', 10), command = self.load_network)
		
		self.run_button.place(x = 880, y = 20, width = 50, height = 25)
		self.pause_button.place(x = 928, y = 20, width = 52, height = 25)

		self.lr_entry.place(x = 880, y = 55, width = 60, height = 25)
		self.lr_button.place(x = 938, y = 55, width = 42, height = 25)
		self.interval_entry.place(x = 880, y = 80, width = 60, height = 25)
		self.interval_button.place(x = 938, y = 80, width = 42, height = 25)
		self.layer_button.place(x = 880, y = 105, width = 100, height = 25)

		self.port_entry.place(x = 880, y = 140, width = 100, height = 25)
		self.save_button.place(x = 880, y = 165, width = 50, height = 25)
		self.load_button.place(x = 928, y = 165, width = 52, height = 25)


	def set_run(self):
		self.running = True

	def set_pause(self):
		self.running = False

	def adjust_lr(self):
		self.learning_rate = float(self.lr_entry.get())

	def adjust_sample(self):
		self.update_interval = float(self.interval_entry.get())

	def save_network(self):
		encoded_weights = [str(x) for x in self.network.weights]
		structure = '\n'.join([str(self.layers), str(self.network.active_layers), ''] + encoded_weights)
		
		save_file = open(str(self.port_entry.get()) + '.txt', 'w+')
		save_file.write(structure)
		save_file.close()

	def load_network(self):
		try:
			load_file = open(str(self.port_entry.get()) + '.txt', 'r+')
			payload = load_file.readlines()
			for x in range(len(payload)):
				payload[x] = payload[x].strip()
			load_file.close()
		except:
			self.port_entry.configure(bg = convert((100, 0, 0)))

		if self.network.active_layers == int(payload[1]):
			if str(self.layers) == payload[0]:
				self.port_entry.configure(bg = convert((0, 100, 0)))
				weights = literal_eval(str(payload[3:len(payload)]))
				for x in range(len(self.network.weights)):
					self.network.weights[x] = literal_eval(weights[x])

			else:
				self.port_entry.configure(bg = convert((100, 0, 0)))
		else:
			self.port_entry.configure(bg = convert((100, 0, 0)))


	def run(self, backprop = True):

		targets = self.network.targets

		if self.running == True:

			self.network.forward_feed()
			if backprop == True:
				self.network.back_propagate(self.learning_rate)

			self.epochs += 1

			#Cost absolute
			self.cost_list.append(sum([self.network.cost_normal(x) for x in range(len(self.network.nodes[-1]))]))
			if len(self.cost_list) > self.sample_range:
				self.cost_list.pop(0)

			#Cost average
			self.cost_average.append(round(sum(self.cost_list)/len(self.cost_list), 3))
			if len(self.cost_average) > self.sample_range:
				self.cost_average.pop(0)

			#Percentage absolute
			if targets.index(max(targets)) == self.network.nodes[-1].index(max(self.network.nodes[-1])):
				self.percentage_list.append(1)
			else:
				self.percentage_list.append(0)
			if len(self.percentage_list) > self.sample_range:
				self.percentage_list.pop(0)

			#Percentage average
			self.percentage_average.append(round((sum(self.percentage_list)/len(self.percentage_list))*100, 3))
			if len(self.percentage_average) > self.sample_range:
				self.percentage_average.pop(0)

		if self.epochs % self.update_interval == 0 or self.running == False:

			#Update text variables
			self.c.itemconfig(self.epoch_variable, text = self.epochs)
			self.c.itemconfig(self.cost_variable, text = round(sum(self.cost_list)/len(self.cost_list), 3))
			self.c.itemconfig(self.percentage_variable, text = str(round((sum(self.percentage_list)/len(self.percentage_list))*100, 2)) + '%')
			self.c.itemconfig(self.run_variable, text = str(self.running))
			self.c.itemconfig(self.lr_variable, text = str(self.learning_rate))

			#Update node visualisation
			multiplier = 255/(ceil(max(self.network.nodes[-1] + self.network.targets))+0.0001)
			for i in range(len(self.output_circles)):

				x = floor(multiplier*self.network.nodes[-1][i])
				if x >= 0:
					colour = convert((0, x, 0))
				else:
					colour = convert((-x, 0, 0))
				self.c.itemconfig(self.output_circles[i], fill = colour)

				x = floor(multiplier*self.network.targets[i])
				if x >= 0:
					colour = convert((0, x, 0))
				else:
					colour = convert((-x, 0, 0))
				self.c.itemconfig(self.target_circles[i], fill = colour)

			#Update graphs
			if self.epochs < self.sample_range:
				text_start = 0
			else:
				text_start = self.epochs - self.sample_range

			for x in range(len(self.cost_graph_x_intervals)):
				self.c.itemconfig(self.cost_graph_x_intervals[x], text = str(text_start+((x/(len(self.cost_graph_x_intervals)-1))*self.sample_range)))
			for y in range(len(self.cost_graph_y_intervals)):
				self.c.itemconfig(self.cost_graph_y_intervals[y], text = round((y/(len(self.cost_graph_y_intervals)-1)) * max(self.cost_average), 3))

			for x in self.cost_points:
				self.c.delete(x)

			self.cost_points = []

			y_multiplier = 100/(max(self.cost_average)+0.001)

			for i in range(len(self.cost_average)):
				x = (i*self.range_multiplier)+60
				y = 180-((self.cost_average[i]*y_multiplier))
				self.cost_points.append(self.c.create_oval(x-2, y-2, x+2, y+2, fill = 'blue', outline = 'blue'))

			#Update graphs
			for x in range(len(self.percentage_graph_x_intervals)):
				self.c.itemconfig(self.percentage_graph_x_intervals[x], text = str(text_start+((x/(len(self.percentage_graph_x_intervals)-1))*self.sample_range)))

			for x in self.percentage_points:
				self.c.delete(x)

			self.percentage_points = []

			for i in range(len(self.percentage_average)):
				x = (i*self.range_multiplier)+60
				y = 320-((self.percentage_average[i]))
				self.percentage_points.append(self.c.create_oval(x-2, y-2, x+2, y+2, fill = 'blue', outline = 'blue'))

		self.window.update()