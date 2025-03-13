import matplotlib.pyplot as plt  # Библиотека для построения графиков
from sklearn.metrics import roc_curve, auc  # Метрики для построения ROC-кривой и вычисления AUC
import pandas as pd  # Работа с таблицами данных (DataFrame)
import numpy as np  # Библиотека для работы с массивами и математическими операциями

# Функция для проверки наличия слова в заданном списке
def check_word_in_colocation(word, colocation):
    return 1 if word in colocation else 0  # Возвращает 1, если слово есть в списке colocation, иначе 0

# Функция для построения ROC-кривой на основе данных из файла t_stat.xlsx
def t_stat():
    # Загрузка данных из Excel-файла
    df = pd.read_excel('C:/Users/artem/Documents/Учёба/7 сем/санд/РГЗ/t_stat.xlsx', index_col=False)
    
    # Список целевых словосочетаний (предопределенные данные для проверки)
    colocation = ['sample', 'mean', 'kernel', 'test', 'scale', 'decision','gaussian']
    
    # Получение предсказанных значений для t_stat
    y_score_t_stat = df['t_stat'].values
    
    # Формирование истинных меток (1, если слово из 'word2' есть в colocation, иначе 0)
    y_true_t_stat = df['word2'].apply(lambda word: check_word_in_colocation(word, colocation))
    print('y_score_t_stat', y_score_t_stat)
    print('y_true_t_stat', y_true_t_stat)
    # Вычисление значений FPR (false positive rate) и TPR (true positive rate) для построения ROC-кривой
    fpr_t_stat, tpr_t_stat, trsh = roc_curve(y_true_t_stat, y_score_t_stat)
    print('Пороги t_stat', trsh)
    # Вычисление площади под кривой (AUC)
    roc_auc_t_stat = auc(fpr_t_stat, tpr_t_stat)
    
    # Построение ROC-кривой
    plt.figure()
    plt.plot(fpr_t_stat, tpr_t_stat, color='darkorange', lw=2, 
             label=f'ROC curve (area = {roc_auc_t_stat:.2f}) for t_stat')  # Основная линия ROC-кривой
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Линия случайного классификатора
    plt.xlim([0.0, 1.0])  # Установка диапазона значений по оси X
    plt.ylim([0.0, 1.05])  # Установка диапазона значений по оси Y
    plt.xlabel('False Positive Rate')  # Подпись оси X
    plt.ylabel('True Positive Rate')  # Подпись оси Y
    plt.title('Receiver Operating Characteristic')  # Заголовок графика
    plt.legend(loc="lower right")  # Легенда графика
    plt.show()  # Отображение графика

# Функция для построения ROC-кривой на основе данных из файла mi.xlsx
def mi():
    # Загрузка данных из Excel-файла
    df = pd.read_excel('C:/Users/artem/Documents/Учёба/7 сем/санд/РГЗ/mi.xlsx', index_col=False)
    
    # Список целевых словосочетаний
    colocation = ['sample', 'mean', 'kernel', 'test', 'scale', 'decision','gaussian']
    
    # Получение предсказанных значений для MI
    y_score_mi = df['MI'].values
    
    # Формирование истинных меток
    y_true_mi = df['word2'].apply(lambda word: check_word_in_colocation(word, colocation))
    
    # Вычисление FPR, TPR и порогов вероятностей
    fpr_mi, tpr_mi, trsh = roc_curve(y_true_mi, y_score_mi)
    print('Пороги mi',trsh)  # Печать порогов вероятностей для анализа (вспомогательный вывод)
    
    # Вычисление площади под ROC-кривой (AUC)
    roc_auc_mi = auc(fpr_mi, tpr_mi)
    
    # Построение ROC-кривой
    plt.figure()
    plt.plot(fpr_mi, tpr_mi, color='darkorange', lw=2, 
             label=f'ROC curve (area = {roc_auc_mi:.2f}) for mi')  # Основная линия ROC-кривой
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Линия случайного классификатора
    plt.xlim([0.0, 1.0])  # Установка диапазона значений по оси X
    plt.ylim([0.0, 1.05])  # Установка диапазона значений по оси Y
    plt.xlabel('False Positive Rate')  # Подпись оси X
    plt.ylabel('True Positive Rate')  # Подпись оси Y
    plt.title('Receiver Operating Characteristic')  # Заголовок графика
    plt.legend(loc="lower right")  # Легенда графика
    plt.show()  # Отображение графика

# Функция для построения ROC-кривой на основе данных из файла pmi.xlsx
def pmi():
    # Загрузка данных из Excel-файла
    df = pd.read_excel('C:/Users/artem/Documents/Учёба/7 сем/санд/РГЗ/pmi.xlsx', index_col=False)
    
    # Список целевых словосочетаний
    colocation = ['sample', 'mean', 'kernel', 'test', 'scale', 'decision','gaussian']
    
    # Получение предсказанных значений для PMI
    y_score_mi = df['PMI'].values
    
    # Формирование истинных меток
    y_true_mi = df['word2'].apply(lambda word: check_word_in_colocation(word, colocation))
    
    # Вычисление FPR и TPR для построения ROC-кривой
    fpr_mi, tpr_mi, trsh = roc_curve(y_true_mi, y_score_mi)
    print('Пороги mi',trsh)
    # Вычисление площади под ROC-кривой (AUC)
    roc_auc_mi = auc(fpr_mi, tpr_mi)
    
    # Построение ROC-кривой
    plt.figure()
    plt.plot(fpr_mi, tpr_mi, color='darkorange', lw=2, 
             label=f'ROC curve (area = {roc_auc_mi:.2f}) for Pmi')  # Основная линия ROC-кривой
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Линия случайного классификатора
    plt.xlim([0.0, 1.0])  # Установка диапазона значений по оси X
    plt.ylim([0.0, 1.05])  # Установка диапазона значений по оси Y
    plt.xlabel('False Positive Rate')  # Подпись оси X
    plt.ylabel('True Positive Rate')  # Подпись оси Y
    plt.title('Receiver Operating Characteristic')  # Заголовок графика
    plt.legend(loc="lower right")  # Легенда графика
    plt.show()  # Отображение графика

# Вызов функций для построения ROC-кривых для трех наборов данных
t_stat()  # Построение ROC-кривой для t_stat
mi()  # Построение ROC-кривой для mi
pmi()  # Построение ROC-кривой для pmi
