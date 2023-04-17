# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:19:53 2023

@author: thuli
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

DF = pd.read_excel("C:/Users/thuli/Documents/Paradas.xlsx")
DF = DF.iloc[:,:3]
DF2 = DF.groupby(["Ativo", "Código da Parada"]).count()
DF2 = DF.groupby(["Ativo"]).apply(lambda x: x["Código da Parada"].value_counts().head(3))
DF4 = DF2.reset_index()
DF4.rename(columns={"Código da Parada":"Ocorrência","level_1":"Código"},inplace=True)
DF3= DF2.unstack()
DF3= DF2.unstack().reset_index()
DF2.index[0][0] == 'Conversion Press 11'
CP11 = (DF4[DF4["Ativo"] == "Conversion Press 11"])
CP12 = (DF4[DF4["Ativo"] == "Conversion Press 12"])
CP26 = (DF4[DF4["Ativo"] == "Conversion Press 26"])
CP27 = (DF4[DF4["Ativo"] == "Conversion Press 27"])

ax1 = sns.countplot(data = DF, x="Ativo",hue="Código da Parada")
plt.show()

fig,ax = plt.subplots()
sns.barplot(data = DF4, x="Ativo",y="Ocorrência",hue="Código")

plt.show()

sns.set_theme(style="white")
sns.color_palette()  

#plt.rcdefaults()


fig,ax = plt.subplots(2,2)

sns.barplot(data = CP11, x = "Ativo",y="Ocorrência",hue="Código",ax=ax[0][0], width=0.3, saturation=1) 
sns.barplot(data = CP12, x = "Ativo",y="Ocorrência",hue="Código",ax=ax[0][1], width=0.3, saturation=1)
sns.barplot(data = CP26, x = "Ativo",y="Ocorrência",hue="Código",ax=ax[1][0], width=0.3, saturation=1)
sns.barplot(data = CP27, x = "Ativo",y="Ocorrência",hue="Código",ax=ax[1][1], width=0.3, saturation=1)

for i in range(2):
    for j in range(2):
        for container in ax[i][j].containers:
            ax[i][j].bar_label(container)
        ax[i][j].set(xlabel=None)
plt.show()