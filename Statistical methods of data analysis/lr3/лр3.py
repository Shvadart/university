import numpy as np
import pandas as pd
import scipy.stats as sp
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

significance = 0.05
alpha = 0.1

if __name__ == '__main__':
    # Считывание данных
    data = pd.read_csv("c:/Users/artem/Documents/Учёба/7 сем/СМАд/data.csv")
    # Формируем матрицу X по модели с дополнительным регрессором x1**3.
    X = np.array([[data.loc[i, "x1"] ** 2,
                   data.loc[i, "x1"],
                   data.loc[i, "x2"] ** 3,
                   data.loc[i, "x2"] ** 2,
                   data.loc[i, "x1"] * data.loc[i, "x2"],
                   data.loc[i, "x1"] ** 3
                   ]
                 for i in data.index])
    # Производим оценку параметров
    theta_vector = np.linalg.inv(X.T @ X) @ X.T @ data["y"].to_numpy()
    print("Вектор точечных оценок параметров: ", theta_vector.round(2))
    data["y^"] = (X @ theta_vector).tolist()
    # Построение доверительных интервалов для каждого параметра
    temp = np.linalg.inv(X.T @ X)
    print("Доверительные интервалы с уровнем доверия {:.2f}".format(1-alpha))
    for j in range(len(theta_vector)):
        theta_dev = abs(np.sqrt(temp[j][j]) * sp.t.ppf(alpha/2, len(X)-len(theta_vector)))
        print("θ{:d}:\t{:.2f}\t~\t{:.2f}".format(j+1, theta_vector[j]-theta_dev, theta_vector[j]+theta_dev))
    # Производим оценку ошибок
    error_est = data["y"].to_numpy() - X @ theta_vector
    data["y-y^"] = error_est.tolist()
    # Производим оценку дисперсии
    dispersion_est = (error_est.T @ error_est) / (len(X)-len(theta_vector))
    # Проверка о незначимости параметров
    print("Проверка гипотезы о незначимости параметров с уровнем значимости {:.2f}".format(significance))
    F_critical = sp.f.isf(significance, 1, len(X) - len(theta_vector))
    print("Критическое значение: {:.2f}".format(F_critical))
    for j in range(len(theta_vector)):
        F = (theta_vector[j]**2/(dispersion_est * temp[j][j]))
        if F < F_critical:
            print("θ{:d}: F = {:.2f} < {:.2f} \t=> Параметр незначим".format(j + 1, F, F_critical))
        else:
            print("θ{:d}: F = {:.2f} > {:.2f} \t=> Параметр значим".format(j + 1, F, F_critical))
    del temp
    # Проверка о незначимости регрессии
    print("Проверка гипотезы о незначимости регрессии с уровнем значимости {:.2f}".format(significance))
    F_critical = sp.f.isf(significance, len(theta_vector)-1, len(X) - len(theta_vector))
    RSSh = sum((y - data["y"].mean())**2 for y in data["y"].tolist())
    RSS = (data["y"].to_numpy() - X @ theta_vector).T @ (data["y"].to_numpy() - X @ theta_vector)
    F = ((RSSh-RSS) / (len(theta_vector)-1)) / (RSS / (len(X) - len(theta_vector)))
    if F < F_critical:
        print("F = {:.2f} < {:.2f} \t=> Регрессия незначима".format(F, F_critical))
    else:
        print("F = {:.2f} > {:.2f} \t=> Регрессия значима".format(F, F_critical))
    # Прогнозные значения
    # Фиксируя x2
    print("Прогноз математического ожидания с фиксированным x2 и уровнем доверия {:.2f}".format(1 - alpha))
    x1_values = [-1+2*(j)/10 for j in range(11)]
    x2_values = np.ones(len(x1_values))
    def predict(x1_values, x2_values):
        f_array = np.array([[x1_values[j] ** 2,
                           x1_values[j],
                           x2_values[j]**3,
                           x2_values[j]**2,
                           1,
                           x1_values[j]*x2_values[j]] for j in range(len(x1_values))])
        y = np.array([f_x.T @ theta_vector for f_x in f_array])
        dev = np.array([abs(sp.t.ppf(alpha/2, len(X)-len(theta_vector)) *
                        np.sqrt(dispersion_est)*np.sqrt(f_x.T @ np.linalg.inv(X.T @ X) @ f_x)) for f_x in f_array])
        return pd.DataFrame({
            "x1": x1_values,
            "x2": x2_values,
            "left": y-dev,
            "right": y+dev
        })
    prediction = predict(x1_values, x2_values)
    print(prediction.round(2))
    def plot_prediction(prediction, column, file_name):
        plt.plot(prediction[column], prediction["left"], "-.")
        plt.plot(prediction[column], prediction["right"], "-.")
        plt.xlabel(column)
        plt.ylabel("y")
        plt.savefig(file_name, bbox_inches='tight')
        plt.show()
    plot_prediction(prediction, "x1", "c:/Users/artem/Documents/Учёба/7 сем/СМАд/x1_plot.png")
    # Фиксируя x1
    print("Прогноз математического ожидания с фиксированным x1 и уровнем доверия {:.2f}".format(1 - alpha))
    x2_values = [-1+2*(j)/10 for j in range(11)]
    x1_values = np.ones(len(x2_values))
    prediction = predict(x1_values, x2_values)
    print(prediction.round(2))
    plot_prediction(prediction, "x2", "c:/Users/artem/Documents/Учёба/7 сем/СМАд/x2_plot.png")