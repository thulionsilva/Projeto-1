# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:06:39 2023

@author: Thúlio Nascimento
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
''' ----------------------------------------------------------------------- '''
def plot_series_single(classe,label):
    for col in classe.df.iloc[:,:6]:
        fig, ax1 = plt.subplots(2,1)
        sns.lineplot(x=classe.df.index, y=classe.df[col], ax=ax1[0])
        ax1[0].set_title(label)
        sns.lineplot(x=classe.df.index, y=drawdown(classe.df[col]).squeeze(), ax=ax1[1],color='r')
        ax1[1].fill_between(classe.df.index,drawdown(classe.df[col]).squeeze(), color='r',alpha=0.5)


def plot_retorno(classe,label):
    fig, ax1 = plt.subplots(2,1)
    sns.lineplot(x=classe.df.index, y=classe.df["Retorno"], ax=ax1[0])
    ax1[0].set_title(label)
    sns.lineplot(x=classe.df.index, y=drawdown(classe.df["Retorno"]).squeeze(), ax=ax1[1],color='r')
    ax1[1].fill_between(classe.df.index,drawdown(classe.df["Retorno"]).squeeze(), color='r',alpha=0.5)
''' ----------------------------------------------------------------------- '''
''' Returno drawdown panda'''
def drawdown(df):
    for value in range(len(df)):
        if value == 0:
            draw = [0]
        else:
            draw.append((df[value]-max(df[:value+1]))/max(df[:value+1])*100) 
    df2 = pd.DataFrame(draw,columns=["Drawdown"])
    return df2

''' ----------------------------------------------------------------------- '''
def gap_count(df):
    '''
    GAP = (df["Abertura"] - df["Último"].shift(1)).fillna(0)
    GAP = GAP[(GAP!=0)]
    GAP_abs = GAP.apply(lambda x:abs(x))
    '''
    #Se for diferente de zero é um gap e retorna true ou false
    #Soma todos os trues resultando na  quantidade de gaps
    return ((df["Abertura"] - df["Último"].shift(1)).dropna() != 0).sum()
''' ----------------------------------------------------------------------- '''
def gap_closing_count(df):
    subtracted_by_closing = df.sub(df["Último"].shift(1),axis=0).fillna(0)
    GAP = subtracted_by_closing["Abertura"]
    gap_negativo = subtracted_by_closing[GAP > 0]
    gap_negativo = gap_negativo[gap_negativo.Mínima < 0]
    GAP = subtracted_by_closing["Abertura"]
    gap_positivo = subtracted_by_closing[GAP < 0]
    gap_positivo = gap_positivo[gap_positivo.Máxima < 0]
    
    return (gap_positivo.count() + gap_negativo.count())[1]
    
''' ----------------------------------------------------------------------- '''
def do_all(ETH,IBV,NDQ):
    #Fill in the missing dates of the index
    ETH.df = ETH.df.asfreq('D')
    IBV.df = IBV.df.asfreq('D')
    NDQ.df = NDQ.df.asfreq('D')
    #Get the interval of dates
    interval = get_date_interval(ETH.df, IBV.df, NDQ.df)
    #Chop the dataframe so they have the same date intervaal
    ETH.set_equal_timeframe(interval)
    IBV.set_equal_timeframe(interval)
    NDQ.set_equal_timeframe(interval)
    #Delete the weekend from the database
    ETH.business_days_only()
    IBV.business_days_only()
    NDQ.business_days_only()
    #Turn all strings into number 
    ETH.df = ETH.df.applymap(convert_values_to_float)
    IBV.df = IBV.df.applymap(convert_values_to_float)
    NDQ.df = NDQ.df.applymap(convert_values_to_float)
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

def convert_values_to_float(s):
    
    if isinstance(s, float):
        return s

    val_int = 0
    splitted_int_decimal = s[0:-1].split(",")
    splitted_int_only = splitted_int_decimal[0].split(".")
    
    if len(splitted_int_only) == 1:
        splitted_int_only = splitted_int_only[0]
    if len(splitted_int_only) == 2:
        splitted_int_only = splitted_int_only[0] + splitted_int_only[1]
        
    if s[-1] == 'B':
        val_int = float(splitted_int_only[0]+splitted_int_decimal[1])*10000000
    elif s[-1] == 'M':
        val_int = float(splitted_int_only[0]+splitted_int_decimal[1])*10000
    elif s[-1] == 'K':
        val_int = float(splitted_int_only[0]+splitted_int_decimal[1])*10
    elif s[-1] == '%':
        if len(splitted_int_decimal) == 1:
            val_int = float(splitted_int_decimal[0])

        else:
            val_int = float(splitted_int_only[0]+splitted_int_decimal[-1])/100
    elif s == '-':
        val_int = 0.0
    else:
        val_int = float(splitted_int_only+s.split(",")[1])/100
    return val_int

'''======================================================================================'''
class DataFrame_treating():
    def __init__(self,df):
        self.df = df
        print("Convertendo datas de string para DateTime")
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%d.%m.%Y')
        self.df.rename(index=self.df['Data'],inplace=True)
        self.df.drop('Data',axis=1,inplace=True)
    def business_days_only(self):
        self.df = self.df[self.df.index.dayofweek<5]
    
    def set_equal_timeframe(self, limites):
        self.df = self.df[(self.df.index >= limites[0]) & (self.df.index <= limites[1])]
    
    def fill_void(self):
        self.df.fillna(self.df[["Último"]].shift(1), inplace=True)
        self.df.iloc[:,-2:] = self.df.iloc[:,-2:].fillna(0)
        self.df.fillna(method='ffill', axis=1, inplace=True)

    #def volume_converter(self):
        
