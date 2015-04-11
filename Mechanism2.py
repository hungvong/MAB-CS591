import numpy as np
from math import log10
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import random

#Set number of agents
n = 30

#Settings
l = -1
pl = 1 #Depends on the MAB
p_list = [] #Saves history of prices, per round
kt = np.array([6,3,8,9,11,2,1,100,50,33,2,8,19,88])
k = np.sum(kt) #number of items left
epsilon = k**(-0.25)

#Delta function
delta = ((1./k) * log10(k))**(0.25)

#Compute alpha
alpha =  (float(k)/float(n))**(1-delta)

#Initialize lists
Sl_list = []
Rl_list = []

Sl_max = (1+delta)*alpha
R_max = 0
l_max = 0
Sl = 0
Rl = 0

while (True):

	print "INFINITE LOOP"

	p_list.extend([pl])

	#Compute l and pl
	l = l + 1
	pl = (1.+delta)**(-l)

	#                                       n
	#Offer price pl to m = delta * ----------------------- agents
	#                             log_{1+delta}(1/epsilon) 
	b = 1. + delta #log base
	log_result = log10(1./epsilon)/log10(b)
	m = delta * (n / log_result)

	#Let Sl be the fraction of them who accept -- randomly choose
	Sl = random()*Sl_max
	if (Sl == Sl_max):
		Sl = Sl - 0.0000001
	Sl_list.extend([Sl])

	#Let Rl=pl*Sl be the average per agent revenue
	Rl = pl*Sl
	Rl_list.extend([Rl])

	if ((Sl >= alpha*(1.+delta)**(-1.)) and (Rl >= R_max)):
		R_max = Rl
		l_max = l

	if ((pl <= epsilon) or (Sl >= (1+delta)*alpha) or (Rl <= R_max*(1+delta)**(-2))):
		break;

