#!/usr/bin/env python
# coding: utf-8

# # Change the base (radix) of a number
# 
# ## References
# - https://en.wikipedia.org/wiki/Radix
# - https://en.wikipedia.org/wiki/Positional_notation#Base_conversion
# 
# $$ n_{radix} $$
# $$ 16_{10} = 10000_2 $$

# In[6]:


get_ipython().run_line_magic('pfile', './basechange.py')


# In[8]:


get_ipython().system('pytest ./basechange.py')

