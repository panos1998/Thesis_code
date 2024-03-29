#%%
"""Naive Bayes evaluator"""
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.naive_bayes import GaussianNB
from arfftocsv import processing
from evaluation import function_evaluation

all_labels = ['LeicGender','LeicRace','raeducl','mstat','shlt','hlthlm',
'mobilb','lgmusa','grossa','finea','LeicHBP','LeicAge','hearte',
'psyche','bmicat','physActive','drinkd_e','smoken','itot','cfoodo1m',
'jphysa','estwt','wstva','chol','hdl','ldl','trig','sys1','dias3',
'fglu','hba1c','hemda','eatVegFru','everHighGlu','rYdiabe']

to_replace = {'LeicAge': ['50-59', '60-69', '>=70'], 'LeicGender': ['Female', 'Male'],
'bmicat': ["'1.underweight less than 18.5'",
 "'2.normal weight from 18.5 to 24.9'", "'3.pre-obesity from 25 to 29.9'",
 "'4.obesity class 1 from 30 to 34.9'", "'5.obesity class 2 from 35 to 39.9'",
  "'6.obesity class 3 greater than 40'"],
'LeicRace': [0, 6], 'hemda': ["'Not applicable'", 'Yes', 'No'],
 'wstva':[],'LeicHBP': ['No', 'Yes'], 'rYdiabe': ['0.no', '1.yes'],
 'raeducl':["'2.upper secondary and vocational training'",'3.tertiary',
 "'1.less than secondary'",'.o:other',"'.h:missing HSE value'",".m:Missing"],
  'mstat':['3.partnered','1.married','5.divorced','7.widowed','4.separated',
  "'8.never married'"],'shlt':["'2.Very good'",'3.Good','1.Excellent','4.Fair','5.Poor'],
   'hlthlm':['0.no','1.yes','.d:DK'],'hearte':['0.no','1.yes'],
   'psyche':['0.no','1.yes'], 'physActive':['Yes','No'], 'smoken':['0.No',
  '1.Yes',".m:Missing"],'jphysa': ["'1.Sedentary occupation'",
  "'3.Physical work'","'2.Standing occupation'","'.w:not working'",
   "'4.Heavy manual work'",'.m:Missing'], 'everHighGlu':['No',"'Not applicable'",'Yes'],
   'eatVegFru':['Yes', 'No'],'mobilb':[],'lgmusa':[], 'grossa':[],
   'finea':[], 'drinkd_e':[],'itot':[],'cfoodo1m':[], 'estwt':[], 'chol':[],
   'ldl':[], 'hdl':[], 'trig':[], 'sys1':[], 'dias3':[], 'fglu':[], 'hba1c':[]
}

values = {'LeicAge': [0, 1, 2], 'LeicGender': [0, 1],
 'bmicat': [1, 2, 3, 4, 5, 6],'LeicRace': [0, 1],
 'hemda': [0, 1, 2], 'wstva':[],'LeicHBP':[0,1],'rYdiabe': [0, 1],
  'raeducl':[2,3,1,0,4,np.nan], 'mstat':[3,1,5,7,4,8],'shlt':[2,3,1,4,5],
   'hlthlm':[0,1,2],'hearte':[0,1], 'psyche':[0,1], 'physActive':[1,0],
  'smoken':[0,1,np.nan], 'jphysa':[1,3,2,5,4,np.nan], 'everHighGlu':[0,2,1],
   'eatVegFru':[1,0],'mobilb':[],'lgmusa':[],'grossa':[], 'finea':[],
    'drinkd_e':[],'itot':[],'cfoodo1m':[], 'estwt':[],'chol':[],'ldl':[], 'hdl':[],
  'trig':[], 'sys1':[], 'dias3':[], 'fglu':[], 'hba1c':[]
 }
 #Prepare data
data = processing(labels=all_labels, to_replace=to_replace,all_labels=all_labels, values= values)
imp = KNNImputer(n_neighbors=1) # impute the data with nearest neighboor using n= 1 neighbors
x =imp.fit_transform(data) # apply imputation
data = pd.DataFrame(x, columns=all_labels) # the imputed data
#print(pd.isna(data).sum())
X = data[all_labels[:-1]]# get the features
y= data[all_labels[len(all_labels)-1]]# get the target class
#Evaluate model capability by measuring AUC
clf = GaussianNB()
# Final evaluation with threshold optimization
function_evaluation(clf, X, y)

# %%
