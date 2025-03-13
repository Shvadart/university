import numpy as np
import pandas as pd
import scipy.stats as scs
import itertools
import math

file_name = 'C:/V2.csv'
feature = 'A16'
positive_feature = 1
negative_feature = 2
qualitative = np.array(['A1', 'A4', 'A9', 'A12', 'A13'])
numerical = np.array(['A2', 'A3', 'A8', 'A14'])
all_col = np.concatenate((qualitative, numerical, np.array([feature])))
all_col = all_col[np.argsort([int(i[1:]) for i in all_col])]

n = all_col.size
quantiles_levels = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])

def printIntervals(quantiles) :
    if (quantiles.size == 2) :
        if (math.isinf(quantiles[-1])) :
            print('[{}; {}], ({}; {})'.format(quantiles[0], quantiles[0], quantiles[0], quantiles[1]))
        else :
            print('[{}; {}], ({}; {}]'.format(quantiles[0], quantiles[0], quantiles[0], quantiles[1]))
        return
    for i in range(quantiles.size - 1) :
        if (i == 0) :
            print('[', end='')
        else : 
            print('(', end='')
        print(round(quantiles[i], 4), '; ', round(quantiles[i + 1], 4), ']', 
              end='', sep='')
        if (i < quantiles.size - 2) :
            print(', ', end='')
        else :
            print()

def getQuantiles(arr, lev) :
    quantiles = np.array([np.quantile(arr, lv) for lv in lev])
    quantiles_unique = {}
    for q in (quantiles) :
        freq = sum(arr <= q)
        quantiles_unique[freq] = q

    res = np.array([quantiles_unique[key] for key in quantiles_unique])
    if res.size > 1 :
        return res
    else :
        return np.concatenate(res, np.array([res[0], float('inf')]))

def getInterval(x, quantiles) :
    if quantiles.size == 2 :
        if x == quantiles[0] :
            return 0
        else :
            return 1
    for i in range(1, quantiles.size) :
        if x <= quantiles[i] :
            return i - 1

class TestResults :
    stat = 0.0
    pvalue = 0.0
    def __init__(self, stat_, pvalue_) :
        self.stat = stat_
        self.pvalue = pvalue_

def significanceTest(r, n) :
    t = (np.abs(r) / np.sqrt(1 - r**2)) * np.sqrt(n - 2)
    return TestResults(t, scs.t(n - 2).sf(t) * 2)

def permutCriteria(x, y, M, alpha=0.05) :
    t = significanceTest(np.corrcoef(x, y)[1][0], x.size).stat
    t_r = np.array([significanceTest(np.corrcoef(np.random.permutation(x), y)[0][1], x.size).stat
                     for _ in range(M)])
    t_r.sort()
    ind = np.searchsorted(t_r, t)
    stat = np.quantile(t_r, 1 - alpha)
    if ind == t_r.size :
        return TestResults(stat, 0)
    pvalue = (t_r.size - ind) / t_r.size
    return TestResults(stat, pvalue)
   

df1 = pd.read_csv(file_name, sep=';', decimal=',')

N = len(df1.index)

for i in df1.index :
    df1.at[i, feature] = 1 if df1[feature][i] == positive_feature else 0

positive = sum(df1[feature] == 1)
negative = sum(df1[feature] == 0)
apriori_chance = positive / negative
posneg = positive + negative

for c in qualitative :
    dict = {}
    for ind in df1.index :
            if df1[c][ind] not in dict :
                dict[df1[c][ind]] = 0

    cross_tab = pd.crosstab(df1[feature], df1[c])

    for key in dict:
    # Check if key exists in the cross-tab for both categories (0 and 1)
        if key in cross_tab.index:
            pos = cross_tab.at[1, key] if 1 in cross_tab.index else 0  # Safely access index 1
            neg = cross_tab.at[0, key] if 0 in cross_tab.index else 0  # Safely access index 0
            dict[key] = (pos + 1) / (pos + 1 + apriori_chance * (neg + 1))
        else:
            dict[key] = 0
    for j in df1.index :
        df1.at[j, c] = dict[df1[c][j]]
    print({k:round(v, 4) for k, v in dict.items()})

df1.to_csv('df1.csv', sep=';')
df2 = df1.copy()

for c in numerical :
    intervals = getQuantiles(df1[c], quantiles_levels)
    print(c, ': ', end='')
    printIntervals(intervals)
    for i in df2.index :
        df2.at[i, c] = getInterval(df2[c][i], intervals)

df2.to_csv("df2.csv", sep=';')

pearson_coef = np.zeros((n, n))
signif_stat = np.zeros((n, n))
signif_pvalue = np.zeros((n, n))
signif_permut_pvalue = np.zeros((n, n))
signif_permut_quantiles = np.zeros((n, n))

for i, j in itertools.product(range(n), range(n)) :
    df1[all_col[i]] = df1[all_col[i]].astype(float)
    df1[all_col[j]] = df1[all_col[j]].astype(float)
    pearson_coef[i][j] = pearson_coef[j][i] = np.corrcoef(df1[all_col[i]], df1[all_col[j]])[0][1]
    t = significanceTest(pearson_coef[i][j], N)
    signif_stat[i][j] = signif_stat[j][i] = t.stat
    signif_pvalue[i][j] = signif_pvalue[j][i] = t.pvalue
    res_permut = permutCriteria(df1[all_col[i]], df1[all_col[j]], 100)
    signif_permut_pvalue[i][j] = signif_permut_pvalue[j][i] = res_permut.pvalue
    signif_permut_quantiles[i][j] = signif_permut_quantiles[j][i] = res_permut.stat

df_pearson_coef = pd.DataFrame()
df_signif_stat = pd.DataFrame()
df_signif_pvalue = pd.DataFrame()
df_signif_permut_pvalue = pd.DataFrame()
df_signif_permut_quantiles = pd.DataFrame()

for i in range(n) :
    df_pearson_coef[all_col[i]] = pearson_coef[i]

for i in range(n) :
    df_signif_stat[all_col[i]] = signif_stat[i]

for i in range(n) :
    df_signif_pvalue[all_col[i]] = signif_pvalue[i]

for i in range(n) :
    df_signif_permut_pvalue[all_col[i]] = signif_permut_pvalue[i]

for i in range(n) :
    df_signif_permut_quantiles[all_col[i]] = signif_permut_quantiles[i]

df_pearson_coef.index = all_col.tolist()
df_signif_stat.index = all_col.tolist()
df_signif_pvalue.index = all_col.tolist()
df_signif_permut_pvalue.index = all_col.tolist()
df_signif_permut_quantiles.index = all_col.tolist()

df_pearson_coef.to_csv('pearson_coef.csv', sep=';')
df_signif_stat.to_csv('signif_stat.csv', sep=';')
df_signif_pvalue.to_csv('signif_pvalue.csv', sep=';')
df_signif_permut_pvalue.to_csv('signif_permut_pvalue.csv', sep=';')
df_signif_permut_quantiles.to_csv('signif_permut_quantiles.csv', sep=';')