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

ETH = sl.OALL(pd.read_csv("ETHUSD.csv"))
IBV = sl.OALL(pd.read_csv("IBOVESPA.csv"))
NDQ = sl.OALL(pd.read_csv("NASDAQ.csv"))
df1 = ETH.df
df2 = IBV.df
df3 = NDQ.df

sl.do_all(ETH, IBV, NDQ)

print(ETH.df.head(10))
print(IBV.df.columns)

#fig,ax = plt.subplots()
type(ETH.df.iloc[1,-2])
#ax.scatter(ETH.df['Vol.'],ETH.df['Var%'])
df1 = ETH.df
df2 = IBV.df
df3 = NDQ.df



df1 = df1.applymap(sl.conv)








'''
older_date = [df1.index[0],df2.index[0],df3.index[0]]
older_date.sort()
older_date[-1]
df1_new = df1[df1.index >= older_date[-1]]
df2_new = df2[df2.index >= older_date[-1]]
df3_new = df3[df3.index >= older_date[-1]]
latest_date = [df1.index[-1],df2.index[-1],df3.index[-1]]
latest_date.sort()
'''

#ax.set_xticklabels()
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.yaxis.set_visible(False)
ax.xaxis.set(ticks=range(1,1500,100))
plt.show()

#sns.lineplot(data=ETH.df,x=ETH.df.index, y="Vol.",hue="Var%", style="Var%")

