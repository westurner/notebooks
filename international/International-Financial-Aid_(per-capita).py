
# coding: utf-8

# # International Financial Aid (per-capita) [World Bank 1960-2013]
# 
# Datasets:
# * http://data.worldbank.org/indicator/DT.ODA.ALLD.CD/countries/1W
# * http://data.worldbank.org/indicator/SP.POP.TOTL
# 

# In[1]:

#!pip install conda
#!conda install --yes pandas matplotlib


# In[2]:

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import json
    
print(pd.__version__, np.__version__)


# In[103]:

datadir = "aid_data"

import os
os.path.exists(datadir) or os.makedirs(datadir)

# http://data.worldbank.org/indicator/DT.ODA.ALLD.CD/countries/1W
wb_net_aid_received_zip = os.path.join(datadir, "wb_net_aid_received.zip")
get_ipython().system(u'wget --continue --no-clobber "http://api.worldbank.org/v2/en/indicator/dt.oda.alld.cd?downloadformat=csv" -O $wb_net_aid_received_zip')
#!ls -al $datadir
wb_net_aid_received_csv_name = "dt.oda.alld.cd_Indicator_en_csv_v2.csv"
#!ls unzip -l $wb_net_aid_received_csv_name
get_ipython().system(u'unzip -u $wb_net_aid_received_zip "$wb_net_aid_received_csv_name" -d $datadir')
#!ls -al $datadir
wb_net_aid_received_csv = os.path.join(datadir, wb_net_aid_received_csv_name)

# http://data.worldbank.org/indicator/SP.POP.TOTL
wb_pop_total_zip = os.path.join(datadir, "wb_pop_total.zip")
get_ipython().system(u'wget --continue --no-clobber "http://api.worldbank.org/v2/en/indicator/sp.pop.totl?downloadformat=csv" -O $wb_pop_total_zip')
#!ls -al $datadir
#!unzip -l $wb_pop_total_zip
wb_pop_total_csv_name = "sp.pop.totl_Indicator_en_csv_v2.csv"
get_ipython().system(u'unzip -u $wb_pop_total_zip $wb_pop_total_csv_name -d $datadir')
#!ls -al $datadir
wb_pop_total_csv = os.path.join(datadir, wb_pop_total_csv_name)

# http://www.oecd.org/dac/stats/aidtopoorcountriesslipsfurtherasgovernmentstightenbudgets.htm
oecd_aid_statistics_xls = os.path.join(datadir, "oecd_aid_statistics.xls")
get_ipython().system(u'wget --continue --no-clobber "http://www.oecd.org/development/stats/ODA%202012%20Tables%20and%20Charts.xls" -O $oecd_aid_statistics_xls')

get_ipython().system(u'ls -al $datadir')


# In[104]:

df_net_aid = pd.read_csv(wb_net_aid_received_csv, header=2)
df_net_aid


# In[20]:

df_pop_total = pd.read_csv(wb_pop_total_csv, header=2)
df_pop_total


# In[24]:

df_net_aid[['Country Name', 'Country Code', '2012']]


# In[25]:

df_pop_total[['Country Name', 'Country Code', '2012']]


# In[31]:

df_aid_pop = pd.merge(df_net_aid, df_pop_total,
                      on='Country Code',
                      how='outer',
                      suffixes=('_aid', '_pop'))
df_aid_pop.head()


# In[86]:

for year in xrange(1960, 2012 + 1):
    aidcolumn = '%d_aid' % year
    popcolumn = '%d_pop' % year
    aidpercapitacolumn = '%d_aid_per_capita' % year
    df_aid_pop[aidpercapitacolumn] = df_aid_pop[aidcolumn] / df_aid_pop[popcolumn]
    
path = 'wb_aid_per_capita_1960-2013.csv'
df_aid_pop.to_csv(path)

df_aid_pop


# In[92]:

df_per_capita_2012 = df_aid_pop[['Country Code', 'Country Name_aid',
                            '2012_aid', '2012_pop', '2012_aid_per_capita']]
df_per_capita_2012


# In[93]:

df_per_capita_2012.sort(columns=['2012_aid_per_capita'])


# In[94]:

df_per_capita_2012.sort(columns=['2012_aid_per_capita'], ascending=False)


# In[95]:

df_per_capita_2012[
    df_per_capita_2012['2012_aid_per_capita']
    .isnull()
]


# In[96]:

(df_per_capita_2012[
    df_per_capita_2012['2012_aid_per_capita']
    .notnull()
].sort('2012_aid_per_capita', ascending=False))


# In[98]:

get_ipython().system(u'pwd')
path = None  # "wb_aid_per_capita_2012.csv"
print(df_per_capita_2012.to_csv(path))


# In[ ]:



