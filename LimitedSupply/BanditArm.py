#Multi-Armed Bandit Class
import numpy as np
from math import log10
import math
import pandas as pd
from random import random

class BanditArm:

	def __init__(self, k, n, i, mechanism):

		#For mechanism #1:
		if (mechanism == 1):
			self.k = k #number of items
			self.n = n #number of buyers
			self.i = i #number of total possible prices

			# =============== Initialize these dictionaries ============= #
			self.rt = {}  #r_t variable
			self.St = {}  #S_t variable
			self.Nt = {}

			# ================== Initialize these lists ================= #
			self.p_list1 = [] #Holds a list of prices as they change per round


			# ================== Compute Alpha, Delta =================== #
			self.alpha1 = np.floor(log10(float(n)))
			self.delta1 = (k**(-1./3.)) * ((log10(n))**(2./3.))


			# =================== Initialize Variables ================== #
			#Array of possible prices
			P = np.zeros(i)
			for jj in range (1, i+1):
				P[jj-1] = self.delta1 * (1 + self.delta1)**jj
				self.Nt[P[jj-1]] = 0;

			self.P = P

			#Number of items sold per price
			self.kt = dict()
			for price in P:
				self.kt[price] = 0

		#Mechanism #2:
		elif (mechanism == 2):
			self.k = k #number of items
			self.n = n #number of buyers
			self.i = i #number of possible prices

			# ======== Compute Alpha, Delta, Epsilon, and Delta ======== #
			self.epsilon = k**(-0.25) #Compute epsilon
			self.delta2 = ((1./k) * log10(k))**(0.25) #Delta function
			self.alpha2 =  (float(k)/float(n))**(1-self.delta2) #Compute alpha
			self.gamma = np.min((self.alpha2, 1./math.e)) #Compute gamma

			# =============== Initialize these variables =============== #
			self.l = -1
			self.Sl_max = (1 + self.delta2) * self.alpha2
			self.R_max = 0
			self.l_max = 0
			self.Sl = 0
			self.Rl = 0

			#Initialize lists
			self.Sl_list = [] #Saves history of Sl, per round
			self.Rl_list = [] #Saves history of Rl, per round
			self.p_list = [] #Saves history of prices, per round

		#Combination of mechanism 1 and 2 -- call it "mechanism 3"
		elif (mechanism == 3):
			self.k = k #number of items
			self.n = n #number of buyers
			self.i = i #number of total possible prices

			######## SET UP MECHANISM 1

			# =============== Initialize these dictionaries ============= #
			self.rt = {}  #r_t variable
			self.St = {}  #S_t variable
			self.Nt = {}

			# ================== Initialize these lists ================= #
			self.p_list1 = [] #Holds a list of prices as they change per round


			# ================== Compute Alpha, Delta =================== #
			self.alpha1 = np.floor(log10(float(n)))
			self.delta1 = (k**(-1./3.)) * ((log10(n))**(2./3.))


			# =================== Initialize Variables ================== #
			#Array of possible prices
			P = np.zeros(i)
			for jj in range (1, i+1):
				P[jj-1] = self.delta1 * (1 + self.delta1)**jj
				self.Nt[P[jj-1]] = 0;

			self.P = P

			#Number of items sold per price
			self.kt = dict()
			for price in P:
				self.kt[price] = 0


			######## SET UP MECHANISM 2

			# ======== Compute Alpha, Delta, Epsilon, and Delta ======== #
			self.epsilon = k**(-0.25) #Compute epsilon
			self.delta2 = ((1./k) * log10(k))**(0.25) #Delta function
			self.alpha2 =  (float(k)/float(n))**(1-self.delta) #Compute alpha
			self.gamma = np.min((self.alpha2, 1./math.e)) #Compute gamma

			# =============== Initialize these variables =============== #
			self.l = -1
			self.Sl_max = (1 + self.delta2) * self.alpha2
			self.R_max = 0
			self.l_max = 0
			self.Sl = 0
			self.Rl = 0

			#Initialize lists
			self.Sl_list = [] #Saves history of Sl, per round
			self.Rl_list = [] #Saves history of Rl, per round
			self.p_list2 = [] #Saves history of prices, per round

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
				self.rt[p] = (self.alpha1 / (self.Nt[p] + 1.)) + np.sqrt( (self.alpha1 * self.St[p]) / (self.Nt[p] + 1.) )

				#Compute It
				It = p * np.min((self.k, self.n*(self.St[p] + self.rt[p])))
				It_vals.extend([It])

			idx = np.argmax(It_vals)
			p = self.P[idx]
			self.p_list1.extend([p])

			#Add chosen price to Nt
			self.Nt[p] += 1
			self.kt[p] 

			return p

		else:
			return 99999

	#Update the value of K
	def update_k(self,p):
		self.k -= self.kt[p]

	#Update kt
	def update_kt(self,p):
		self.kt[p] += 1

	#Update n and alpha
	def decrement_n(self):
		self.n -= 1

		try:
			self.alpha1 = np.floor(log10(float(self.n)))
		except ValueError:
			self.alpha1 = 0

		
	#Compute pl
	def compute_pl(self):
		self.l = self.l + 1
		self.pl = (1. + self.delta2)**(-self.l)
		self.p_list2.extend([self.pl])

		return self.pl

	#                                       n
	#Offer price pl to m = delta * ----------------------- agents
	#                             log_{1+delta}(1/epsilon) 
	def offer_pl(self):
		b = 1. + self.delta2 #log base
		log_result = log10(1./self.epsilon)/log10(b)
		m = self.delta2 * (self.n / log_result)
		m = int(np.ceil(m))

		return m

	def computeSlandPl(self,m,pl,ideal_prices):
		accept = 0.
		total = 0.
		for agent in range (0,int(m)):
			if (ideal_prices[agent] > pl):
				accept += 1

			total += 1
		self.Sl = float(accept) / total
		self.Sl_list.extend([self.Sl])

		self.Rl = pl * self.Sl
		self.p_list2.extend([pl])


