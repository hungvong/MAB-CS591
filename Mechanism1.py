import numpy as np
from math import log10

#Set number of agents
n = 10

#Set k
k = 5

#Delta function
d = (k**(-1/3)) * (log10(n))**(2/3)

#Compute active prices P
i_len = 10
P = np.zeros(1,i_len)
for i in range (1,i_len):
	P[i] = d*(1+d)^i 

t = 0
p = 10 #Depends on the MAB
Nt = {}
kt = np.array([1,1,0,0,0,1,1]) #depends on the MAB
while (k >= 1):

	#Update the Nt dictionary
	if (p not in Nt):
		Nt[p] = 1; #This is the first time p has occurred in this auction
	else:
		Nt[p] += 1;

	St(p) = kt(p) / Nt[p]
	rt(p) = alpha / (Nt[p] + 1) + np.sqrt((alpha*St(p))/(Nt[p]+1))
	It = p * np.min(k, n*(St(p) + rt(p)))
	p = np.argmax(It(p))
	k -= 1

	#Increment the current round number
	t += 1