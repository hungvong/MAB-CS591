import numpy as np
from math import log10
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import random

k = 100. #Number of items
n = 30. #number of buyers
i = 10 #total number of prices in list
Nt = {} #Dictionary which holds the number of times a price has occurred in a round
t = 0 #Stores current round
p_list = []

#compute delta
delta = (k**(-1./3.)) * ((log10(n))**(2./3.))

#compute alpha
alpha = np.floor(log10(float(n)))

#Initialize list of prices & dictionary
P = np.zeros(i)
for jj in range (1, i+1):
	P[jj-1] = delta * (1 + delta)**jj
	Nt[P[jj-1]] = 0;

#Initialize rt, St
rt = {}
St = {}

#input kt dictionary
kt = dict()
for price in P:
	kt[price] = random.randint(0,20)

while (k >= 1):

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

kt_df = pd.DataFrame(kt.items(),columns=['Price','N_sold'])
kt_df = kt_df.sort(['Price'])

#Plot the results
fig = plt.figure()
ax = fig.gca(projection='3d')
t_vector = np.arange(len(P))+1#np.arange(t) + 1
ax.plot(t_vector, P, kt_df['N_sold'])
ax.set_xlabel('Round')
ax.set_ylabel('Price')
ax.set_zlabel('Number of items sold')
plt.show()
