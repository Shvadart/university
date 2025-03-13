import pandas as pd
import numpy as np
import random
import scipy.stats
from matplotlib import pyplot as plt
from scipy.linalg import toeplitz
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.decomposition import PCA
np.set_printoptions(suppress=True)
random.seed(42)

n = 3000
x1j, x2j, x3j, yj, sigma_vector = [], [], [], [], []
theta = [1, 1, 1, 1, 0.01, 0.01, 0.01, 1, 1, 1]

def u(x1,x2,x3):
    return theta[0] + theta[1]*x1 + theta[2]*x2 + theta[3]*x3 +theta[4]*x1**2 + theta[5]*x2**2 + theta[6]*x3**2 + theta[7]*x1*x2 + theta[8]*x1*x3 + theta[9]*x2*x3



for i in range(n):
    x1, x2, x3 = random.uniform(-1, 1), random.uniform(-1, 1),random.uniform(-1, 1)
    sigma2 = 0.1*x1**2+0.3*x2**2
    e = np.random.normal(0, sigma2)
    y = u(x1,x2,x3) + e
    x1j.append(x1), x2j.append(x2), x3j.append(x3), yj.append(y), sigma_vector.append(sigma2)
fig = plt.figure(figsize=(20,10))

plt.scatter(x1j, yj, alpha=0.8, label='x1')
plt.scatter(x2j, yj, alpha=0.8, label='x2')
plt.scatter(x3j, yj, alpha=0.3, label='x3')
plt.legend(loc='upper left', frameon=False, prop={'size': 20})
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

X = np.array([np.ones(n),
np.reshape(x1j, (n, )),
np.reshape(x2j, (n, )),
np.reshape(x3j, (n, )),
pow(np.reshape(x1j, (n, )), 2),
pow(np.reshape(x2j, (n, )), 2),
pow(np.reshape(x3j, (n, )), 2),
np.array(x1j)*np.array(x2j),
np.array(x1j)*np.array(x3j),
np.array(x2j)*np.array(x3j)]).T
y = np.reshape(yj, (n, ))
et = y - np.dot(X, theta)
sigma2_new = sum(pow(et, 2)/n)
print('sigma2_new =', sigma2_new)

V = sigma2_new ** toeplitz(np.arange(n))
theta_ls = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, y))
theta_gls = np.dot(np.linalg.inv(np.dot(np.dot(X.T, np.linalg.inv(V)),X)), np.dot(np.dot(X.T, np.linalg.inv(V)), y))
print('theta_ls =', np.around(theta_ls, 4))
print('theta_gls =', np.around(theta_gls, 4))

R_ls = np.dot((theta - theta_ls).T, (theta - theta_ls))
R_gls = np.dot((theta - theta_gls).T, (theta - theta_gls))
print('R_ls =', R_ls)
print('R_gls =', R_gls)
Zt = np.array([np.ones(n), 0.5*(1-abs(np.array(x1j)*np.array(x2j)))]).T
ct = pow(et, 2)/sigma2_new
alpha = np.dot(np.linalg.inv(np.dot(Zt.T, Zt)), np.dot(Zt.T, ct))
c_new = np.dot(Zt, alpha)
ess_div_2 = sum((c_new - np.mean(ct))**2)
FT = scipy.stats.f.ppf(q=1-0.05, dfn=1, dfd=n)
print('F =', ess_div_2)
print('FT =', FT)
zipped_lists = zip(yj, x1j, x2j, x3j)
sorted_pairs = sorted(zip(yj, x1j, x2j, x3j, sigma_vector), key=lambda x: x[4])
tuples = zip(*sorted_pairs)
yj, x1j, x2j, x3j, sigma_vector= [ list(tuple) for tuple in tuples]
X = np.array([np.ones(n)[:1000],
np.reshape(x1j, (n, ))[:1000],
np.reshape(x2j, (n, ))[:1000],
np.reshape(x3j, (n, ))[:1000],
pow(np.reshape(x1j, (n, )), 2)[:1000],
pow(np.reshape(x2j, (n, )), 2)[:1000],
pow(np.reshape(x3j, (n, )), 2)[:1000],
np.array(x1j)[:1000]*np.array(x2j)[:1000],
np.array(x1j)[:1000]*np.array(x3j)[:1000],
np.array(x2j)[:1000]*np.array(x3j)[:1000]]).T
y = np.reshape(yj, (n, ))[:1000]
theta = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, y))
y_hat = np.dot(X, theta)
RSS1 = sum((y - y_hat)**2)
zipped_lists = zip(yj, x1j, x2j, x3j)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
yj, x1j, x2j, x3j = [ list(tuple) for tuple in tuples]
X = np.array([np.ones(n)[2000:],
np.reshape(x1j, (n, ))[2000:],
np.reshape(x2j, (n, ))[2000:],
np.reshape(x3j, (n, ))[2000:],
pow(np.reshape(x1j, (n, )), 2)[2000:],
pow(np.reshape(x2j, (n, )), 2)[2000:],
pow(np.reshape(x3j, (n, )), 2)[2000:],
np.array(x1j)[2000:]*np.array(x2j)[2000:],
np.array(x1j)[2000:]*np.array(x3j)[2000:],
np.array(x2j)[2000:]*np.array(x3j)[2000:]]).T
y = np.reshape(yj, (n, ))[2000:]
theta = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, y))
y_hat = np.dot(X, theta)
RSS2 = sum((y - y_hat)**2)
FT = scipy.stats.f.ppf(q=1-0.05, dfn=991, dfd=991)
print('F =', RSS2 / RSS1)
print('FT =', FT)
