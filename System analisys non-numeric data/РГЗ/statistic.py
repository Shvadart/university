import re
import pandas as pd
import math
from scipy.stats import t
import numpy as np
N=123645.0
total_train_word = 108.0
file_path = 'text_sent_2.txt'

df = pd.read_excel('result.xlsx',index_col=False)
with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

def get_total_word_count(target_word):
    target_word_count = 0
    sentences = re.split(r'\n+', text)  # предполагается, что предложения уже разделены по строкам
    for sentence in sentences:
       words = sentence.split()
       for i in range(0,len(words)):
            if words[i] == target_word :
                target_word_count += 1  
    return target_word_count           

word1_arr=df['word1'].values
word2_arr=df['word2'].values
o11_array=df['o11'].values

t_crit = t.ppf(1 - 0.001, N - 1)
print("Критическое значение для t-test при alfa = 0.001: ", t_crit)

def t_student():
    result=[]
    soglasie=[]
    for i in range(0,len(word1_arr)):
         x=o11_array[i]/N
         nu=(total_train_word*get_total_word_count(word2_arr[i]))/(N*N)
         s_square=x*(1-x)
         result.append(
              (x-nu)/(math.sqrt(s_square/N))
         )
         if (x-nu)/(math.sqrt(s_square/N)) > t_crit:
              soglasie.append('Отвергается')
         else:
              soglasie.append('Не отвергается')
    return result,soglasie


 

df['t_stat'], df['t_stat_soglasie']= t_student() 

print(df.sort_values(by='t_stat', ascending=False))
df.sort_values(by='t_stat', ascending=False).to_excel('t_stat.xlsx',index=False)

def calculate_mi(row, N):
  mi_total = 0
  O_11 = row['o11']
  O_12 = row['o12']
  O_21 = row['o21']
  O_22 = row['o22']
  O_1_sum = O_11 + O_12  
  O_2_sum = O_21 + O_22  
  O_sum_1 = O_11 + O_21  
  O_sum_2 = O_12 + O_22  

  O_ij_list = [(O_11, O_1_sum, O_sum_1),
               (O_12, O_1_sum, O_sum_2),
               (O_21, O_2_sum, O_sum_1),
               (O_22, O_2_sum, O_sum_2)]

  for O_ij, O_i_sum, O_j_sum in O_ij_list:
    if O_ij > 0:
      mi_total += (O_ij / N) * np.log2((N * O_ij) / (O_i_sum * O_j_sum))
  return mi_total


def calculate_pmi():
    result = []
    for i in range(0,len(word1_arr)):
        result.append(np.log2((o11_array[i] * N) / (108.0 * get_total_word_count(word2_arr[i]))))
    return result



def save_to_excel(dataframe, filename, column):
    dataframe.sort_values(by=column, ascending=False).to_excel(filename, index=False)

# Расчёт t-статистики
print("Выполняется расчет t-статистики...")
df['t_stat'], df['t_stat_soglasie'] = t_student()
save_to_excel(df[['word1', 'word2', 't_stat', 't_stat_soglasie']], 't_stat.xlsx', 't_stat')

# Расчёт MI
print("Выполняется расчет MI...")
df['MI'] = df.apply(lambda row: calculate_mi(row, N), axis=1)
save_to_excel(df[['word1', 'word2', 'MI']], 'mi.xlsx', 'MI')

# Расчёт PMI
print("Выполняется расчет PMI...")
df['PMI'] = calculate_pmi()
save_to_excel(df[['word1', 'word2', 'PMI']], 'pmi.xlsx', 'PMI')

print("Расчёты завершены. Файлы сохранены.")
