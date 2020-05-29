#Data handling tool for preparing datasets

from sys import *
path.append('D:/NetworkLib/tools')
path.append('D:/NetworkLib/networks')
path.append('D:/NetworkLib/datasets')

from functions import *
from dnn import *
from random import *
from time import sleep
from pathlib import *
from ast import *

#Useful function to convert a string representation of a list into an actual list
def toList(x):
	#Split list into input and targets
	inputs = x[x.find('['):x.find(']')+1]
	targets = x[x.find(']')+3:len(x)]
	return [list(map(str, literal_eval(inputs))), list(map(str, literal_eval(targets)))]

class Dataset:

	def __init__(self):
		self.data = ''

	def data_import(self, x):
		try:
			path = Path(__file__).parent / ('../datasets/' + str(x) + '.txt') #Create a path to the target dataset
			self.data = path.open().read().splitlines() #Open and format the dataset
			self.data = list(map(toList, self.data)) #Convert the string representations of lists into list objects

		except Exception as error:
			print(error)
			print('ERROR: dataset not found')

	def data_replace(self, replacement_dict):
		for pair in range(len(self.data)):

			for inputs in range(len(self.data[pair][0])):

				#Try except will ensure that any corrupt data will be ignored
				try:
					#Find the input as a key in the dictionary and set it to the corresponding value
					self.data[pair][0][inputs] = replacement_dict[self.data[pair][0][inputs]]
				except Exception as e:
					print(e)
					return 'ERROR: could not find', self.data[pair][0][inputs], 'in replacement dictionary'

			for targets in range(len(self.data[pair][1])):

				#Try except will ensure that any corrupt data will be ignored
				try:
					#Find the target as a key in the dictionary and set it to the corresponding value
					self.data[pair][1][targets] = replacement_dict[str(self.data[pair][1][targets])]
				except Exception as e:
					print(e)
					return 'ERROR: could not find', self.data[pair][0][inputs], 'in replacement dictionary'

	def data_get(self):
		return self.data