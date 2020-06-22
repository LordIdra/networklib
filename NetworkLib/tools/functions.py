from time import *
from random import randint

def fromRGB(r, g, b):
	return f'#{r:02x}{g:02x}{b:02x}'

def toRGB(hex):
	return (int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16))

def distributedRange():

	ranges = []
	for number in range(200):
		#abs() lets us automatically invert negatives
		for iterations in range((100-number)**2):
			ranges.append((100-number)/100)

	return ranges

class timer:

	def __init__(self):
		self.timestart = 0
		self.timeend = 0
		self.timeduration = 0

	def start(self):
		self.timestart = int(round(time() * 100000)) / 100000

	def stop(self):
		self.timeend = int(round(time() * 100000)) / 100000
		self.timeduration = self.timeend-self.timestart
		return self.timeduration