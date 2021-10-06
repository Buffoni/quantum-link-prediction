#!/usr/bin/env python
# coding: utf-8

# # Importing raw data

# In[1]:


import pickle
import numpy as np
from scipy import sparse
#import networkx as nx
#from datetime import date
#import random

NUM_OF_VERTICES_TOTAL = 64719 # number of vertices of the semantic net

data_source = 'CompetitionSet2017_3.pkl'
#data_source = 'CompetitionSet2017_3.pkl'

full_dynamic_graph_sparse, unconnected_vertex_pairs, year_start, years_delta = pickle.load( open( data_source, "rb" ) )

NUM_OF_EDGES = full_dynamic_graph_sparse[:, 0].size

print(data_source+' has '+str(len(full_dynamic_graph_sparse))+' edges between a total of '+str(NUM_OF_VERTICES_TOTAL)+ ' vertices.\n\n')
print('The goal is to predict which of '+str(len(unconnected_vertex_pairs))+' unconnectedvertex-pairs\nin unconnected_vertex_pairs will be connected until '+str(year_start+years_delta)+'.')


# # Pre-processing data (currently not being used)
# 
# It seems the data generates a lot of nodes with 0 degree. For the methods we use this is useless since we can only predict new links inside a connected graph, so we will process the data to create an edge list corresponding to the smaller graph. Later on we can use the dictionary here to revert the scores back to the original graph node indices.

# In[1]:


data = []
dataflat = []

for a in full_dynamic_graph_sparse[:, :2]:
    data.append([a[0], a[1]])
    dataflat.append(a[0])
    dataflat.append(a[1])

mydict = {}


for i,item in enumerate(dataflat):
    if(i>0 and item in mydict):
        continue
    else:    
        mydict[item] = i

invDict = {v: k for k, v in mydict.items()}

numbered = []

for [item1, item2] in data:
    numbered.append([mydict[item1], mydict[item2]])

edge_list = np.array(numbered)

NUM_OF_VERTICES = edge_list.max() + 1


# ## Exporting edge_list.txt

# In[ ]:


np.savetxt("edge_list.txt", edge_list, fmt='%i',)


# # L3 Method (Istvan)

# In[2]:


from scipy.sparse import dok_matrix
import datetime

A    = dok_matrix((NUM_OF_VERTICES_TOTAL, NUM_OF_VERTICES_TOTAL))
Diag = dok_matrix((NUM_OF_VERTICES_TOTAL, NUM_OF_VERTICES_TOTAL))
D    = np.zeros([NUM_OF_VERTICES_TOTAL, 1])

print(datetime.datetime.now().time())
print("Building adjacency matrix and degree vector.")
for a in full_dynamic_graph_sparse[:, :2]:
    A[a[0], a[1]] = 1;
    A[a[1], a[0]] = 1;

D = np.asarray(A.sum(1))

print("Found ", np.count_nonzero(D==0)," unconnected nodes.")

D = np.where(D == 0, 1, D) # Adds 1 to the degree on unconnected nodes to avoid div by 0

print(datetime.datetime.now().time())


# In[ ]:


print(datetime.datetime.now().time())
print("Building D^-1/2.")

for i,d in enumerate(D):
    Diag[i,i] = 1/np.sqrt(d);

print(datetime.datetime.now().time())
print("Computing Ã.")
A_tilde = Diag*A*Diag;

print(datetime.datetime.now().time())
print("Computing P.")
P_scores = A*A_tilde*A;

print(datetime.datetime.now().time())


# # Post process scores

# In[ ]:


competition_scores = []

for item in unconnected_vertex_pairs:
    competition_scores.append([item[0], item[1], P_scores[item[0], item[1]]])
    
competition_scores = np.array(competition_scores)

nonzero_scores = 1*10**6 - np.count_nonzero(competition_scores[:, 2] == 0)

print("Istvan's method computes the scores of ",nonzero_scores," links.")


# In[ ]:


# Get sorted index of predictions given the initial array of 1.000.000 predictions
sorted_predictions = np.argsort(-competition_scores[:, 2])


# # AUC (for 2014 -> 2017 predictions)

# In[ ]:


import matplotlib.pyplot as plt

def calculate_ROC(data_vertex_pairs, data_solution):
    data_solution = np.array(data_solution)
    data_vertex_pairs_sorted = data_solution[data_vertex_pairs]
    
    xpos=[0]
    ypos=[0]
    ROC_vals=[]
    for ii in range(len(data_vertex_pairs_sorted)):
        if data_vertex_pairs_sorted[ii]==1:
            xpos.append(xpos[-1])
            ypos.append(ypos[-1]+1)
        if data_vertex_pairs_sorted[ii]==0:
            xpos.append(xpos[-1]+1)
            ypos.append(ypos[-1])      
            ROC_vals.append(ypos[-1])
    
    ROC_vals=np.array(ROC_vals)/max(ypos)
    ypos=np.array(ypos)/max(ypos)
    xpos=np.array(xpos)/max(xpos)
    
    plt.plot(xpos, ypos)
    plt.show()
    
    AUC=sum(ROC_vals)/len(ROC_vals)
    return AUC


# In[ ]:


with open('TrainSet2014_3_solution.pkl', "rb" ) as pkl_file:
        unconnected_vertex_pairs_solution = pickle.load(pkl_file)
    
AUC = calculate_ROC(sorted_predictions, np.array(unconnected_vertex_pairs_solution))
print('Area Under Curve for Evaluation: ', AUC,'\n\n\n')


# # Preparing a file for submission

# In[ ]:


import json

# Save the results for submission.
submit_file = "test_submission_01.json"
all_idx_list_float=list(map(float, sorted_predictions))
with open(submit_file, "w", encoding="utf8") as json_file:
    json.dump(all_idx_list_float, json_file)
    
print("Solution stored as "+submit_file+".\nLooking forward to your submission.")

