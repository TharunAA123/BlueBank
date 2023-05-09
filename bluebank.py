#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:08:44 2023

@author: tharunabrahamaju
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


json_file = open('loan_data_json.json')
data = json.load(json_file)

loandata = pd.DataFrame(data)

#finding unique values for the purpose column
loandata['purpose'].unique()

#data description for important columns
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#exp() for annual income
income = np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income

#categorization via fico
length = len(loandata)
ficocat = []
for x in range (0, length):
    category = loandata['fico'][x]
    if category >= 700:
        cat = "Excellent"
    elif category >= 660:
        cat = "Good"
    elif category >= 601:
        cat = "Fair"
    elif category >= 400:
        cat = "Poor"
    elif category >= 300:
        cat = "Very Poor"
    else:
        cat = "Unknown"
    ficocat.append(cat)
    
ficocat = pd.Series(ficocat)
loandata['fico.category'] = ficocat

#if the interest rate is > 0.12, its "High", else "Low"
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

#number of loans by fico.category
catplot = loandata.groupby(['fico.category']).size()
catplot.plot.bar(color = 'green', width = 0.1)
plt.show()

purposecount = loandata.groupby(['purpose']).size()
purposecount.plot.bar(color = 'red', width = 0.2)
plt.show()

#scatterplots
ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint, ypoint, color = '#4caf50')
plt.show()

#writing to csv
loandata.to_csv('loan_cleaned.csv', index = True)