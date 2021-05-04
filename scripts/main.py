import numpy as np
import pandas as pd
import scipy.stats
import itertools 
from itertools import combinations
import os
import argparse

parser = argparse.ArgumentParser(description="Find the minimum set of words") # Instantiate the parser

parser.add_argument('-i','--csv', type=str, help='path to csv file', required=True)
parser.add_argument('-a1','--a1', type=float, help='alpha_1 for num_of_words', required=True)
parser.add_argument('-a2','--a2', type=float, help='alpha_2 for correlation val.', required=True)
parser.add_argument('-a3','--a3', type=float, help='alpha_3 for effort', required=True)
parser.add_argument('-n','--best', type=int, help='number of best', default=1)
parser.add_argument('-v','--verbose', type=int, help='verbose', default=0)

args = parser.parse_args()

a_1 = args.a1 #coeff. for num_of_words (refer to Eq. 9)
a_2 = args.a2 #coeff. for correlation  ("" "")
a_3 = args.a3 #coeff. for effort ("" "")

verbose = args.verbose

grd = [58,90.4,6,28,93,15,93,62,62,2,95,7.4,43,29,86] #Perceptual Intellegibilities (provided as a part of Dataset)

df = pd.read_csv(args.csv)
x = df.iloc[:, 6:].to_numpy() # matrix of corr. values of each word for each subject
x_nm = df.iloc[:, 1].to_numpy() #list of all words

#pruned list of 14 words chosen for experiments
nm = ['NATURALIZATION', 'AUTOBIOGRAPHY', 'EXACTITUDE', 'IRRESOLUTE', 'INALIENABLE', 'LEGISLATURE', 'OVERSHADOWED', 'PSYCHOLOGICAL', 'DISSATISFACTION', 'AGRICULTURAL', 'APOTHECARY', 'AUTHORITATIVE', 'EXAGGERATE', 'INEXHAUSTIBLE']

# Effort values computed for each of the above 14 words (refer to Section 4.1)
e = [43, 36, 31, 24, 33, 26, 35, 41, 41, 37, 36, 39, 30, 43] 

nm_to_eff = {}
for ind in range(len(nm)):
	nm_to_eff[nm[ind]] = e[ind]/sum(e) #transform, [0, infi) --> [0, 1] changed tp sum(e) from max(e)

cost_arr=[] # array to save cost for each possible combination
names_arr = [] # array to save set for words for each possible combination
pc_val_avg_arr = [] # array to save corr. value for each possible combination
eff_val_arr = [] # array to save effort value for each possible combination
k_arr = []

num = len(nm)
pts = np.arange(0, num)


for i in range(1, num+1):
	var = list(map(set, itertools.combinations(pts, i)))
	if verbose == 1:
		print('Evaluating all possible subsets of size: ' + str(i) + '. Total possible subsets: ' + str(len(var)))

	for j in range(0, len(var)):
		
		#compute effort for the set
		nm_var = x_nm[list(var[j])]
		eff_var = []
		for nm_ in nm_var:
			eff_var.append(nm_to_eff[nm_.upper()])
		eff_val = sum(np.array(eff_var))
		eff_val_arr.append(eff_val)

		# compute corr. for the set
		xvar = x[list(var[j]), :]
		k = np.mean(xvar,axis=0)
		pc_val_avg = abs(scipy.stats.pearsonr(k, grd)[0])
		pc_val_avg_arr.append(pc_val_avg)
		k_arr.append(k)

		# compute total cost for the set (refer to Eq. 9)
		cost = a_1*(len(xvar)/num) - a_2*(pc_val_avg) - a_3*eff_val 
		cost_arr.append(cost)
		names_arr.append(nm_var)

print("---Best %d (%.2f %.2f %.2f --- %s "%(args.best, a_1, a_2, a_3,args.csv))
sorted_inds = np.asarray(cost_arr).argsort()[:args.best]
for optimal_ind in sorted_inds:
	#print('optimal_ind : ', optimal_ind)
	print('cost: ', round(cost_arr[optimal_ind], 5), end=" | ")
	print('L: ', round(len(names_arr[optimal_ind])/num,5), end=" | ")
	print('PC-avg: ', round(pc_val_avg_arr[optimal_ind], 5), end=" | ")
	print('Ef: ', round(eff_val_arr[optimal_ind], 5), end=" | ")
	print('words: ', names_arr[optimal_ind])

	pred = k_arr[optimal_ind] #predicted "raw" intelligibility for all subjects
	pred = (pred-min(pred))/(max(pred)-min(pred)) #min-max normalization
	grd = np.array(grd)
	grd = (grd-min(grd))/(max(grd)-min(grd)) #min-max normalization

#save normalized intelligibilities (can be used for scatterplots, Fig.2 in the paper)
intel_type = args.csv.split('/')[-1].strip('.csv')
np.save('plotvals/'+intel_type+'_pred.npy', pred)
if not os.path.exists('plotvals/grd.npy'):
	np.save('plotvals/grd.npy', grd)
