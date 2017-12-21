
# coding: utf-8

# In[8]:

0.6 * 0.7


# In[9]:

(0.6+1)*(0.7+1)


# In[10]:

((0.6+1)*(0.7+1)) - 1


# In[11]:

((0.6+1)*(0.7+1)) - 1 - (0.6 * 0.7)


# In[12]:

((0.6+1)*(0.7+1)) - 1 - (0.6 * 0.7) - 0.6


# In[13]:

((0.6+1)*(0.7+1)) - 1 - (0.6 * 0.7) - 0.6 == 0.7


# In[14]:

import numpy as np
print(np.allclose(((0.6+1)*(0.7+1)) - 1 - (0.6 * 0.7) - 0.6, 0.7))


# In[15]:

def an_oddity(a, b):
    output = ((a+1)*(b+1)) - 1 - (a*b) - a
    #print(output)
    return np.allclose(output, b)


# In[16]:

an_oddity(0.6, 0.7)


# In[17]:

an_oddity(0.8, 0.9)


# In[18]:

an_oddity(0.2, 0.9)


# In[19]:

all((an_oddity(a,b) for (a,b) in np.random.randn(1000, 2)))


# In[ ]:



