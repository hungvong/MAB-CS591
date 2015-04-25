from BanditArm import BanditArm
import numpy as np

#Initialize variables
k = [17, 8, 30, 9, 36]
i = 10
n = 200

#Initialize bandits
arm1 = BanditArm(k[0],n,i)
arm2 = BanditArm(k[1],n,i)
arm3 = BanditArm(k[2],n,i)
arm4 = BanditArm(k[3],n,i)
arm5 = BanditArm(k[4],n,i)


items_left = [] #List which will hold the number of items left, per round
t = 0 #Round number
p = np.zeros(5)
k_total = np.sum(k)

while (k_total >= 1):

	items_left.extend([k])

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

