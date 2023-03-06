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
ETH = sl.DataFrame_treating(pd.read_csv("ETHUSD.csv"))
IBV = sl.DataFrame_treating(pd.read_csv("IBOVESPA.csv"))
NDQ = sl.DataFrame_treating(pd.read_csv("NASDAQ.csv"))

''' Calling function that treat the dataframe '''
sl.do_all(ETH, IBV, NDQ)

#fig,ax = plt.subplots()
#ax.scatter(ETH.df['Vol.'],ETH.df['Var%'])

''' Normalizando os dados '''
ETH.df[['Último_norm','Abertura_norm','Máxima_norm','Mínima_norm']] = ETH.df.iloc[:,0:4].apply(lambda col: col/ETH.df.iloc[0,1]*100)
IBV.df[['Último_norm','Abertura_norm','Máxima_norm','Mínima_norm']] = IBV.df.iloc[:,0:4].apply(lambda col: col/IBV.df.iloc[0,1]*100)
NDQ.df[['Último_norm','Abertura_norm','Máxima_norm','Mínima_norm']] = NDQ.df.iloc[:,0:4].apply(lambda col: col/NDQ.df.iloc[0,1]*100)

''' Criando retorno diario '''
 # Alternative method -> ETH.df.Último.pct_change()
ETH.df["Retorno"] = (ETH.df.Último/ETH.df.Último.shift(1) - 1)
ETH.df["Retorno"][0] = 0

IBV.df["Retorno"] = (IBV.df.Último/IBV.df.Último.shift(1) - 1)
IBV.df["Retorno"][0] = 0

NDQ.df["Retorno"] = (NDQ.df.Último/NDQ.df.Último.shift(1) - 1)
NDQ.df["Retorno"][0] = 0

'''Aplitute entre máximo e mínimo '''
ETH.df["Aplitude_max_mix_diário"] = abs(ETH.df['Máxima_norm'] - ETH.df['Mínima_norm'])
IBV.df["Aplitude_max_mix_diário"] = abs(IBV.df['Máxima_norm'] - IBV.df['Mínima_norm'])
NDQ.df["Aplitude_max_mix_diário"] = abs(NDQ.df['Máxima_norm'] - NDQ.df['Mínima_norm'])

'''Aplitute entre máximo e mínimo '''
ETH.df["Aplitude_fechamento_abertura_diário"] = abs(ETH.df['Abertura_norm'] - ETH.df['Último_norm'])
IBV.df["Aplitude_fechamento_abertura_diário"] = abs(IBV.df['Abertura_norm'] - IBV.df['Último_norm'])
NDQ.df["Aplitude_fechamento_abertura_diário"] = abs(NDQ.df['Abertura_norm'] - NDQ.df['Último_norm'])

'''Média da variação entre máximo e mínimo diário'''
ETH.df["Aplitude_fechamento_abertura_diário"].mean()
IBV.df["Aplitude_fechamento_abertura_diário"].mean()
NDQ.df["Aplitude_fechamento_abertura_diário"].mean()

'''Média da variação entre máximo e mínimo diário'''

ETH.df["Aplitude_max_mix_diário"].mean()
IBV.df["Aplitude_max_mix_diário"].mean()
NDQ.df["Aplitude_max_mix_diário"].mean()

'''Aplitute entre máximo e mínimo anual'''
ETH.df.resample('Y').max()["Máxima_norm"] - ETH.df.resample('Y').min()["Mínima_norm"]
IBV.df.resample('Y').max()["Máxima_norm"] - IBV.df.resample('Y').min()["Mínima_norm"]
NDQ.df.resample('Y').max()["Máxima_norm"] - NDQ.df.resample('Y').min()["Mínima_norm"]

'''retorno anual'''
ETH.df.resample('Y').last()["Último_norm"] - ETH.df.resample('Y').first()["Último_norm"]
IBV.df.resample('Y').last()["Último_norm"] - IBV.df.resample('Y').first()["Último_norm"]
NDQ.df.resample('Y').last()["Último_norm"] - NDQ.df.resample('Y').first()["Último_norm"]


ETH.df['col2'] = ETH.df["Retorno"].resample('Y').mean().asfreq('D').bfill()

''' retorno acumulativo '''
ETH.df["Retorno_acumulado"] = (ETH.df.Último.pct_change()[1:]+1).cumprod() - 1

ETH.df["Retorno"].groupby(lambda x: x.year).mean().asfreq('D')

''' retorno acumulativo dos últimos 12 meses'''
(ETH.df["Retorno"].last("12M")+1).cumprod()-1

''' Retorno ano a ano'''
ETH.df.groupby(lambda x: x.year).last()["Último_norm"] - ETH.df.groupby(lambda x: x.year).first()["Último_norm"]

ETH.df["Retorno"].resample('Y').mean()
ETH.df["Retorno"].resample('Y').var()
ETH.df["Retorno"].resample('Y').std()


ETH.df["Retorno"].resample('Y').get_group(pd.to_datetime("2017-12-31 00:00:00")).sort_values()


df1 = ETH.df
df2 = IBV.df
df3 = NDQ.df

df = ETH.df["Último_norm"].copy().index
df_ETH = ETH.df["Último_norm"].copy()

'''Correlação entre fechamento de ativos '''
ETH.df["Último"].corr(IBV.df["Último"])

'''Correlação entre fechamento de ativos janela de 45 dias'''
ETH.df["Último"].rolling(45).corr(IBV.df["Último"])

ETH.df["Último"].resample('45D').apply(lambda x: x.corr(IBV.df["Último"]))
ETH.df["Último"].rolling(45,step=45).apply(lambda x: x.corr(IBV.df["Último"]))


'''Calculando quantas vezes ouve GAP'''
#Subtrai a abertura pelo fechamento do dia anterior
#Se for diferente de zero é um gap e retorna true ou false
#Soma todos os trues resultando na  quantidade de gaps
((ETH.df["Abertura"] - ETH.df["Último"].shift(1)).dropna() != 0).sum()

ETH.df[((ETH.df["Abertura"] - ETH.df["Último"].shift(1)) != 0)]

'''Calculando a média de GAP '''

GAP = ETH.df["Abertura"] - ETH.df["Último"].shift(1)
GAP = GAP[GAP.isnull() != True]
GAP = GAP[(GAP!=0)]
GAP_abs = GAP.apply(lambda x:abs(x))
GAP_mean = GAP.groupby(lambda x:x.year).mean()





#ax.set_xticklabels()
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
# ax.yaxis.set_visible(False)
# ax.xaxis.set(ticks=range(1,1500,100))
# plt.show()

#sns.lineplot(data=ETH.df,x=ETH.df.index, y="Vol.",hue="Var%", style="Var%")

