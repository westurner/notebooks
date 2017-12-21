
# coding: utf-8

# In[3]:

get_ipython().magic(u'pinfo %matplotlib')


# In[1]:

get_ipython().magic(u'matplotlib inline')
#%pylab inline
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import json

import quandl
import os

from IPython.display import display

#KEY = '...'
#!mkdir ./.keys
#with open('./.keys/quandl-api-key.json','w') as f:
#    json.dump({'key': KEY}, f)

KEYFILE = './.keys/quandl-api-key.json'
if os.path.exists(KEYFILE):
    with open('./.keys/quandl-api-key.json','r') as f:
        quandl_token = json.load(f)['key']
        
    import functools
    _quandl_get = functools.partial(quandl.get, authtoken=quandl_token)
else:
    _quandl_get = quandl.get
    
print(pd.__version__, np.__version__)
fig = plt.figure()


# In[ ]:

# http://www.quandl.com/FRED-Federal-Reserve-Economic-Data/USARGDPR-Real-GDP-in-the-United-States
# http://www.quandl.com/FRED-Federal-Reserve-Economic-Data/GDP-Gross-Domestic-Product-1-Decimal
# http://www.quandl.com/FRED-Federal-Reserve-Economic-Data/FYGFD-Gross-Federal-Debt
# http://www.quandl.com/FRED-Federal-Reserve-Economic-Data/USAPOPL-Population-in-the-United-States
# http://www.quandl.com/FRED-Federal-Reserve-Economic-Data/CPIAUCSL-Consumer-Price-Index-for-All-Urban-Consumers-All-Items-USA-Inflation
import collections
_data = collections.OrderedDict()
for _key in ['FRED/USARGDPR', 'FRED/GDP', 'FRED/FYGFD', 'FRED/USAPOPL', 'FRED/CPIAUCSL']:
    _data[_key.replace('/','_')] = _quandl_get(_key)


# In[ ]:

mpl.rcParams['figure.figsize'] = (20,4)


# In[ ]:


#for k,v in _data.iteritems():
#    v.plot(
#        title=k,
#        xlim=('1940','2020'),
#        ylim=(0, v.max()),
#        xticks=[str(x) for x in range(1949,2017,4)],
#        #x_compat=True,
#)
#usargdpr.plot(), usagdp.plot(), fygfd.plot(), popl.plot()
#usargdpr.


# In[ ]:

_data['FRED_USARGDPR'].head(), _data['FRED_FYGFD'].head()


# In[ ]:

((_data['FRED_USARGDPR'].resample('A', how='mean'))
 / _data['FRED_FYGFD'].resample('A', how='mean')).plot(title='USARGDPR / FYGFD')
((_data['FRED_GDP'].resample('A', how='mean'))
 / _data['FRED_FYGFD'].resample('A', how='mean')).plot(title='GDP / FYGFD')


# In[ ]:

((_data['FRED_GDP'].resample('A', how='mean'))
 / _data['FRED_USAPOPL'].resample('A', how='mean')).plot(title='FRED_GDP / FRED_USAPOPL')


# In[ ]:

((_data['FRED_FYGFD'].resample('A', how='mean'))
 / _data['FRED_GDP'].resample('A', how='mean')).plot(title='FRED_FYGFD / FRED_GDP')


# In[ ]:

plot = _data['FRED_CPIAUCSL'].resample('A', how='mean').plot(
    xticks=[str(x) for x in range(1949,2017,4)],
    x_compat=True,
    title="Yearly Inflation (CPI)"
    )
plot.legend(loc='upper left')


def add_line(plot, _year, text=None):
    _max = plot.yaxis.get_view_interval()[-1]
    plot.plot((_year,_year), (0, _max),
            color='gray', linewidth=1.5, linestyle="--")
    plot.annotate(
                text if text is not None else _year,
                xy=(_year, 0),
                xycoords='data',
                xytext=(+10, +30),
                textcoords='offset points',
                fontsize=12,
                #arrowprops=dict(arrowstyle="->"), #, connectionstyle=""), #arc3,rad=.2"),
                rotation='vertical',
                verticalalignment='bottom',
                horizontalalignment='center')

for year in range(1949, 2017, 4):
    add_line(plot, str(year))

display(plot)


# In[ ]:

us_presidents_csv_url = 'https://commondatastorage.googleapis.com/ckannet-storage/2012-05-08T122246/USPresident-Wikipedia-URLs-Thmbs-HS.csv' 


# In[ ]:


def get_presidents_df(data_file='./data/us_presidents.csv', data_url=us_presidents_csv_url):
    datadir = os.path.dirname(data_file)
    os.path.exists(datadir) or os.makedirs(datadir)
    get_ipython().system(u'wget --continue --no-clobber $data_url -O $data_file')
    df = presidents = pd.read_csv(data_file)
    
    df = presidents[['President ','Took office ','Left office ']]
    df['Took office '] = pd.to_datetime(presidents['Took office '])
    df['Left office '] = pd.to_datetime(presidents['Left office '], coerce=True)
    #display(df)
    df = df.set_index('Took office ', drop=False, verify_integrity=True)
    df['term'] = df['Left office '] - df['Took office ']
    
    col = df['term']
    val = col[0]
    df['term'] = (
        col.apply(
            lambda x: x.astype('datetime64'),
            convert_dtype=False))
    col = df['term']
    val = col[0]
    print(val)
    
    #val.item().days
    #df['terms'] = df['term'].apply(
    #    lambda x: (x.item().days if x.item() else 0)
    #    / float(365.25*4))
    return df

#df['terms'] = (df['term'] / np.timedelta64(1, 'D')) / float(365.25*4) # pandas 0.13

df = get_presidents_df()
display(df.head())

def presidents_by_year(df=None):
    if df is None:
        df = get_presidents_df()
    for year,name in df.ix[:,['President ']].to_records():
        print(year.year, name)

def add_presidents(plot, presidents=None, yearmin=0):
    if presidents is None:
        presidents = get_presidents_df()

    for year,name in presidents.ix[str(yearmin):,['President ']].to_records():
        #print year.year, name
        add_line(plot, year, name)

def poli_plot(df, **kwargs):
    yearmin = df.index.min().year
    yearmax = 2017
    
    plot = df.plot(
        xticks=[str(x) for x in range(yearmax, yearmin,-4)],
        x_compat=True,
        **kwargs)
    plot.legend(loc='upper left')
    
    add_presidents(plot, yearmin=yearmin)
    return plot


# In[ ]:


df = _data['FRED_CPIAUCSL']
poli_plot(df)


# In[ ]:

df = ((_data['FRED_GDP'].resample('A', how='mean')) / _data['FRED_USAPOPL'].resample('A', how='mean'))
poli_plot(df, title="GDP per capita (thousands of dollars)")


# In[ ]:

df = ((_data['FRED_FYGFD'].resample('A', how='mean')) / _data['FRED_USAPOPL'].resample('A', how='mean'))
poli_plot(df, title="Federal debt per capita (thousands of dollars)")


# In[ ]:


inflation_factor_linear = (_data['FRED_CPIAUCSL'] / _data['FRED_CPIAUCSL'].max()).resample('A', how='mean')
inflation_factor_uhh = 1 / inflation_factor_linear
cpi = inflation_factor_uhh
#display( cpi.head()) 
#display( cpi.tail())


df = ((_data['FRED_FYGFD'].resample('A', how='mean')) / _data['FRED_USAPOPL'].resample('A', how='mean'))
#print( df.columns )

scaled = (df * cpi)
#display(scaled.tail())
display(poli_plot(_data['FRED_CPIAUCSL'], title="inflation (FRED CPI UCSL)"))
plot = poli_plot(_data['FRED_CPIAUCSL'].resample('A','mean').pct_change(), title='yearly % change in inflation')
plot.axhline()

display(plot)


display(poli_plot(df, title="debt-per-capita"))
display(poli_plot(scaled, title="debt-per-capita scaled for inflation"))
plot = poli_plot(scaled.pct_change(), title="Yearly % change in debt-per-capita scaled for inflation")
plot.axhline()
display(plot)


#poli_plot(df)
#poli_plot(df * inflation_factor_linear)


# In[ ]:




# In[ ]:

# TODO: add house/senate majority party
# TODO: add major wars


# In[ ]:

get_ipython().system(u'wget --continue --no-clobber https://github.com/unitedstates/congress-legislators/raw/master/legislators-historical.yaml -O ./data/legislators-historical.yaml')
get_ipython().system(u'wget --continue --no-clobber https://github.com/unitedstates/congress-legislators/raw/master/legislators-current.yaml -O ./data/legislators-current.yaml')
#import yaml
#data = None
#with open('./data/legislators-historical.yaml','rb') as f:
#    data = yaml.load(f)
get_ipython().system(u'ls ./data')


# In[ ]:

import yaml
def iter_members(
    data_files=['./data/legislators-historical.yaml',
                './data/legislators-current.yaml']):
    
    for data_file in data_files:
        data = None
        with open(data_file,'rb') as f:
            data = yaml.load(f)
        for m in data:
            for t in m['terms']:
                yield (
                    t['state'],
                    t['type'],
                    t['start'],
                    t['end'],
                    t.get('party'),
                    m['name']['first'],
                    m['name']['last'],
                    m.get('bio',{}).get('gender', 'M'), # ...
                    m.get('bio',{}).get('birthday')
                )
iter_members.columns = [
    'state',
    'type',
    'start',
    'end',
    'party',
    'first',
    'last',
    'gender',
    'birthday'
]

_legislator_data = list(iter_members())


# In[ ]:

df = pd.DataFrame.from_records(
    _legislator_data,
    columns=iter_members.columns)
df['start'] = pd.to_datetime(df['start'])
df['end'] = pd.to_datetime(df['end'])
df['birthday'] = pd.to_datetime(df['birthday'])
df.set_index('start', drop=False, inplace=True)
display(df.head())
display(df)


# In[ ]:

col = df['party']
uniques = dict.fromkeys(col.unique())
#print(uniques)

_party_map = {}
repub, democ, other = [], [], []
for x in uniques:
    if x is not None:
        if 'Republ' in x:
            repub.append(x)
            _party_map[x] = 'Republican'
        elif 'Democr' in x:
            democ.append(x)
            _party_map[x] = 'Democrat'
        else:
            other.append(x)
            _party_map[x] = 'Other' # ...
    else:
        other.append(x)
        _party_map[x] = 'Other' # ...
        

print(len(repub), repub)
print(len(democ), democ)
print(len(other), other)


# In[ ]:


display(df['1949':]['party'].value_counts())
display(df[df['party']=='Liberal'])


# In[ ]:

# print(df2[df2['state'] == 'NE'][['type', 'party','first','last']].sort().to_string())


# In[ ]:

print('# party')
print(df[df['state'] == 'NE']['party'].value_counts(normalize=True))
print('# type')
print(df[df['state'] == 'NE']['type'].value_counts())


# In[ ]:

df['two_party_fail'] = df['party'].apply(lambda x: _party_map.get(x))
display( df['two_party_fail'].value_counts() )
display( df['two_party_fail'].value_counts(normalize=True) )


# In[ ]:

# objective: draw chart with per-year, per-two-party-counts
# group by year
# count factors

def start_year(x):
    return x.year - (x.year % 2)

grouper = df.groupby([start_year, 'two_party_fail'])

whoa = grouper.aggregate({'two_party_fail':len}).unstack()

display(whoa.plot())
display(whoa.head())
display(whoa.tail())

#df.pivot_table(values='two_party_fail', cols=['start'], aggfunc=len)


# In[ ]:

grouper = df.groupby([start_year, 'gender'])

whoa = grouper.aggregate({'gender':len}).unstack()
display(whoa.plot())


# In[2]:

# Q. how are these misleading / maybe not as helpful as they could be?
# 1. they count by start year, so they don't show the state at any given time
#    to show the state at any given time would require
#    a 'currently_serving' function
#    which, one might think could take into account standard terms/elections
#    as appropriate for rep/sen,
#    but there are special cases in mid-stream

# 2. they do not stratify by rep/sen; the counts are lumped together
#    'share_y' split by 'type' might be helpful

# ... how many hours would it take to draw these in [spreadsheet tool]
#     only to realize that you have no idea what 
#     'settings' were used to create a (very beautiful) chart?
#     ... python tools for visual studio now support 
#         something like `ipython --pylab=inline/qt`
#         ... i work on various platforms, so that's not an option for me
#         ... not sure what sort of configuration is required to get
#             anaconda ce working with this ide
#     ... ipython qt, ipython notebook
#     ... spyder ide
#     ... you can run these as scheduled jobs which generate online charts,
#         but then, still, without the source,
#         what smoke are you
# ... "you can get a good look at a t-bone steak by"

