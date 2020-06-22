from sys import *
path.append('D:/NetworkLib/main')

from panel import Panel
import csv

p = Panel([784, 400, 400, 200, 10], 'tanh', 0.0001, update_interval = 5, sample_range = 400)

print('IMPORTING TRAINING DATA...')
train_data = list(csv.reader(open('../datasets/mnist_train.csv')))
print('TRAINING DATA IMPORTED\n')
print('IMPORTING TESTING DATA...')
test_data = list(csv.reader(open('../datasets/mnist_test.csv')))
print('TESTING DATA IMPORTED\n')

normal_value = 0.99-(1.98/255)
to_break = False

while to_break == False:

	if p.running == True:
		inputs = [int(train_data[p.epochs][value])*normal_value for value in range(1, 784)]
		targets = [-0.99 for i in range(10)]
		targets[int(train_data[p.epochs][0])] = 0.99

		p.network.set_inputs(inputs)
		p.network.set_targets(targets)

	if p.epochs > 40000:
		to_break = True

	p.run()

print('TRAINING PHASE COMPLETE. PRESS RUN TO CONTINUE.')

p.running = False
to_break = False
percentage_full = []

while to_break == False:

	if p.running == True:
		inputs = [int(test_data[p.epochs][value])*normal_value for value in range(1, 784)]
		targets = [-0.99 for i in range(10)]
		targets[int(test_data[p.epochs][0])] = 0.99

		p.network.set_inputs(inputs)
		p.network.set_targets(targets)

		percentage_full.append(p.percentage_list[-1])

		p.epochs += 1

	if p.epochs > 44000:
		to_break = True

	p.run(False)

print(str(sum(percentage_full)/len(percentage_full)*100) + '%')

while True:
	p.window.update()