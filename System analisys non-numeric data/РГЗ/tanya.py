# import pandas as pd
# import numpy as np
# import scipy.stats as stats

# with open('text_sent_2.txt', 'r', encoding='utf-8') as file:
#     text = file.read().splitlines()

# word_combinations = []
# for sentence in text:
#     words = sentence.split()  
#     if len(words) > 1:  
#         for i in range(len(words) - 1):
#             word_combinations.append((words[i], words[i + 1])) 
# df = pd.DataFrame(word_combinations, columns=['first_word', 'second_word'])

# df = df.groupby(['first_word', 'second_word']).size().reset_index(name='O11')

# N = len(word_combinations)  
# print(N)
# first_word_counts = df.groupby('first_word')['O11'].sum().reset_index(name='total_first_word_count')
# df = df.merge(first_word_counts, on='first_word', how='left')
# df['O12'] = df['total_first_word_count'] - df['O11']
# second_word_counts = df.groupby('second_word')['O11'].sum().reset_index(name='total_second_word_count')
# df = df.merge(second_word_counts, on='second_word', how='left')
# df['O21'] = df['total_second_word_count'] - df['O11']
# df['O22'] = N - df['O11'] - df['O12'] - df['O21']
# df['first_word_count'] = df['total_first_word_count'] 
# df['second_word_count'] = df['total_second_word_count'] 

# df_nearest = df[(df['first_word'] == 'train')].sort_values(by=['O11'], ascending=False)
# df_nearest = df_nearest.reset_index(drop=True)


# def calculate_mi(row, N):
#   mi_total = 0
#   O_11 = row['O11']
#   O_12 = row['O12']
#   O_21 = row['O21']
#   O_22 = row['O22']
#   O_1_sum = O_11 + O_12  
#   O_2_sum = O_21 + O_22  
#   O_sum_1 = O_11 + O_21  
#   O_sum_2 = O_12 + O_22  

#   O_ij_list = [(O_11, O_1_sum, O_sum_1),
#                (O_12, O_1_sum, O_sum_2),
#                (O_21, O_2_sum, O_sum_1),
#                (O_22, O_2_sum, O_sum_2)]

#   for O_ij, O_i_sum, O_j_sum in O_ij_list:
#     if O_ij > 0:
#       mi_total += (O_ij / N) * np.log2((N * O_ij) / (O_i_sum * O_j_sum))
#   return mi_total
# df['MI'] = df.apply(lambda row: calculate_mi(row, N), axis=1)

# df['PMI'] = np.log2((df['O11'] * N) / (df['total_first_word_count'] * df['total_second_word_count']))

# if N > 0:
#     df['x_bar'] = df['O11'] / N
#     df['mu'] = (df['total_first_word_count'] * df['total_second_word_count']) / (N ** 2)  # Р С›Р В¶Р С‘Р Т‘Р В°Р ВµР СР В°РЎРЏ РЎвЂЎР В°РЎРѓРЎвЂљР С•РЎвЂљР В° Р В±Р С‘Р С–РЎР‚Р В°Р СР СРЎвЂ№
#     df['s2'] = df['x_bar'] * (1 - df['x_bar'])
#     df['t_value'] = np.where(df['s2'] > 0,
#                              (df['x_bar'] - df['mu']) / np.sqrt(df['s2'] / N), 0)  # Р  Р В°РЎРѓРЎвЂЎР ВµРЎвЂљ t-Р С”РЎР‚Р С‘РЎвЂљР ВµРЎР‚Р С‘РЎРЏ
# else:
#     df['t_value'] = 0
# df_nearest = df_nearest.merge(df[['first_word', 'second_word', 't_value']], on=['first_word', 'second_word'], how='left')

# #t_critical = stats.t.ppf(1 - alpha, df=N-1)
# #print(t_critical)

# df_loss_pmi = df[df['first_word'] == 'train'][['first_word', 'second_word', 'PMI']].sort_values(by='PMI', ascending=False)
# df_loss_mi = df[df['first_word'] == 'train'][['first_word', 'second_word', 'MI']].sort_values(by='MI', ascending=False)

# with pd.ExcelWriter('loss.xlsx') as writer:
#     df_nearest[['first_word', 'second_word', 'O11', 'O12', 'O21', 'O22', 'first_word_count', 'second_word_count']].to_excel(writer,sheet_name='Bigrams', index=False)
#     df_nearest[['first_word', 'second_word', 't_value']].sort_values(by='t_value', ascending=False).to_excel(writer, sheet_name='T_Values', index=False)
#     df_loss_pmi.to_excel(writer, sheet_name='PMI', index=False)
#     df_loss_mi.to_excel(writer, sheet_name='MI', index=False)


import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np


biagrams_df = pd.read_excel('loss.xlsx', sheet_name='Bigrams')
t_values_df = pd.read_excel('loss.xlsx', sheet_name='T_Values')
pmi_df = pd.read_excel('loss.xlsx', sheet_name='PMI')
mi_df = pd.read_excel('loss.xlsx', sheet_name='MI')

collocations_df = pd.read_excel('loss.xlsx', sheet_name='collocation')

collocations_df = collocations_df.sort_values(by=['first_word', 'second_word']).reset_index(drop=True)
t_values_df = t_values_df.sort_values(by=['first_word', 'second_word']).reset_index(drop=True)
pmi_df = pmi_df.sort_values(by=['first_word', 'second_word']).reset_index(drop=True)
mi_df = mi_df.sort_values(by=['first_word', 'second_word']).reset_index(drop=True)

def plot_roc_curve(df, criterion_column, criterion_name):
    y_true = collocations_df['collocation']
    y_scores = df[criterion_column]

    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    auc_value = auc(fpr, tpr)

    
    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx]

  
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=criterion_name)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC-РєСЂРёРІР°СЏ РґР»СЏ РєСЂРёС‚РµСЂРёСЏ {}'.format(criterion_name))
   

    
    plt.plot(fpr[optimal_idx], tpr[optimal_idx], 'ro', label='Optimal Point')

    
    max_fpr = np.max(fpr)
    max_tpr = np.max(tpr)
    diagonal = np.linspace(0, max_tpr, num=100)
    plt.plot(diagonal, diagonal, 'k--', label='Random Classifier')
    
    
    print('AUC for {}: {}'.format(criterion_name, auc_value))
    print('Optimal threshold for {}: {}'.format(criterion_name, optimal_threshold))
    print('Optimal point: (FPR: {}, TPR: {})'.format(fpr[optimal_idx], tpr[optimal_idx]))

    plt.show()


plot_roc_curve(t_values_df, 't_value', 't-test')
plot_roc_curve(pmi_df, 'PMI', 'PMI')
plot_roc_curve(mi_df, 'MI', 'MI')