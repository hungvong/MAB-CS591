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
arm1 = BanditArm(k[0],n,i,1)
arm2 = BanditArm(k[1],n,i,1)
arm3 = BanditArm(k[2],n,i,1)
arm4 = BanditArm(k[3],n,i,1)
arm5 = BanditArm(k[4],n,i,1)

#Randomly choose each customer's "ideal" price
max_price = np.max([arm1.P, arm2.P, arm3.P, arm4.P, arm5.P])
ideal_prices = np.random.random(n) * (max_price + 1)


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

	if (min_price == 50000):
		break;

	#Keep track of the bandit prices per round
	temp = np.copy(p)

	for value in range (0,len(temp)):
		if (temp[value] == 99999):
			temp[value] = 0
	price_per_round.append(temp)

	#Check if each player's ideal value is greater than the current price
	item_bought = False
	for yy in range (0,len(ideal_prices)):
		if (ideal_prices[yy] >= min_price):
			ideal_prices = np.delete(ideal_prices,yy) #remove the buyer from the list
			item_bought = True
			break;


	#Keep track of the overall minimum price and the round in which it occurs
	if (min_price < overall_minimum_price):
		overall_minimum_price = min_price
		overall_minimum_round = t
	
	#Update k_total if an item is bought
	if (item_bought):
		if (min_indx == 0):
			arm1.update_k(min_price)
			arm1.update_kt(min_price)

		elif (min_indx == 1):
			arm2.update_k(min_price)
			arm2.update_kt(min_price)
		
		elif (min_indx == 2):
			arm3.update_k(min_price)
			arm3.update_kt(min_price)

		elif (min_indx == 3):
			arm4.update_k(min_price)
			arm4.update_kt(min_price)

		elif (min_indx == 4):
			arm5.update_k(min_price)
			arm5.update_kt(min_price)


		k_total -= 1

		#Decrement n
		arm1.decrement_n()
		arm2.decrement_n()
		arm3.decrement_n()
		arm4.decrement_n()
		arm5.decrement_n()

		n -= 1

	#Increment round number
	t += 1
	print "t =",t
	print "n =",n
	print "k_total = ",k_total
	print "====================="

	if (n == 0):
		break;

#Plot the results
arm1_kt_df = pd.DataFrame(arm1.kt.items(),columns=['Price','N_sold'])
arm1_kt_df = arm1_kt_df.sort(['Price'])
arm2_kt_df = pd.DataFrame(arm2.kt.items(),columns=['Price','N_sold'])
arm2_kt_df = arm2_kt_df.sort(['Price'])
arm3_kt_df = pd.DataFrame(arm3.kt.items(),columns=['Price','N_sold'])
arm3_kt_df = arm3_kt_df.sort(['Price'])
arm4_kt_df = pd.DataFrame(arm4.kt.items(),columns=['Price','N_sold'])
arm4_kt_df = arm4_kt_df.sort(['Price'])
arm5_kt_df = pd.DataFrame(arm5.kt.items(),columns=['Price','N_sold'])
arm5_kt_df = arm5_kt_df.sort(['Price'])

#Price vs. # of Items Sold
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(arm1_kt_df['Price'],arm1_kt_df['N_sold'])
ax.plot(arm2_kt_df['Price'],arm2_kt_df['N_sold'],'r')
ax.plot(arm3_kt_df['Price'],arm3_kt_df['N_sold'],'g')
ax.plot(arm4_kt_df['Price'],arm4_kt_df['N_sold'],'k')
ax.plot(arm5_kt_df['Price'],arm5_kt_df['N_sold'],'m')
ax.legend(['Arm 1', 'Arm 2', 'Arm 3', 'Arm 4', 'Arm 5'])
ax.set_title('Price vs. Number of Items Sold')
ax.set_xlabel('Price')
ax.set_ylabel('Number of Items Sold')
plt.show()

#Number of Items left
t_vector = np.arange(t)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t_vector,price_per_round)
ax.legend(['Arm 1', 'Arm 2', 'Arm 3', 'Arm 4', 'Arm 5'],loc=4)
ax.set_title('Price per Round')
ax.set_xlabel('Round')
ax.set_ylabel('Price')
#ax.set_ylim([0,360])
plt.show()

#Plot price per round

