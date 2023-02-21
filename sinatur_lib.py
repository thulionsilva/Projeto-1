# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:06:39 2023

@author: Thúlio Nascimento
"""
import pandas as pd
''' ----------------------------------------------------------------------- '''
def do_all(ETH,IBV,NDQ):
    #Fill in the missing dates of the index
    ETH.df = ETH.df.asfreq('D')
    IBV.df = IBV.df.asfreq('D')
    NDQ.df = NDQ.df.asfreq('D')
    #Get the interval of dates
    interval = get_date_interval(ETH.df, IBV.df, NDQ.df)
    #Chop the dataframe so they have the same date intervaal
    ETH.chop_DF(interval)
    IBV.chop_DF(interval)
    NDQ.chop_DF(interval)
    #Delete the weekend from the database
    ETH.BDays_Only()
    IBV.BDays_Only()
    NDQ.BDays_Only()
    #Turn all strings into number 
    ETH.df = ETH.df.applymap(conv)
    IBV.df = IBV.df.applymap(conv)
    NDQ.df = NDQ.df.applymap(conv)
    #Fill void
    ETH.fill_void()
    IBV.fill_void()
    NDQ.fill_void()


''' ----------------------------------------------------------------------- '''

def get_date_interval(df1,df2,df3):
    older_date = [df1.index[0],df2.index[0],df3.index[0]]
    older_date.sort()
    latest_date = [df1.index[-1],df2.index[-1],df3.index[-1]]
    latest_date.sort()
    return [older_date[-1],latest_date[0]]

''' ----------------------------------------------------------------------- '''

def conv(s):
    
    if isinstance(s, float):
        return s

    val_int = 0
    a = s[0:-1].split(",")
    b = a[0].split(".")
    
    if len(b) == 2:
        b = b[0] + b[1]
        
    if s[-1] == 'B':
        val_int = float(b[0]+a[1])*10000000
    elif s[-1] == 'M':
        val_int = float(b[0]+a[1])*10000
    elif s[-1] == 'K':
        val_int = float(b[0]+a[1])*10
    elif s[-1] == '%':
        if len(a) == 1:
            val_int = float(a[0])
            print("entering")
        else:
            val_int = float(b[0]+a[-1])/100
    elif s == '-':
        val_int = 0.0
    else:
        val_int = float(b[0]+s.split(",")[1])/100
    return val_int

'''======================================================================================'''
class OALL():
    def __init__(self,df):
        self.df = df
        print("Convertendo datas de string para DateTime")
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%d.%m.%Y')
        self.df.rename(index=self.df['Data'],inplace=True)
        self.df.drop('Data',axis=1,inplace=True)
    def BDays_Only(self):
        self.df = self.df[self.df.index.dayofweek<5]
    
    def chop_DF(self, limites):
        self.df = self.df[(self.df.index >= limites[0]) & (self.df.index <= limites[1])]
    
    def fill_void(self):
        self.df.fillna(self.df[["Último"]].shift(1), inplace=True)
        self.df.iloc[:,-2:] = self.df.iloc[:,-2:].fillna(0)
        self.df.fillna(method='ffill', axis=1, inplace=True)

    #def volume_converter(self):
        
