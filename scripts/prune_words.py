import os
import pandas as pd

import argparse

parser = argparse.ArgumentParser(description="Pruning words") # Instantiate the parser
parser.add_argument('--dir', type=str, help='path to csv dir',required=True)
parser.add_argument('--ns', type=int, help='max. number of syllables', default=4)
parser.add_argument('--dist', type=float, help='max. F1-F2 (formant) distance', default=2400)
args = parser.parse_args()

csv_dir = args.dir
ns = args.ns
f_dist = args.dist

csv_path = os.path.join(csv_dir, 'words.csv')
df_words = pd.read_csv(csv_path)

print('Total words: ', len(df_words))

print(' Pruning ...')
print(' Max. number of syllabels = ', str(ns))
print(' Max. formant distance = ', str(f_dist))

df_words = df_words.drop_duplicates(subset=['Word'], keep='first') # drop duplicate words 765 --> 449
print('Total unique words: ', len(df_words))

wrd_arr = [] # list to store all the words that satisfy our constraints. (Section 5.2)
wrd_id_arr = [] # list to store all IDs of words that satisfy our constraints.
for i, row in df_words.iterrows():
	if row['Syllables'] > ns and row['Sum_Dist'] > f_dist:
		#if row['Word'] in wrd_arr:
			wrd_arr.append(row['Word'])
			wrd_id_arr.append(row['File'])
			
print('Total unique words (after pruning): ', len(wrd_arr))
print('Pruned set of words: ', wrd_arr)

var = ['sm', 'unk', 'ld', 'os']
for v in var:
	csv_path = os.path.join(csv_dir, 'I_'+v+'.csv')
	df = pd.read_csv(csv_path)
	df_pruned = df[df['File'].isin(wrd_id_arr)]
	save_path = os.path.join(csv_dir, 'I_'+v+'_pruned.csv')
	df_pruned.to_csv(save_path, index=False)
	print('Pruned I_'+v+' scores saved at, '+save_path)



				

