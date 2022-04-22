#%%
from turtle import width
from arfftocsv import processing
import numpy as np
import pandas as pd
import tqdm

all_labels = ['LeicGender','LeicRace','raeducl','mstat','shlt','hlthlm',
'mobilb','lgmusa','grossa','finea','LeicHBP','LeicAge','hearte',
'psyche','bmicat','physActive','drinkd_e','smoken','itot','cfoodo1m',
'jphysa','estwt','wstva','chol','hdl','ldl','trig','sys1','dias3',
'fglu','hba1c','hemda','eatVegFru','everHighGlu','rYdiabe']
# this function deletes @ and empty lines so that produce a 
labels = ['LeicAge','LeicGender','bmicat','LeicRace','hemda','wstva','LeicHBP','rYdiabe']

to_replace = {'LeicAge': ['50-59', '60-69', '>=70'], 'LeicGender': ['Female', 'Male'], 
'bmicat': ["'1.underweight less than 18.5'",
 "'2.normal weight from 18.5 to 24.9'", "'3.pre-obesity from 25 to 29.9'",
 "'4.obesity class 1 from 30 to 34.9'", "'5.obesity class 2 from 35 to 39.9'",
  "'6.obesity class 3 greater than 40'"],
'LeicRace': [0, 6], 'hemda': ["'Not applicable'", 'Yes', 'No'],
 'wstva':[],'LeicHBP': ['No', 'Yes'], 'rYdiabe': ['0.no', '1.yes']
}

values = {'LeicAge': [0, 1, 2], 'LeicGender': [0, 1],
 'bmicat': [1, 2, 3, 4, 5, 6],'LeicRace': [0, 6],
 'hemda': [0, 1, 2], 'wstva':[],'LeicHBP':[0,1],'rYdiabe': [0, 1]}

path = 'LeicLog.csv'
data = processing(labels=labels, to_replace=to_replace,all_labels=all_labels, values= values, path=path)
# Apply machine learning techniques
X = data[labels[:-1]] # get the features
y = data[labels[len(labels)-1]] # get the target class
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV 
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

aucs = np.zeros((10, 8, 100)) # initialize an array to store aucs
#for j in range (500):         # TRUE POSITIVE RATE = SENSITIVITY
for k in tqdm.tqdm(range(100), colour='CYAN'): # for 100 epochs
    for i in range(0,10): # run through 10 different stratified datasets
       j = 0                                       # TRUE NEGATIVE RATE = SPECIFICITY
       X_train, X_test, y_train, y_test = train_test_split(X, y,train_size= 0.7,test_size=0.3, stratify=y) # stratified train/test split 70/30
       for c in [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]:#evaluate each dataset over 8 different C values
           clf = LogisticRegression(C=c, solver='liblinear',penalty='l2').fit(X_train, y_train) # train classifier over a dataset for C values
           y_pred = (clf.predict_proba(X_test))[:,1] # get prob predictions
           fpr, sensitivity, thresholds = roc_curve(y_test, y_pred) # get metrics
           aucs[i, j, k] =(roc_auc_score(y_test, y_pred)) #3-order tensor saves auc for each C
           j = j + 1                                      # for each dataset for each epoch
means = np.mean(np.mean(aucs, axis =2), axis =0) # mean auc per c over all datasets and epochs
print(means)
plt1 = plt.figure(1)
plt.xlabel('C value')
plt.ylabel('Mean AUC')
plt.plot(['0.0001', '0.001', '0.01', '0.1', '1', '10', '100', '1000'], means)
# να δουμε αυριο τι να αλλαξουμε μπας κ φτασουμε τα σωστα, οπως regularization C, penalty l1, l2 
#Υπαρχει μια απόκλιση 4%
#Εδω θα βαλουμε αυριο το κωδικα για να βρουμε το threshold, να ψαξω αν πρωτα πρεπει να κανω  training  και μετα hyper
# parameters ή βολευει οπως το εκανα
#%%
clf = LogisticRegression(C=100, solver='liblinear', penalty='l2').fit(X_train, y_train)
aucs = list()
bests = list()
for i in tqdm.tqdm(range(0,10)):
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
       train_size=0.7, stratify=y)
   clf.fit(X_train,y_train)
   probs = clf.predict_proba(X_test)[:,1]
   aucs.append(roc_auc_score(y_test, probs))
   fpr, tpr, thr= roc_curve(y_test, probs)
   metrics = [(tp,1-fp, th) for tp, fp, th in zip(tpr, fpr, thr)]
   bests.append(max(metrics, key=lambda tuple: tuple[0]+tuple[1]))
   #print(metrics)
print('best AUC: ',np.max(aucs), 'mean AUC: ', np.mean(aucs),'min AUC: ', np.min(aucs))
best = max(bests,key=lambda tuple:tuple[0]+tuple[1])
best_array=np.array(bests)
print('Max sens: ',np.max(best_array[:,0]),'Min sens: ', np.min(best_array[:,0]))
print('Max spec: ',np.max(best_array[:,1]),'Min spec: ', np.min(best_array[:,1]))
print('J: ', best[0]+best[1]-1,'Threshold: ', best[2],'sensitivity: ', best[0],'specificity: ',best[1])
# %%
