#Multi-Armed Bandit Class
import numpy as np
from math import log10
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import random

class BanditArm:

	def __init__(self, k, n, i):

		self.k = k #number of items
		self.n = n #number of buyers
		self.i = i #number of total possible prices

		# ============== Initialize these dictionaries ============= #
		self.rt = {}  #r_t variable
		self.St = {}  #S_t variable
		self.Nt = {}

		# ================== Initialize these lists ================= #
		self.p_list = [] #Holds a list of prices as they change per round


		# ================== Compute Alpha, Delta =================== #
		self.alpha = np.floor(log10(float(n)))
		self.delta = (k**(-1./3.)) * ((log10(n))**(2./3.))


		# =================== Initialize Variables ================== #
		#Array of possible prices
		P = np.zeros(i)
		for jj in range (1, i+1):
			P[jj-1] = self.delta * (1 + self.delta)**jj
			self.Nt[P[jj-1]] = 0;

		self.P = P

		#Randomly choose each customer's "ideal" price
		max_price = np.max(P)
		self.ideal_prices = np.random.random(n) * (max_price + 1)

		#Number of items sold per price
		self.kt = dict()
		test = 9
		for price in P:
			self.kt[price] = test
			test -= 1

	#Find the p that minimizes It
	def minimizeIt(self):

		if (self.k > 0):
			'''
			This function finds which price minimizes the variable It
			'''

			It_vals = []

			for jj in range (0,self.i):
				p = self.P[jj]

				#Compute St[p]
				try:
					self.St[p] = float(self.kt[p]) / self.Nt[p]
				except ZeroDivisionError:
					self.St[p] = 1

				#Compute rt[p]
				self.rt[p] = (self.alpha / (self.Nt[p] + 1.)) + np.sqrt( (self.alpha * self.St[p]) / (self.Nt[p] + 1.) )

				#Compute It
				It = p * np.min((self.k, self.n*(self.St[p] + self.rt[p])))
				It_vals.extend([It])

			idx = np.argmax(It_vals)
			p = self.P[idx]
			self.p_list.extend([p])

			#Add chosen price to Nt
			self.Nt[p] += 1

			return p

		else:
			return 99999

	#Update the value of K
	def update_k(self,p):
		self.k -= self.kt[p]


		