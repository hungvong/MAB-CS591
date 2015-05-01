from BanditArm import BanditArm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#============== Initialize Mech 2 ================#

#Initialize variables
k = [7, 8, 14, 9, 28]
i = 10

#Initialize p and find k_total
pl = np.zeros(5)
m = np.zeros(5)
k_total = np.sum(k)
n = 10^(k_total)

#Randomly choose each customer's "ideal" price
max_price = 1
ideal_prices = np.random.random(n) * (max_price + 1)


#============== Initialize Mech 1 ================#

#Randomly choose each customer's "ideal" price
max_price = np.max([arm1.P, arm2.P, arm3.P, arm4.P, arm5.P])
ideal_prices = np.random.random(n) * (max_price + 1)


#Initialize overall min price and round index
overall_minimum_price = 50000
overall_minimum_round = -1

t = 0 #Round number
p = np.zeros(5)
k_total = np.sum(k)

price_per_round = []


#Initialize bandits
arm1 = BanditArm(k[0],n,i,3)
arm2 = BanditArm(k[1],n,i,3)
arm3 = BanditArm(k[2],n,i,3)
arm4 = BanditArm(k[3],n,i,3)
arm5 = BanditArm(k[4],n,i,3)


while (k_total >= 1):
#if (True):

	arm1_stop = False
	arm2_stop = False
	arm3_stop = False
	arm4_stop = False
	arm5_stop = False


	#============= MECHANISM 1 =============#

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


	#============= MECHANISM 2 ==============#

	while (True):

		if (arm1_stop == False):
			pl[0] = arm1.compute_pl()
			m[0] = arm1.offer_pl()
			arm1.computeSlandPl(m[0],pl[0],ideal_prices)
			if ((arm1.Sl >= arm1.gamma*(1.+arm1.delta2)**(-1.)) and (arm1.Rl >= arm1.R_max)):
				arm1.R_max = arm1.Rl
				arm1.l_max = arm1.l

		if (arm2_stop == False):
			pl[1] = arm2.compute_pl()
			m[1] = arm2.offer_pl()
			arm2.computeSlandPl(m[1],pl[1],ideal_prices)
			if ((arm2.Sl >= arm2.gamma*(1.+arm2.delta2)**(-1.)) and (arm2.Rl >= arm2.R_max)):
				arm2.R_max = arm2.Rl
				arm2.l_max = arm2.l

		if (arm3_stop == False):
			pl[2] = arm3.compute_pl()
			m[2] = arm3.offer_pl()
			arm3.computeSlandPl(m[2],pl[2],ideal_prices)
			if ((arm3.Sl >= arm3.gamma*(1.+arm3.delta2)**(-1.)) and (arm3.Rl >= arm3.R_max)):
				arm3.R_max = arm3.Rl
				arm3.l_max = arm3.l

		if (arm4_stop == False):
			pl[3] = arm4.compute_pl()
			m[3] = arm4.offer_pl()
			arm4.computeSlandPl(m[3],pl[3],ideal_prices)
			if ((arm4.Sl >= arm4.gamma*(1.+arm4.delta2)**(-1.)) and (arm4.Rl >= arm4.R_max)):
				arm4.R_max = arm4.Rl
				arm4.l_max = arm4.l
		
		if (arm5_stop == False):
			pl[4] = arm5.compute_pl()
			m[4] = arm5.offer_pl()
			arm5.computeSlandPl(m[4],pl[4],ideal_prices)
			if ((arm5.Sl >= arm5.gamma*(1.+arm5.delta2)**(-1.)) and (arm5.Rl >= arm5.R_max)):
				arm5.R_max = arm5.Rl
				arm5.l_max = arm5.l


		#Now check each arm
		if (arm1_stop == False):
			if ((arm1.pl <= arm1.epsilon) or (arm1.Sl >= (1 + arm1.delta2) * arm1.alpha2) or (arm1.Rl <= arm1.R_max * (1 + arm1.delta2)**(-2))):
				arm1_stop = True
				print "arm 1 stopped"

		if (arm2_stop == False):
			if ((arm2.pl <= arm2.epsilon) or (arm2.Sl >= (1 + arm2.delta2) * arm2.alpha2) or (arm2.Rl <= arm2.R_max * (1 + arm2.delta2)**(-2))):
				arm2_stop = True
				print "arm 2 stopped"

		if (arm3_stop == False):
			if ((arm3.pl <= arm3.epsilon) or (arm3.Sl >= (1 + arm3.delta2) * arm3.alpha2) or (arm3.Rl <= arm3.R_max * (1 + arm3.delta2)**(-2))):
				arm3_stop = True
				print "arm 3 stopped"

		if (arm4_stop == False):
			if ((arm4.pl <= arm4.epsilon) or (arm4.Sl >= (1 + arm4.delta2) * arm4.alpha2) or (arm4.Rl <= arm4.R_max * (1 + arm4.delta2)**(-2))):
				arm4_stop = True
				print "arm 4 stopped"

		if (arm5_stop == False):
			if ((arm5.pl <= arm5.epsilon) or (arm5.Sl >= (1 + arm5.delta2) * arm5.alpha2) or (arm5.Rl <= arm5.R_max * (1 + arm5.delta2)**(-2))):
				arm5_stop = True
				print "arm 5 stopped"


		if (arm1_stop and arm2_stop and arm3_stop and arm4_stop and arm5_stop):
			break;


	#Find max price
	max_price_mech2 = -1

	if (arm1.p_list[arm1.l_max] > max_price_mech2):
		max_price_mech2 = arm1.p_list2[arm1.l_max]

	if (arm2.p_list[arm2.l_max] > max_price_mech2):
		max_price_mech2 = arm2.p_list2[arm2.l_max]

	if (arm3.p_list[arm3.l_max] > max_price_mech2):
		max_price_mech2 = arm3.p_list2[arm3.l_max]

	if (arm4.p_list[arm4.l_max] > max_price_mech2):
		max_price_mech2 = arm4.p_list2[arm4.l_max]

	if (arm5.p_list[arm5.l_max] > max_price_mech2):
		max_price_mech2 = arm5.p_list2[arm5.l_max]


	#Check if each player's ideal value is greater than the current price
	item_bought = False
	for yy in range (0,len(ideal_prices)):
		if (ideal_prices[yy] >= min_price*max_price_mech2):
			ideal_prices = np.delete(ideal_prices,yy) #remove the buyer from the list
			item_bought = True
			break;

	#Keep track of the overall minimum price and the round in which it occurs
	if (min_price*max_price_mech2 < overall_minimum_price):
		overall_minimum_price = min_price*max_price_mech2
		overall_minimum_round = t

	#Update k_total if an item is bought
	if (item_bought):
		if (min_indx == 0):
			arm1.update_k(min_price*max_price_mech2)
			arm1.update_kt(min_price*max_price_mech2)

		elif (min_indx == 1):
			arm2.update_k(min_price*max_price_mech2)
			arm2.update_kt(min_price*max_price_mech2)
		
		elif (min_indx == 2):
			arm3.update_k(min_price*max_price_mech2)
			arm3.update_kt(min_price*max_price_mech2)

		elif (min_indx == 3):
			arm4.update_k(min_price*max_price_mech2)
			arm4.update_kt(min_price*max_price_mech2)

		elif (min_indx == 4):
			arm5.update_k(min_price*max_price_mech2)
			arm5.update_kt(min_price*max_price_mech2)


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
