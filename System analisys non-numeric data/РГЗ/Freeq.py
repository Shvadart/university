import pandas as pd
import numpy as np
import math
import re
from scipy.stats import t
from scipy.stats import chi2
from collections import Counter
file_path = 'text_sent_2.txt'
target_word = 'train'

total_bigrams = 0
target_word_count = 0


with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
def get_bigramms():
    # Разбиваем текст на предложения

    sentences = re.split(r'\n+', text)  # предполагается, что предложения уже разделены по строкам
    global total_bigrams
    global target_word_count 
    # Список для хранения биграмм, где ERROR стоит на второй позиции
    bigrams_with_error = []
    
    # Обрабатываем каждое предложение
    for sentence in sentences:
        # Разбиваем предложение на слова
        words = sentence.split()
        total_bigrams+=len(words)-1
        # Ищем биграммы с variance как word2
        for i in range(0,len(words) - 1):
            if words[i] == target_word :
                target_word_count += 1  
                bigrams_with_error.append((words[i],words[i+1]))

    # Подсчитываем частоту биграмм
    bigram_counts = Counter(bigrams_with_error)
    
    return bigram_counts.most_common()

arr = get_bigramms()
result=[]
for bigram in arr:
    
    word1=bigram[0][0]
    word2=bigram[0][1]
    o12=0
    o21=0
    o22=0
  
    sentences = re.split(r'\n+', text)  # предполагается, что предложения уже разделены по строкам
  
    for sentence in sentences:
       
        # Разбиваем предложение на слова
        words = sentence.split()
       
        for i in range(len(words) - 1):
            if words[i] == word1 and words[i+1]!=word2:  
                o12+=1
            if words[i] != word1 and words[i+1]==word2:
                o21+=1
               
    # o21=211-bigram[1]     
    result.append([word1,word2,bigram[1],o12,o21,total_bigrams-o12-o21-bigram[1]])


df = pd.DataFrame(result,columns=['word1','word2','o11','o12','o21','o22'])
# Сохранение DataFrame в Excel
df.to_excel('result.xlsx', index=False)
print(total_bigrams)
print(target_word_count)
print("Данные успешно сохранены в файл 'result.xlsx'.")