from BanditArm import BanditArm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Initialize variables
k = [7, 8, 14, 9, 28]
i = 10

#Initialize p and find k_total
pl = np.zeros(5)
m = np.zeros(5)
k_total = np.sum(k)
n = 10^(k_total)

#Initialize bandits
arm1 = BanditArm(k[0],n,i,2)
arm2 = BanditArm(k[1],n,i,2)
arm3 = BanditArm(k[2],n,i,2)
arm4 = BanditArm(k[3],n,i,2)
arm5 = BanditArm(k[4],n,i,2)

#Randomly choose each customer's "ideal" price
max_price = 1
ideal_prices = np.random.random(n) * (max_price + 1)

arm1_stop = False
arm2_stop = False
arm3_stop = False
arm4_stop = False
arm5_stop = False


while (True):

	if (arm1_stop == False):
		pl[0] = arm1.compute_pl()
		m[0] = arm1.offer_pl()
		arm1.computeSlandPl(m[0],pl[0],ideal_prices)
		if ((arm1.Sl >= arm1.gamma*(1.+arm1.delta)**(-1.)) and (arm1.Rl >= arm1.R_max)):
			arm1.R_max = arm1.Rl
			arm1.l_max = arm1.l

	if (arm2_stop == False):
		pl[1] = arm2.compute_pl()
		m[1] = arm2.offer_pl()
		arm2.computeSlandPl(m[1],pl[1],ideal_prices)
		if ((arm2.Sl >= arm2.gamma*(1.+arm2.delta)**(-1.)) and (arm2.Rl >= arm2.R_max)):
			arm2.R_max = arm2.Rl
			arm2.l_max = arm2.l

	if (arm3_stop == False):
		pl[2] = arm3.compute_pl()
		m[2] = arm3.offer_pl()
		arm3.computeSlandPl(m[2],pl[2],ideal_prices)
		if ((arm3.Sl >= arm3.gamma*(1.+arm3.delta)**(-1.)) and (arm3.Rl >= arm3.R_max)):
			arm3.R_max = arm3.Rl
			arm3.l_max = arm3.l

	if (arm4_stop == False):
		pl[3] = arm4.compute_pl()
		m[3] = arm4.offer_pl()
		arm4.computeSlandPl(m[3],pl[3],ideal_prices)
		if ((arm4.Sl >= arm4.gamma*(1.+arm4.delta)**(-1.)) and (arm4.Rl >= arm4.R_max)):
			arm4.R_max = arm4.Rl
			arm4.l_max = arm4.l
	
	if (arm5_stop == False):
		pl[4] = arm5.compute_pl()
		m[4] = arm5.offer_pl()
		arm5.computeSlandPl(m[4],pl[4],ideal_prices)
		if ((arm5.Sl >= arm5.gamma*(1.+arm5.delta)**(-1.)) and (arm5.Rl >= arm5.R_max)):
			arm5.R_max = arm5.Rl
			arm5.l_max = arm5.l


	#Now check each arm
	if (arm1_stop == False):
		if ((arm1.pl <= arm1.epsilon) or (arm1.Sl >= (1 + arm1.delta) * arm1.alpha) or (arm1.Rl <= arm1.R_max * (1 + arm1.delta)**(-2))):
			arm1_stop = True
			print "arm 1 stopped"

	if (arm2_stop == False):
		if ((arm2.pl <= arm2.epsilon) or (arm2.Sl >= (1 + arm2.delta) * arm2.alpha) or (arm2.Rl <= arm2.R_max * (1 + arm2.delta)**(-2))):
			arm2_stop = True
			print "arm 2 stopped"

	if (arm3_stop == False):
		if ((arm3.pl <= arm3.epsilon) or (arm3.Sl >= (1 + arm3.delta) * arm3.alpha) or (arm3.Rl <= arm3.R_max * (1 + arm3.delta)**(-2))):
			arm3_stop = True
			print "arm 3 stopped"

	if (arm4_stop == False):
		if ((arm4.pl <= arm4.epsilon) or (arm4.Sl >= (1 + arm4.delta) * arm4.alpha) or (arm4.Rl <= arm4.R_max * (1 + arm4.delta)**(-2))):
			arm4_stop = True
			print "arm 4 stopped"

	if (arm5_stop == False):
		if ((arm5.pl <= arm5.epsilon) or (arm5.Sl >= (1 + arm5.delta) * arm5.alpha) or (arm5.Rl <= arm5.R_max * (1 + arm5.delta)**(-2))):
			arm5_stop = True
			print "arm 5 stopped"


	if (arm1_stop and arm2_stop and arm3_stop and arm4_stop and arm5_stop):
		break;

	#print pl


n_groups = 5

prices = (arm1.pl * 100., arm2.pl * 100., arm3.pl * 100., arm4.pl * 100., arm5.pl * 100.)
percent_accept = (arm1.Sl * 100., arm2.Sl * 100., arm3.Sl * 100., arm4.Sl * 100., arm5.Sl * 100.)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, prices, bar_width,
                 alpha=opacity,
                 color='b',
                 label='% of Original Price')

rects2 = plt.bar(index + bar_width, percent_accept, bar_width,
                 alpha=opacity,
                 color='r',
                 label='% Acceptance')

plt.ylabel('Percentage')
plt.title('% of Original Price and % Acceptance Rate Per Arm \n k = ' + str(k))
plt.xticks(index + bar_width, ('Arm 1', 'Arm 2', 'Arm 3', 'Arm 4', 'Arm 5'))
plt.legend(loc=2)

plt.tight_layout()
plt.show()