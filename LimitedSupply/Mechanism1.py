import numpy as np
from math import log10
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import random

k = 10. #Number of items
n = 50. #number of buyers
i = 10 #total number of prices in list
Nt = {} #Dictionary which holds the number of times a price has occurred in a round
t = 0 #Stores current round
p_list = []
items_left = [] #List which will hold the number of items left, per round

#compute delta
delta = (k**(-1./3.)) * ((log10(n))**(2./3.))

#compute alpha
alpha = np.floor(log10(float(n)))

#Initialize list of prices & dictionary
P = np.zeros(i)
for jj in range (1, i+1):
	P[jj-1] = delta * (1 + delta)**jj
	Nt[P[jj-1]] = 0;

#Randomly choose each customer's "ideal" price
max_price = np.max(P)
ideal_prices = np.random.random(n) * (max_price + 2)

#Initialize rt, St, g
rt = {}
St = {}
g = {} 

#input kt dictionary
kt = dict()
test = 9
for price in P:
	kt[price] = test
	test -= 1

while (k >= 1):

	items_left.extend([k])

	#Update g
	player = 0
	temp = {}
	for player_price in ideal_prices:
		temp[player] = player_price / P
		player += 1

	#Store gain vector for the current round
	g[t] = temp 

	It_vals = []

	#Find which price minimizes It
	for jj in range (0,i):
		p = P[jj]

		#Compute St[p]
		try:
			St[p] = float(kt[p]) / Nt[p]
		except ZeroDivisionError:
			St[p] = 1

		#Compute rt[p]
		rt[p] = (alpha / (Nt[p] + 1.)) + np.sqrt( (alpha * St[p]) / (Nt[p] + 1.) )

		#Compute It
		It = p * np.min((k, n*(St[p] + rt[p])))

		It_vals.extend([It])

	idx = np.argmax(It_vals)
	p = P[idx]
	p_list.extend([p])

	#Add chosen price to Nt
	Nt[p] += 1

	t += 1

	k -= kt[p]
	#n -= kt[p]

kt_df = pd.DataFrame(kt.items(),columns=['Price','N_sold'])
kt_df = kt_df.sort(['Price'])


# ============= COMPUTE RAGRET ============ #

#Get forecaster's chosen arm: It = {1, ... , K}



'''
#No Ragrets
R = np.zeros((n,t))

for round_i in range (0, t):
	gain_vector = g[round_i]

	for player in range(0, n):
		expected_values = []

		for i in range (0, t):
			#Compute max(E sum(gi,t))
			expected_val1 = gain_vector[player][i] += 1
'''




#Plot the results

#Price vs. # of Items Sold
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(kt_df['Price'],kt_df['N_sold'])
ax.set_title('Price vs. Number of Items Sold')
ax.set_xlabel('Price')
ax.set_ylabel('Number of Items Sold')
plt.show()

#Number of Items left
t_vector = np.arange(len(items_left))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t_vector,items_left)
ax.set_title('Number of Items Left')
ax.set_xlabel('Round')
ax.set_ylabel('# of Items')
plt.show()

fig = plt.figure()
ax = fig.gca(projection='3d')
t_vector = np.arange(len(P))+1#np.arange(t) + 1
ax.plot(t_vector, P, kt_df['N_sold'])
ax.set_xlabel('Round')
ax.set_ylabel('Price')
ax.set_zlabel('Number of items sold')
plt.show()

