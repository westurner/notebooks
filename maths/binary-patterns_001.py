
# coding: utf-8

# # Binary Patterns 001
# Author: @westurner

# ## combinations and probabilities

# In[1]:

# this is "wrong"
# probability of feature 1, probability of feature 2

p1 = 0.5
p2 = 0.7
p1 + p2


# In[2]:

# this is "wrong"
p1 * p2


# In[3]:

# what is this called?
# reasoning: numbers smaller than 1 multiplied get smaller
print((1+p1)*(1+p2)-1)


# In[4]:

print((1+p1)*(1+p2)-(1*2))


# ## a simple binary game

# In[5]:

# w,x,y,z,  s
s1 = [
[[1,0,1,0], 1],
[[0,0,0,1], 0],
[[1,1,1,0], 1],
[[0,0,1,0], 1]
]
s2 = [
[[1,0,1,0], 1],
[[0,0,0,1], 0],
[[1,1,1,0], 1],
[[0,0,1,0], 0]
]
print(s1)
print(s2)


# what are the relation(s) between the features w,x,y,z and s?
# 
# with human intuition, we can see that for
# - s1: s is always 1 when y is 1
# - s1: s is always 0 when y is 0
# - s2: s is always 1 when (w,y) is (1,1)
# - s2: s is always 0 when (w) is 0

# In[6]:

from collections import defaultdict, OrderedDict
class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *a, **kw):
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory


# In[7]:

for ((w,x,y,z), s) in s1:
    print(w,x,y,z,s)
    
import itertools
import operator

def find_features(s1):
    f = OrderedDefaultDict(lambda: 0)
    feature_names = 'wxyzs'
    for ((w,x,y,z), s) in s1:
        features = locals()
        for r in range(1, len(feature_names)+1):
            for comb in itertools.combinations(feature_names[:-1], r):  # *
                if features[feature_names[-1]]:  # *
                    features_ = [features.get(comb[i], 0) for i in range(r)]
                    f[('AND', comb)] += all(features_)
                    if r > 1:
                        f[('OR', comb)] += reduce(operator.or_, features_)
                        f[('XOR', comb)] += reduce(operator.xor, features_)
    #print(json.dumps(f, indent=2))
    f_inv = sorted(
        ((v,k) for (k,v) in f.items()),
        key=lambda x: (x[0], len(feature_names) - len(x[1][1]), x[1]), # TODO: occam's razor
        reverse=True)

    for count_, features_ in f_inv:
        if features_ != ('s',) and count_ > 0: #and 's' in features:  # *
            print("%s: %s" % (count_, features_))
print('# s1')
find_features(s1)
print('# s2')
find_features(s2)


# Wow, that's a lot of solutions. A few observations:
# 
# - That's more solutions than I intended in conjuring ``s1`` and ``s2`` as test cases.
#   - My brain and visual cortex seem to test mostly just for ``AND``.
# - I could not filter out solutions containing s (``feature_names[:-1]``).
# - This may not be the best data structure for the problem: is there any reason to leave ``s`` out of the matrix?
#   - Would ``numpy.matrix`` be more efficient for this type of a combinatorics and logic problem?
#     - ``pandas.DataFrame`` would print prettier with ``_repr_html_``
#       - Is the ``.count()`` method of ``DataFrame`` useful for anything other than ``AND`` here?
# - I could reverse the ``range()`` of combination lengths ``r`` to test for more complex features first and then try and bisect by splitting features with higher frequencies in half in search of less complex features with greater frequency.
# - This still isn't the complete set of possible solutions:
#   - I filter out solutions with zero frequency. Is a ``NOT(solution_with_zero_frequency)`` likely to be ranked more highly?
#   - I only test for ``w AND x AND y AND z`` but not for variations like ``w AND x OR y XOR z``.
#     - I wish I could recall how associative boolean logic is. Would I also need to add parethesis for every possible grouping?
#       - ``w AND ((x OR y) XOR z)``
#         - ``0 AND .((0 OR 0) XOR 0)`` == ``0``
#         - ``1 AND  ((1 OR 1) XOR 1))`` == ``0``
#       - ``w AND (x OR (y XOR z))``
#         - ``0 AND .(0 OR (0 XOR 0))`` == ``0``
#         - ``1 AND (1 OR (1 XOR 1))`` == ``1`` ... not associative.
#     - At that number of combinations, is mutation or particle swarm optimization likely to find the solution first?
#       - Isn't there a more efficient way to do this without testing all possible logical strings?
#         - How is this problem similar or different to brute-force fuzzing a high-dimensional space?
