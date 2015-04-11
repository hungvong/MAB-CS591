import numpy as np
from math import log10

#Set number of agents
n = 10


#Settings
t = 0
p = 1 #Depends on the MAB
Nt = {}
kt = np.array([0,1,4,0,1]) #depends on the MAB
k = np.sum(kt) #number of items left
alpha = np.floor(log10(n))

#Delta function
d = (k**(-1/3)) * (log10(n))**(2/3)

#Compute active prices P
i_len = 10
P = np.zeros((i_len))
for i in range (1,i_len):
	P[i] = d*(1+d)**i 

#Initialize lists
St = []
rt = []
It = []

while (k >= 1):

	#Update the Nt dictionary
	if (p not in Nt):
		Nt[p] = 1; #This is the first time p has occurred in this auction
	else:
		Nt[p] += 1;

	St.extend([ float(kt[t]) / float(Nt[p])])
	rt.extend([( float(alpha) / float((Nt[p] + 1))) + np.sqrt((float(alpha*St[t]))/float((Nt[p]+1)))])
	It.extend([p * np.min((k, n*(St[t] + rt[t])))])
	p = np.argmax(It) + 1
	k = k - kt[t]

	#Increment the current round number
	t += 1