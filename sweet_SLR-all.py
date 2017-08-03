
# coding: utf-8

# # Sea Level Rise data from Sweet et al (2017)
# described in  https://tidesandcurrents.noaa.gov/publications/techrpt83_Global_and_Regional_SLR_Scenarios_for_the_US_final.pdf

# In[1]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd


# In[2]:

df = pd.read_csv('techrpt083.csv', skiprows=15)


# In[3]:

df.shape


# In[4]:

def df_station(df, station):
    df2 = df[df['Site'].str.contains(station)]
    df3 = df2[df2['Scenario'].str.contains("1.0 - HIGH")]
    df4 = pd.melt(df3, id_vars=df3.columns.values[0:6], 
                  var_name="Date", value_name="Value")
    df5 = df4.copy(deep=True)
    for scenario in df2['Scenario'].values:
        df3 = df2[df2['Scenario'].str.contains(scenario)]
        var = scenario.replace(' ','')
        df4 = pd.melt(df3, id_vars=df3.columns.values[0:6], 
                      var_name="Date", value_name=var)
        df5[var] = df4[var]
    return df5


# In[5]:

df3 = df[~df['Site'].str.contains('GMSL')]


# In[6]:

dfs = [df_station(df3,station) for station in df3['Site'].unique()]


# In[7]:

type(dfs)


# In[8]:

df6 = pd.concat(dfs)


# In[9]:

del df6['Value']
del df6['Scenario']


# In[14]:

del df6['PSMSL ID']


# In[10]:

df6['Date'] = [int(re.findall(r'\d+', v)[0]) for v in df6['Date'].values]
df6.rename(columns = {'Site':'id'}, inplace = True)


# In[15]:

df6.to_csv('all_stations.csv', index=False)


# In[12]:

df6


# In[ ]:



