# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '..\\..\..\..\AppData\Local\Temp'))
	print(os.getcwd())
except:
	pass
# %%
from IPython import get_ipython

# %% [markdown]
# ## Explore different algorithm to extact all primary numbers

# %%
import numpy as np

# %% [markdown]
# ### Most primary method, scan all odd numbers by all odd numbers
# #### The running time without iteraction counting is about 15s

# %%
def pn_1(num = 1000):
    if num < 2:
        return []
    result = [2]
    n_iter = 0
    for n in range(3, num+1, 2):
        primary = True
        for i in range(3, n, 2):
            n_iter += 1
            if n%i == 0:
                primary = False
                break
        if primary:
            result.append(n)
    print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'print(len(pn_1(100000)))')

# %% [markdown]
# ### Scan odd numbers only by numbers lower than square root
# #### this significantly reduced iteration from 227.6M to 1.35M

# %%
def pn_2(num = 1000):
    if num < 2:
        return []
    result = [2]
    n_iter = 0
    for n in range(3, num+1, 2):
        primary = True
        for i in range(3, np.int(np.sqrt(n))+1, 2):
            n_iter += 1
            if n%i == 0:
                primary = False
                break
        if primary:
            result.append(n)
    print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'print(len(pn_2(100000)))')

# %% [markdown]
# ### Further reduced iteration by scanning by numbers primary numbers only.
# #### this reduced iterations by 50%, from 1.35M to 0.64M

# %%
def pn_3(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    result = [2, 3]
    p = 1
    m = 3
#     n_iter = 0
    for n in range(5, num+1, 2):
        primary = True 
        if np.int(np.sqrt(n)) >= m:
            p += 1
            m = result[p]
        for i in result[1:p]:
#             n_iter += 1
            if n%i == 0:
                primary = False
                break
        if primary:
            result.append(n)
#     print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'print(len(pn_3(100000)))')

# %% [markdown]
# ### On top of odd numbers, removed multipliers of 3
# #### Further compressed iterations to 0.63M
# Split numbers to bucket of 6, in every bucket, only check 1st and 5th number

# %%
def pn_4(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
#     n_iter = 0
    for q in range(7, num, 6):
        for n in [q, q+4]:
            primary = True
            if np.int(np.sqrt(n)) >= m:
                p += 1
                m = result[p]
            for i in result[1:p]:
#                 n_iter += 1
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
    if result[-1] > num:
        result = result[:-1]
#     print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_4(100000))')

# %% [markdown]
# ### Iteractions does not compressed in this version, only reverse comparison
# #### Rather than use square root of big number, compare square of smaller number, and eliminated using numpy package
# This reduced running time by about 50%, with the same number of iterations (120 ms above was when using iteraction counting, without counting, the running time was about 100 ms)

# %%
def pn_5(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
#     n_iter = 0
    for q in range(7, num, 6):
        for n in [q, q+4]:
            primary = True
            if m*m <= n:
                p += 1
                m = result[p]
            for i in result[1:p]:
#                 n_iter += 1
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
    if result[-1] > num:
        result = result[:-1]
#     print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_5(1000000))')

# %% [markdown]
# ### Trying to reduce computation of square, but increased running time slightly
# #### rather using square, tried to use adding difference on top of current number
# This introduced new variables, but did not successfully improve program performance

# %%
def pn_6(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    sq = 9
    m = 3
#     n_iter = 0
    for q in range(7, num, 6):
        for n in [q, q+4]:
            primary = True
            if sq <= n:
                p += 1
                r = result[p]
                sq += (r+m)*(r-m)
#                 print('sq:', sq, ', p:', p, ', n:', n, ', r:', r, ', m:', m)
                m = r
#                 m = result[p]
            for i in result[1:p]:
#                 n_iter += 1
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
    if result[-1] > num:
        result = result[:-1]
#     print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_6(1000000))')

# %% [markdown]
# ### Compressed iterations again by removing dividing by 3, as all multiplier of 3 has been removed
# #### This brings iterations from 0.63M to 0.59M, but total running time does not change so much
# When num = 1M, the running time can be reduced slightly (about 2.5%, from 820ms to 800ms)

# %%
def pn_7(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
#     n_iter = 0
    for q in range(7, num, 6):
        for n in [q, q+4]:
            if n>num:
                break
            primary = True
            if m*m <= n:
                p += 1
                m = result[p]
            for i in result[2:p]:
#                 n_iter += 1
#                 print('n = ', n, ', i = ', i)
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
#     if result[-1] > num:
#         result = result[:-1]
#     print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_7(100000))')


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_7(1000000))')


# %%
get_ipython().run_cell_magic('time', '', 'for i in range(100000):\n    p = i*i')


# %%
get_ipython().run_cell_magic('time', '', 'for i in range(100000):\n    p = i**2')


# %%
print(pn_7(100))


# %%
def pn_7_test(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
#     n_iter = 0
    for q in range(7, num, 6):
        for n in [q, q+4]:
            if n>num:
                break
            primary = True
            if m*m <= n:
                p += 1
                m = result[p]
            for i in result[2:p]:
#                 n_iter += 1
#                 print('n = ', n, ', i = ', i)
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
#     if result[-1] > num:
#         result = result[:-1]
#     print('Total iterations: {}'.format(n_iter))
    return result

# %% [markdown]
# ### Avoid to calulation of m*m for every numbers, rather, store its result in a varaible for the comparison
# When num = 1M, the running time can be reduced slightly (lowest running time reduced from ~805ms to 790ms)

# %%
def pn_8(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
    sq = 9
#     n_iter = 0
    for q in range(7, num, 6):
        for n in [q, q+4]:
            if n>num:
                break
            primary = True
            if sq <= n:
                p += 1
                m = result[p]
                sq = m*m
            for i in result[2:p]:
#                 n_iter += 1
#                 print('n = ', n, ', i = ', i)
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
#     if result[-1] > num:
#         result = result[:-1]
#     print('Total iterations: {}'.format(n_iter))
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_7_test(1000000))')


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_8(1000000))')

# %% [markdown]
# ### Removed number check, and only remove the last number when it is larger than the given number
# When num = 1M, the running time can be reduced slightly (lowest running time reduced from ~790ms to 780ms)

# %%
def pn_9(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
    sq = 9
    for q in range(7, num, 6):
        for n in [q, q+4]:
            primary = True
            if sq <= n:
                p += 1
                m = result[p]
                sq = m*m
            for i in result[2:p]:
                if n%i == 0:
                    primary = False
                    break
            if primary:
                result.append(n)
    if result[-1] > num:
        result.pop()
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_9(1000000))')


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_2(1000000))')


# %%
a = pn_9(100)


# %%
print(a)
a.pop()
print(a)


# %%
def pn_10(num = 1000):
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
    sq = 9
    f = 0
    for q in range(7, num, 3):
        n = q + f
#         for n in [q, q+4]:
        primary = True
        f = 1 - f
#         if f == 0:
#             f = 1
#         else:
#             f = 0
        if sq <= n:
            p += 1
            m = result[p]
            sq = m*m
        for i in result[2:p]:
            if n%i == 0:
                primary = False
                break
        if primary:
            result.append(n)
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_9(2000000))')


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_10(2000000))')


# %%
for i in range(7, 100, 6):
    for q in [i, i+4]:
        print(q, end = ',')


# %%
r = 0
for i in range(7, 100, 3):
    print(i+r, end = ',')
    r = 1 - r
    
#     2 4 8 14
#     1 7 11 13
#     1 -3 -3 1


# %%
a = ((2,4,8,14), (1, 7, 11, 13))
f = 1
rlt = []
for i in range(0, 95, 15):
    for b in a[f]:
        if i + b > 1:
            rlt.append(i + b)
    f = 1 - f 
while rlt[-1] > 95:
    rlt.pop()
print(rlt)
# 2, 3, 5, 7, 11, 13

# %% [markdown]
# ### pre-removed multiplier of 5, reduced iterations by ~1%
# When num = 1M, the running time can be reduced slightly (lowest running time reduced from ~780ms to 770ms)

# %%
def pn_11(num = 1000):
#     if type(num) is not int:
#         raise Exception('The number must be integer!')
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
    sq = 9
    f = 1
    seq = ((2, 4, 8, 14), (1, 7, 11, 13))
#     i_iter = 0
    for q in range(0, num, 15):
        for s in seq[f]:
            n = q + s
            if n != 1 and n < num:               
                primary = True
                if sq <= n:
                    p += 1
                    m = result[p]
                    sq = m*m
                for i in result[2:p]:
#                     i_iter += 1
#                     print('n = ', n, 'i = ', i)
                    if n%i == 0:
                        primary = False
                        break
                if primary:
                    result.append(n)
        f = 1 - f
    while result[-1] > num:
        result.pop()
#     print('Total iterations: ', i_iter)
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_11(100000))')


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_11(1000000))')


# %%
type(int(100.5)) is not int


# %%
int(100.5)

# %% [markdown]
# ### As all multipliers of 5 have been removed, no need to divide by 5, which reduced iterations down to 0.56M for 100K input

# %%
def pn_12(num = 1000):
#     if type(num) is not int:
#         raise Exception('The number must be integer!')
    if num < 2:
        return []
    elif num == 2:
        return [2]
    elif num < 5:
        return [2, 3]
    result = [2, 3, 5]
    p = 1
    m = 3
    sq = 9
    f = 1
    seq = ((2, 4, 8, 14), (1, 7, 11, 13))
#     i_iter = 0
    for q in range(0, num, 15):
        for s in seq[f]:
            n = q + s
            if n != 1 and n < num:               
                primary = True
                if sq <= n:
                    p += 1
                    m = result[p]
                    sq = m*m
                for i in result[3:p]:
#                     i_iter += 1
#                     print('n = ', n, 'i = ', i)
                    if n%i == 0:
                        primary = False
                        break
                if primary:
                    result.append(n)
        f = 1 - f
#     while result[-1] > num:
#         result.pop()
#     print('Total iterations: ', i_iter)
    return result


# %%
get_ipython().run_cell_magic('time', '', 'len(pn_12(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_3(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_4(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_5(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_6(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_7(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_8(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_9(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_10(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_11(1000000))')


# %%
get_ipython().run_cell_magic('timeit', '', 'len(pn_12(1000000))')


# %%
print(pn_12(316))


# %%
len(pn_12(316))


# %%
for i in range(95,98):
    print(len(pn_12(i)))

