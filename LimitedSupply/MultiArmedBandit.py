from BanditArm import BanditArm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Initialize variables
k = [7, 8, 14, 9, 28]
i = 10
n = 100

#Initialize bandits
arm1 = BanditArm(k[0],n,i)
arm2 = BanditArm(k[1],n,i)
arm3 = BanditArm(k[2],n,i)
arm4 = BanditArm(k[3],n,i)
arm5 = BanditArm(k[4],n,i)


#Initialize overall min price and round index
overall_minimum_price = 50000
overall_minimum_round = -1

arm1_items_left = [] #List which will hold the number of items left, per round
arm2_items_left = [] #List which will hold the number of items left, per round
arm3_items_left = [] #List which will hold the number of items left, per round
arm4_items_left = [] #List which will hold the number of items left, per round
arm5_items_left = [] #List which will hold the number of items left, per round

t = 0 #Round number
p = np.zeros(5)
k_total = np.sum(k)

price_per_round = []

while (k_total >= 1):
#if (True):

	arm1_items_left.extend([arm1.k])
	arm2_items_left.extend([arm2.k])
	arm3_items_left.extend([arm3.k])
	arm4_items_left.extend([arm4.k])
	arm5_items_left.extend([arm5.k])

	#Maximize It for each bandit arm
	p[0] = arm1.minimizeIt()
	p[1] = arm2.minimizeIt()
	p[2] = arm3.minimizeIt()
	p[3] = arm4.minimizeIt()
	p[4] = arm5.minimizeIt()

	#Select the minimum price of all the prices
	min_price = 50000
	min_indx = -1
	for ll in range (0, len(p)):
		if (p[ll] < min_price):
			min_price = p[ll]
			min_indx = ll

	#Keep track of the bandit prices per round
	temp = np.copy(p)

	for value in range (0,len(temp)):
		if (temp[value] == 99999):
			temp[value] = 0
	price_per_round.append(temp)

	#Keep track of the overall minimum price and the round in which it occurs
	if (min_price < overall_minimum_price):
		overall_minimum_price = min_price
		overall_minimum_round = t
	
	#Update k_total
	if (min_indx == 0):
		arm1.update_k(min_price)
		k_total -= arm1.kt[min_price]

	elif (min_indx == 1):
		arm2.update_k(min_price)
		k_total -= arm2.kt[min_price]
	
	elif (min_indx == 2):
		arm3.update_k(min_price)
		k_total -= arm3.kt[min_price]

	elif (min_indx == 3):
		arm4.update_k(min_price)
		k_total -= arm4.kt[min_price]

	elif (min_indx == 4):
		arm5.update_k(min_price)
		k_total -= arm5.kt[min_price]

	#Increment round number
	t += 1

print t


#Plot the results
arm1_kt_df = pd.DataFrame(arm1.kt.items(),columns=['Price','N_sold'])
arm1_kt_df = arm1_kt_df.sort(['Price'])
arm2_kt_df = pd.DataFrame(arm1.kt.items(),columns=['Price','N_sold'])
arm2_kt_df = arm2_kt_df.sort(['Price'])
arm3_kt_df = pd.DataFrame(arm1.kt.items(),columns=['Price','N_sold'])
arm3_kt_df = arm3_kt_df.sort(['Price'])
arm4_kt_df = pd.DataFrame(arm1.kt.items(),columns=['Price','N_sold'])
arm4_kt_df = arm4_kt_df.sort(['Price'])
arm5_kt_df = pd.DataFrame(arm1.kt.items(),columns=['Price','N_sold'])
arm5_kt_df = arm5_kt_df.sort(['Price'])

#Price vs. # of Items Sold
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(arm1_kt_df['Price'],arm1_kt_df['N_sold'])
ax.plot(arm2_kt_df['Price'],arm2_kt_df['N_sold'],'r')
ax.plot(arm3_kt_df['Price'],arm3_kt_df['N_sold'],'g')
ax.plot(arm4_kt_df['Price'],arm4_kt_df['N_sold'],'k')
ax.plot(arm5_kt_df['Price'],arm5_kt_df['N_sold'],'m')
ax.set_title('Price vs. Number of Items Sold')
ax.set_xlabel('Price')
ax.set_ylabel('Number of Items Sold')
plt.show()

#Number of Items left
t_vector = np.arange(t)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t_vector,price_per_round)
ax.legend(['Arm 1', 'Arm 2', 'Arm 3', 'Arm 4', 'Arm 5'])
ax.set_title('Price per Round')
ax.set_xlabel('Round')
ax.set_ylabel('Price')
plt.show()

#Plot price per round

