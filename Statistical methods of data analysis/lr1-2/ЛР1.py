import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import dataframe_image as dfi


matplotlib.use('TkAgg')
# Параметры модели
theta = [1.0, 0.01, 1.0, 0.01, 1.0]
# Значения факторов
vector_x1 = vector_x2 = [-1.0, -0.5, 0.0, 0.5, 1.0]
# Доля дисперсии от мощности сигнала
deviation_part = 0.05


# Расчёт u
def u(x1, x2):
    return theta[0] * (x1 ** 2) + theta[1] * x1 + theta[2] * (x2 ** 3) + theta[3] * (x2 ** 2) + theta[4] * x1 * x2 


# Построение матрицы истинных значений
def calculate_matrix():
    df = pd.DataFrame(columns=["x1", "x2", "u"])
    for x1 in vector_x1:
        for x2 in vector_x2:
            df.loc[len(df.index)] = [x1, x2, u(x1, x2)]
    return df


# Расчёт мощности сигнала
def signal_power(array):
    average = np.average(array)
    return (np.matmul(np.transpose(array.flatten() - average), array.flatten() - average)) / (array.size - 1)


# Добавление ошибки к матрице
def add_error(df):
    deviation = np.sqrt(deviation_part * signal_power(df["u"].to_numpy()))
    for i in range(len(df.index)):
        error = np.random.normal(0.0, deviation)
        df.loc[i, "e"] = error
        df.loc[i, "y"] = df.loc[i, "u"] + error


# Построение и сохранение графика
def plot_data(df):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('u')
    ax.invert_xaxis()
    ax.plot_trisurf(df.x1, df.x2, df.u, linewidth=1, antialiased=False, alpha=0.8)
    plt.savefig("c:/Users/artem/Documents/Учёба/7 сем/СМАд/plot.png")


if __name__ == '__main__':
    data = calculate_matrix()
    plot_data(data)
    add_error(data)
    data = data.round(2)
    data.to_csv("c:/Users/artem/Documents/Учёба/7 сем/СМАд/data.csv", index=False)
    dfi.export(data, "c:/Users/artem/Documents/Учёба/7 сем/СМАд/table.png")
    

