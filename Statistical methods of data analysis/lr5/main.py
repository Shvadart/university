import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil 

def make_X(x_array: np.array):
    return np.array([[x_array[0][i], 
                      x_array[1][i],
                      x_array[2][i],
                      x_array[3][i],
                      x_array[4][i],
                      x_array[5][i],
                      x_array[6][i],
                      
                      1,] for i in range(len(x_array[0]))])
theta = np.array([1, 1, 1, 1, 1, 1, 1, 1])
def u_calc(x1, x2, x3, x4, x5, x6, x7):
    return theta[0] * x1  + theta[1] * x2 + theta[2] * x3 + theta[3] * x4 + theta[4] * x5 + theta[5] * x6 + theta[6] * x7 + theta[7]

def make_experiments(n: int):
    
    x1 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    x2 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    x3 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    x4 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    x5 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    x6 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    x7 = np.linspace(-1.0, 1.0, ceil(n**(1/8)))
    
    
    #np.random.seed(123)
    
    u = np.array([])
    x1_array = np.array([])
    x2_array = np.array([])
    x3_array = np.array([])
    x4_array = np.array([])
    x5_array = np.array([])
    x6_array = np.array([])
    x7_array = np.array([])
    
    error_array = np.array([])
    y_array = np.array([])
    
    for i1 in x1:
        for i2 in x2:
            for i3 in x3:
                for i4 in x4:
                    for i5 in x5:
                        for i6 in x6:                 
                                    
                            i7 = i4 +2*i5 -i6 + np.random.normal(0, 0.1)
                        
                            
                            x1_array = np.append(x1_array, i1)
                            x2_array = np.append(x2_array, i2)
                            x3_array = np.append(x3_array, i3)
                            x4_array = np.append(x4_array, i4)
                            x5_array = np.append(x5_array, i5)
                            x6_array = np.append(x6_array, i6)
                            x7_array = np.append(x7_array, i7)
                        
                                    
                            u = np.append(u, u_calc(i1, i2, i3, i4, i5, i6, i7))
            
    u_avg = np.average(u)
    omega = (u - u_avg).T @ (u - u_avg) / len(u)

    for i in range(len(u)):
        error = np.random.normal(0.0, np.sqrt(0.6*omega))
        error_array = np.append(error_array, error)
        y_array = np.append(y_array, u[i] + error)
        
    df =  pd.DataFrame({'x1': x1_array, 'x2': x2_array, 'x3': x3_array, 'x4': x4_array, 'x5': x5_array, 'x6': x6_array, 'x7': x7_array, 'u': u, 'e': error_array, 'y': y_array})
    df.to_csv('data.csv', index=False) 
    
    return df

#Класс регрессии по МНК
class OLS():
    def __init__(self):
        self.theta_array = np.array([])
        self.X = np.array([])
        self.Y = np.array([])
        
    def fit(self, X: np.array, Y: np.array):
        self.X = X
        self.Y = Y
        self.theta_array = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.Y
        
    def predict(self, X: np.array):
        return X @ self.theta_array

#Класс ридж-регрессии
class Ridge():
    def __init__(self, alpha: np.float64 = 1):
        self.alpha = alpha
        self.theta_array = np.array([])
        self.X = np.array([])
        self.Y = np.array([])
        
    def fit(self, X: np.array, Y: np.array):
        self.X = X
        self.Y = Y
        self.Lambda = np.diag(np.diag(self.X.T @ self.X)) * self.alpha
        self.theta_array = np.linalg.inv(self.X.T @ self.X + self.Lambda) @ self.X.T @ self.Y
        
    def predict(self, X: np.array):
        return X @ self.theta_array
    
    def norm(self):
        return np.linalg.norm(self.theta_array)
         
    def RSS(self):
        return np.sum((self.X @ self.theta_array - self.Y)**2)

##Класс тестов мультиколлинеарности
class MulticollinearityTest():
    def __init__(self, X: np.array):
        self.X = X
        
    def Det(self):
        return np.linalg.det(self.X.T @ self.X/np.trace(self.X.T @ self.X))
    
    def MinW(self):
        return np.min(np.linalg.eig(self.X.T @ self.X)[0])
    
    def Neumann_Goldstein(self):
        return np.max(np.linalg.eig(self.X.T @ self.X)[0])/self.MinW()
    
    def MaxPairConjugacy(self):
        x_t = self.X.T
        max_k = 0
        max_comb = (0, 0)
        
        for i in range(len(x_t)):
            for j in range(i + 1, len(x_t)):
                
                k = np.dot(x_t[i], x_t[j]) / (np.linalg.norm(x_t[i]) * np.linalg.norm(x_t[j]))
                if k > max_k:
                    max_k = k
                    max_comb = (i, j)
                    
        return (max_k, max_comb)
    
    def MaxConjugacy(self):
        x_t = self.X.T
        R = np.zeros((9, 9))
        
        for i in range(len(x_t)):
            for j in range(i + 1, len(x_t)):
                if i != j:
                    k = np.dot(x_t[i], x_t[j]) / (np.linalg.norm(x_t[i]) * np.linalg.norm(x_t[j]))
                    R[i, j] = k
                    R[j, i] = k
        
        return np.max(R)

#Класс метода главных компонент
class PCA:
    def __init__(self, n_components=None):
        self.n_components = n_components
    
    def fit_transform(self, X):
        n_samples, n_features = X.shape
        
        if self.n_components is None:
            self.n_components = min(n_samples, n_features)
            
        X_centered = X - X.mean(axis=0)
        self.U, self.V = np.linalg.eig(X_centered.T @ X_centered)
        
        self.explained_variance = (self.U[:self.n_components] ** 2) / (n_samples - 1)
        self.explained_variance_ratio = self.explained_variance / np.sum(self.explained_variance)

        return X_centered[:, : self.n_components] @ self.V.T[:self.n_components, : self.n_components]

df = make_experiments(10)
print(df)
#получение необходимых оценок
alpha = 0.01

# 1. Вычисляем X и Y перед использованием в ridge.fit()
X = make_X(np.array([np.array(df['x1']), np.array(df['x2']), np.array(df['x3']), np.array(df['x4']), np.array(df['x5']), np.array(df['x6']), np.array(df['x7'])]))
Y = np.array(df['y'])

ridge = Ridge(alpha)
ridge.fit(X, Y)

print(f'alpha = {alpha}')
print(f'Оценка параметров ридж-регрессией: \n{ridge.theta_array.round(4)}\n')
print(f'Норма параметров: {ridge.norm().round(4)}')
print(f'RSS Ridge: {ridge.RSS().round(4)}')

pca = PCA(8)
Xt = pca.fit_transform(X)
print(f'Значимость признаков МГК:\n{pca.explained_variance_ratio.round(5)}')

#обрезаем последний 0, что бы матрица X^T*X была вырожденной
pca.n_components = 7
Xt = pca.fit_transform(X)
Yt = Y - np.mean(Y)

ols = OLS()
ols.fit(Xt, Yt)
print(f'Оценка параметров МГК:\n{ols.theta_array.round(5)}\n')
est_theta = pca.V.T[:pca.n_components, : pca.n_components] @ ols.theta_array
print(f'Оценка параметров МГК в исходном пр ве:\n{(est_theta).round(5)}')

print(f'Расстояние до истинных значений параметров МГК: {np.linalg.norm(theta[:pca.n_components] - est_theta).round(5)}')
print(f'RSS МГК: {(((Y - X[:, :pca.n_components]@est_theta.T).T)@(Y - X[:, :pca.n_components]@est_theta.T)).round(5)}')

print(f'Расстояние до истинных значений параметров Ridge: {np.linalg.norm(theta - ridge.theta_array).round(5)}')
print(f'RSS Ridge: {ridge.RSS().round(4)}')

#Тесты коллинеарности
X = make_X(np.array([np.array(df['x1']), np.array(df['x2']), np.array(df['x3']), np.array(df['x4']), np.array(df['x5']), np.array(df['x6']), np.array(df['x7'])]))
Test = MulticollinearityTest(X)

print(f'Определитель X^T*X: {Test.Det()}')
print(f'Минимальное собственное число: {Test.MinW().round(3)}')
print(f'Тест Неймана-Голдстейна: {Test.Neumann_Goldstein().round(3)}')
print(f'Максимальная парная сопряженность: значение - {Test.MaxPairConjugacy()[0].round(3)}, пара факторов - {Test.MaxPairConjugacy()[1]}')
print(f'Максимальная сопряженность: {Test.MaxConjugacy().round(3)}')

#Формирования графиков зависимости нормы параметров и квадратов остатков от параметра регуляризации

norm_1, rss_1, norm_2, rss_2  = [], [], [], []

alpha = np.linspace(0.00001, 0.1, 200)
for i in alpha:

    X = make_X(np.array([np.array(df['x1']), np.array(df['x2']), np.array(df['x3']), np.array(df['x4']), np.array(df['x5']), np.array(df['x6']), np.array(df['x7'])]))
    Y = np.array(df['y'])
    
    rols = Ridge(i)
    rols.fit(X, Y)
    
    norm_1.append(rols.norm().round(5)**2)
    rss_1.append(rols.RSS().round(5))
    
   
plt.plot(alpha, norm_1, color='b', label='castom-ridge')
plt.xlabel(r'alpha', fontsize=16)
plt.ylabel(r'norm', fontsize=16)
plt.legend(fontsize=14)
plt.show()

plt.plot(alpha, rss_1, color='g', label='castom-ridge')
plt.xlabel(r'alpha', fontsize=16)
plt.ylabel(r'RSS', fontsize=16)
plt.legend(fontsize=14)
plt.show()
