#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 20:35:07 2022

@author: akinbodebams
"""
#load libraries
import pandas as pd

#create dataframe
df=pd.read_csv('gtb.csv')

#differentiate all airtime purchases from other transactions
df['Airtime_p'] = df['Remarks'].apply(lambda x : 'Airtime_p' if 'Airtime Purchase' in x else "others")
df.replace(',','', regex=True, inplace=True)
df["Debit"] = pd.to_numeric(df["Debit"])


#drop rows where transaction is not airtime
others = df[df['Airtime_p']== "others"].index
df.drop(others, inplace = True)

#shorten remark to only important keywords
df['Remarkss'] = df['Remarks'].apply(lambda x : x.split('-')[0])
df['phone_numbers'] = df['Remarks'].apply(lambda x : x.split('-')[2])
df['recipient']= df['phone_numbers'].apply(lambda x : 'My Number' if x == '2348080415982' else 'Friends')

#differentiate channel of airtime purchase
df['Channel'] = df['Remarkss'].apply(lambda x: 'GTWORLD' if 'GTWORLD' in x else 'USSD')



def sub_cat(data):
    if data == 1500 or data == 1499:
        return 'Weekly Sub'
    elif data > 1500 :
        return 'Monthly Sub'
    else:
        return 'Call Recharge'
    
#extract debits that are 1500 or 1499,03
df['Recharge Type'] = df['Debit'].apply(lambda x : sub_cat(x))

df1 = df[['Trans Date', 'Debit', 'Recharge Type', 'Channel', 'recipient']]


df1.to_csv('new.csv', index = False)