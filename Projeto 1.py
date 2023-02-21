# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:09:50 2023
conda install spyder-kernels <library here> -y
@author: Thúlio Nascimento
"""

import sinatur_lib as sl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates

''' Creating the objects '''
ETH = sl.OALL(pd.read_csv("ETHUSD.csv"))
IBV = sl.OALL(pd.read_csv("IBOVESPA.csv"))
NDQ = sl.OALL(pd.read_csv("NASDAQ.csv"))

''' Calling function that treat the dataframe '''
sl.do_all(ETH, IBV, NDQ)

#fig,ax = plt.subplots()
#ax.scatter(ETH.df['Vol.'],ETH.df['Var%'])

''' Normalizando os dados '''
ETH.df[['Último_norm','Abertura_norm','Máxima_norm','Mínima_norm']] = ETH.df.iloc[:,0:4].apply(lambda col: col/ETH.df.iloc[0,1]*100)
IBV.df[['Último_norm','Abertura_norm','Máxima_norm','Mínima_norm']] = IBV.df.iloc[:,0:4].apply(lambda col: col/IBV.df.iloc[0,1]*100)
NDQ.df[['Último_norm','Abertura_norm','Máxima_norm','Mínima_norm']] = NDQ.df.iloc[:,0:4].apply(lambda col: col/NDQ.df.iloc[0,1]*100)

''' Criando retorno diario '''
ETH.df["Retorno%"] = (ETH.df.Último/ETH.df.Último.shift(1) - 1)*100
ETH.df["Retorno%"][0] = 0

IBV.df["Retorno%"] = (IBV.df.Último/IBV.df.Último.shift(1) - 1)*100
IBV.df["Retorno%"][0] = 0

NDQ.df["Retorno%"] = (NDQ.df.Último/NDQ.df.Último.shift(1) - 1)*100
NDQ.df["Retorno%"][0] = 0

'''Aplitute entre máximo e mínimo '''
ETH.df["Aplitude_max_mix_diário"] = abs(ETH.df['Máxima'] - ETH.df['Mínima'])
IBV.df["Aplitude_max_mix_diário"] = abs(IBV.df['Máxima'] - IBV.df['Mínima'])
NDQ.df["Aplitude_max_mix_diário"] = abs(NDQ.df['Máxima'] - NDQ.df['Mínima'])

ETH.df.resample('Y').max().Máxima - ETH.df.resample('Y').min().Mínima

df1['col2'] = ETH.df["Retorno%"].resample('Y').mean().asfreq('D').bfill()

ETH.df["Retorno%"].resample('Y').mean()
ETH.df["Retorno%"].resample('Y').var()
ETH.df["Retorno%"].resample('Y').std()


ETH.df["Retorno%"].resample('Y').get_group(pd.to_datetime("2017-12-31 00:00:00"))

df1 = ETH.df
df2 = IBV.df
df3 = NDQ.df

#ax.set_xticklabels()
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.yaxis.set_visible(False)
ax.xaxis.set(ticks=range(1,1500,100))
plt.show()

#sns.lineplot(data=ETH.df,x=ETH.df.index, y="Vol.",hue="Var%", style="Var%")

