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
from matplotlib.dates import DateFormatter

''' Creating the objects '''
ETH = sl.DataFrame_treating(pd.read_csv("ETHUSD.csv"))
IBV = sl.DataFrame_treating(pd.read_csv("IBOVESPA.csv"))
NDQ = sl.DataFrame_treating(pd.read_csv("NASDAQ.csv"))

''' Calling function that treat the dataframe '''
sl.do_all(ETH, IBV, NDQ)

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

'''Média da variação entre fechamento abeertura diário'''
ETH.df["Aplitude_fechamento_abertura_diário"].mean()

'''Média da variação entre máximo e mínimo diário'''

ETH.df["Aplitude_max_mix_diário"].mean()

'''Aplitute entre máximo e mínimo anual'''
ETH.df.resample('Y').max()["Máxima_norm"] - ETH.df.resample('Y').min()["Mínima_norm"]

'''retorno anual'''
print("Retorno anual dos ativos")
ETH.df.resample('Y').last()["Último"] - ETH.df.resample('Y').first()["Último"]


#fig0, ax0 = plt.subplots()
#sns.lineplot(data=PLOT_ANUAL, ax=ax0,label="ETH")

''' retorno acumulativo '''
#ETH.df["Retorno_acumulado"] = (ETH.df.Último.pct_change()[1:]+1).cumprod() - 1

''' retorno acumulativo dos últimos 12 meses'''
(ETH.df["Retorno"].last("12M")+1).cumprod()-1
''' Retorno ano a ano'''

'''============================================================================='''

def print_anual_info(classe):
    '''Aplitute entre máximo e mínimo anual'''
    
    RETORNO = classe.df["Retorno"].groupby(lambda x:x.year).mean().to_frame().rename({"Retorno":"Média do retorno"},axis=1)
    RETORNO["Média Amp_max_min"] = classe.df.groupby(lambda x: x.year).max()["Máxima_norm"] - classe.df.groupby(lambda x: x.year).min()["Mínima_norm"]
    RETORNO["Variância do retorno"] = classe.df["Retorno"].groupby(lambda x:x.year).var()
    RETORNO["Desvio Padrão do retorno"] = classe.df["Retorno"].groupby(lambda x:x.year).std()
    RETORNO["Retorno ano a ano"] = (classe.df.groupby(lambda x: x.year).last()["Último"] - classe.df.groupby(lambda x: x.year).first()["Último"])/classe.df.groupby(lambda x: x.year).first()["Último"]
    print('\n',RETORNO)
    return RETORNO

def print_single_info(classe):
    print("\nRetorno acumulado total: ",((classe.df.Último.pct_change()[1:]+1).cumprod() - 1).iloc[-1])
    print("Retorno acumulado 12M: ",((classe.df["Retorno"].last("12M")+1).cumprod()-1).iloc[-1])
    print("Média da variação máximo-mínimo diário: ",classe.df["Aplitude_max_mix_diário"].mean())
    print("Média da variação fechamento-abertura diário: ",classe.df["Aplitude_fechamento_abertura_diário"].mean())
    print("Quantidade de gaps: ", sl.gap_count(classe.df))
    print("Quantidade de gaps fechados: ", sl.gap_closing_count(classe.df))


'''============================================================================='''
RETORNO = print_anual_info(ETH)
RETORNO = print_anual_info(IBV)
RETORNO = print_anual_info(NDQ)

SINGLE = print_single_info(IBV)

#ETH.df["Retorno"].resample('Y').get_group(pd.to_datetime("2017-12-31 00:00:00")).sort_values()


df1_ETH = ETH.df
df2_IBV = IBV.df
df3_NDQ = NDQ.df

df = ETH.df["Último_norm"].copy().index
df_ETH = ETH.df["Último_norm"].copy()

'''============================================================================='''
'''Correlação entre fechamento de ativos '''

corr_df = IBV.df[["Último"]].copy().rename(columns={'Último':'IBV'})
corr_df["NDQ"] = NDQ.df[["Último"]]
corr_df["ETH"] = ETH.df[["Último"]]
corr_df = corr_df.corr()

'''Printing color maps'''
fig, ax_corr = plt.subplots()
sns.heatmap(corr_df,annot=True,cmap='coolwarm', ax=ax_corr)
ax_corr.set_title("Correlação de fechamento")


'''Correlação entre fechamento de ativos janela de 45 dias'''

corr_ETH_IBV = ETH.df["Último"].rolling(45).corr(IBV.df["Último"])
corr_ETH_NDQ = ETH.df["Último"].rolling(45).corr(NDQ.df["Último"])
corr_NDQ_IBV = NDQ.df["Último"].rolling(45).corr(IBV.df["Último"])


fig, corr_axes = plt.subplots(3)
sns.lineplot(x=corr_ETH_IBV.index, y =corr_ETH_IBV,ax=corr_axes[0],label="IBV-ETH",color='g')
sns.lineplot(x=corr_ETH_NDQ.index, y =corr_ETH_NDQ,ax=corr_axes[1],label="ETH-NDQ",color='b')
sns.lineplot(x=corr_NDQ_IBV.index, y =corr_NDQ_IBV,ax=corr_axes[2],label="NDQ-IBV",color='r')
corr_axes[0].set_title("Corelação numa janela de 45 dias")

ETH.df["Último"].resample('45D').apply(lambda x: x.corr(IBV.df["Último"]))
ETH.df["Último"].rolling(45,step=45).apply(lambda x: x.corr(IBV.df["Último"]))


'''============================================================================='''
'''Calculando quantas vezes ouve GAP'''
#Subtrai a abertura pelo fechamento do dia anterior
#Se for diferente de zero é um gap e retorna true ou false
#Soma todos os trues resultando na  quantidade de gaps
((ETH.df["Abertura"] - ETH.df["Último"].shift(1)).dropna() != 0).sum()

ETH.df[((ETH.df["Abertura"] - ETH.df["Último"].shift(1)) != 0)]

'''Calculando a média de GAP '''

GAP = (ETH.df["Abertura"] - ETH.df["Último"].shift(1)).fillna(0)
GAP = GAP[(GAP!=0)]
GAP_abs = GAP.apply(lambda x:abs(x))
GAP_mean = GAP.groupby(lambda x:x.year).mean()


''' Calculando quantas vezes o GAP foi fechado '''
print(sl.gap_closing_count(ETH.df))
    

'''============================================================================='''
'''Starting plot'''
fig, ax = plt.subplots(2,2)
sns.scatterplot(x=ETH.df['Último'], y =IBV.df['Último'],ax=ax[0][0])
ax[0][0].set_ylabel("IBOVESPA")
ax[0][0].set_xlabel("ETHUSD")
ax[0][0].set_title("Correlação de fechamento normalizado")
sns.scatterplot(x=ETH.df['Último'], y =NDQ.df['Último'],ax=ax[0][1])
ax[0][1].set_ylabel("NASDAQ")
ax[0][1].set_xlabel("ETHUSD")
ax[0][1].set_title("Correlação de fechamento normalizado")
sns.scatterplot(x=NDQ.df['Último'], y =IBV.df['Último'],ax=ax[1][0])
ax[1][0].set_xlabel("NASDAQ")
ax[1][0].set_ylabel("IBOVESPA")
ax[1][0].set_title("Correlação de fechamento normalizado")
line_1 = sns.lineplot(x=NDQ.df.index, y =IBV.df['Último_norm'],ax=ax[1][1],label="IBV",color='g')
line_2 = sns.lineplot(x=NDQ.df.index, y =NDQ.df['Último_norm'],ax=ax[1][1],label="NDQ",color='b')
line_3 = sns.lineplot(x=NDQ.df.index, y =ETH.df['Último_norm'],ax=ax[1][1],label="ETH",color='r')
ax[1][1].set_ylabel("Fechamento")
#fig.subplots_adjust(hspace=0.5,top=0.99,botton=0.1)
ax[1][1].set_title("Fechamento normalizado por ano")
#ax[1][1].legend(handles=[line_1,line_2,line_3], title="Ativos")
ax[1][1].legend(title="Ativos")
fig.tight_layout()

'''
def plot_all_series(ETH,NDQ,IBV):
    fig, ax1 = plt.subplots(2,1)
    sns.lineplot(x=ETH.df.index, y=IBV.df['Último_norm'], ax=ax1[0],label="IBOVESPA")
    sns.lineplot(x=ETH.df.index, y=ETH.df['Último_norm'], ax=ax1[0],label = "ETHUSD")
    sns.lineplot(x=ETH.df.index, y=NDQ.df['Último_norm'], ax=ax1[0], label = "NASDAQ")
    ax1[0].legend(title="Ativos")
    
 '''   
def plot_all_series(ETH,NDQ,IBV):
    for col in ETH.df.iloc[:,4:]:
        fig, ax1 = plt.subplots(2,1)
        sns.lineplot(x=ETH.df.index, y=IBV.df[col], ax=ax1[0],label="IBOVESPA")
        sns.lineplot(x=ETH.df.index, y=sl.drawdown(IBV.df[col]).squeeze(), ax=ax1[1],label="IBOVESPA")
        sns.lineplot(x=ETH.df.index, y=ETH.df[col], ax=ax1[0],label = "ETHUSD")
        sns.lineplot(x=ETH.df.index, y=sl.drawdown(ETH.df[col]).squeeze(), ax=ax1[1],label="ETHUSD")
        sns.lineplot(x=ETH.df.index, y=NDQ.df[col], ax=ax1[0], label = "NASDAQ")
        sns.lineplot(x=ETH.df.index, y=sl.drawdown(NDQ.df[col]).squeeze(), ax=ax1[1],label="NASDAQ")
        ax1[0].legend(title="Ativos")

plot_all_series(ETH,NDQ,IBV)

sl.plot_series_single(ETH,"ETHUSD")
sl.plot_retorno(ETH,"ETHUSD")
sl.plot_series_single(IBV,"IBOVESPA")
sl.plot_retorno(IBV,"IBOVESPA")
sl.plot_series_single(NDQ,"NASDAQ")
sl.plot_retorno(NDQ,"NASDAQ")

'''Plot gráfico anual '''

''' Alterantive method
fig, ax2 = plt.subplots()
#IBV.df.groupby(lambda x: x.year).apply(lambda col: sns.lineplot(x=col.index.dayofyear, y=col["Retorno"]*100, ax=ax2,label=col.index.year[1]))
IBV.df.groupby(lambda x: x.year).apply(lambda col: sns.lineplot(x=col.index.day_of_year, y=col["Retorno"]*100, ax=ax2,label=col.index.year[1]))
'''

'''Questão 9 - Plot gráfico anual '''


def anual_returo(classe):
    date_form = DateFormatter("%m-%d")
    fig, ax2 = plt.subplots()
    ax2.xaxis.set_major_formatter(date_form)
    for year, df in classe.df.groupby(lambda x: x.year):
        sns.lineplot(x=df.index.dayofyear, y=df["Retorno"]*100, ax=ax2,label=year)
        
anual_returo(IBV)
anual_returo(ETH)
anual_returo(NDQ)
'''Questão 10 - histogrma com retorno '''
fig, ax3 = plt.subplots(2,2)
sns.histplot(x=NDQ.df["Retorno"] ,bins=100, ax=ax3[0][0],label="NDQ",color='r')
ax3[0][0].legend()

sns.histplot(x=IBV.df["Retorno"] ,bins=100, ax=ax3[0][1],label="IBV")
ax3[0][1].legend()
#ax3[1][0].set_xlim(-50,50)
sns.histplot(x=ETH.df["Retorno"] ,bins=100, ax=ax3[1][0],label="ETH",color='g')
ax3[1][0].legend()

sns.histplot(x=NDQ.df["Retorno"] ,bins=100, ax=ax3[1][1],label="NDQ")
sns.histplot(x=IBV.df["Retorno"] ,bins=100, ax=ax3[1][1],label="IBV")
sns.histplot(x=ETH.df["Retorno"] ,bins=100, ax=ax3[1][1],label="ETH")
ax3[1][1].legend()

'''Questão 11 - drawdown'''
drawd = sl.drawdown(ETH.df['Retorno'])

    #sns.lineplot(x=df.index, y=df["Retorno"]*100, ax=ax2,label="ano")
#ax.set_xticklabels()
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
# ax.yaxis.set_visible(False)
# ax.xaxis.set(ticks=range(1,1500,100))
# plt.show()

#sns.lineplot(data=ETH.df,x=ETH.df.index, y="Vol.",hue="Var%", style="Var%")

