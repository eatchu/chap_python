# -*- coding: utf-8 -*-
"""
csv file -> sparse matrix
 1. csv file read
 2. texts, target 전처리 
 3. max_feature : 열의 차수 결정 - max_feature = 4000 제한
 4. sparse matrix
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import string
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. csv file read
spam_data = pd.read_csv("../data/temp_spam_data2.csv", header = None,
            encoding='utf-8')
print(spam_data.info())
print(spam_data)

# 2. texts, target 전처리 
target = spam_data[0]
texts = spam_data[1]

print(target)
# target dummy(spam=1, ham=0)
target = [ 1 if t == 'spam' else 0 for t in target]
print(target) # [0, 1, 0, 1, 0]

# texts 전처리
def text_prepro(texts):
    # Lower case
    texts = [x.lower() for x in texts]
    # Remove punctuation
    texts = [''.join(c for c in x if c not in string.punctuation) for x in texts]
    # Remove numbers
    texts = [''.join(c for c in x if c not in string.digits) for x in texts]
    # Trim extra whitespace
    texts = [' '.join(x.split()) for x in texts]
    return texts

re_texts = text_prepro(texts)
print(re_texts)
'''
['우리나라 대한민국 우리나라 만세', '비아그라 gram 정력 최고', '나는 대한민국 사람', '보험료 원에 평생 보장 마감 임박', '나는 홍길동']
'''

# 3. max_feature : 열의 차수 결정
tfidf_fit = TfidfVectorizer().fit(re_texts) # 문장 -> 단어벡터 생성기 

voc = tfidf_fit.vocabulary_ # 단어 사전 
print(len(voc)) # 16
# {'우리나라': 9, '대한민국': 2, '만세': 4, '비아그라': 7, 'gram': 0, '정력': 12, '최고': 13, '나는': 1, '사람': 8, '보험료': 6, '원에': 10, '평생': 14, '보장': 5, '마감': 3, '임박': 11, '홍길동': 15}
print(voc)

max_feature = 4000 # 4000 단어 
'''
전체 단어 8603개 중에서 max_feature = 4000 일 때
4000 단어로 짤라서 열의 차수 결정 
'''

# 4. sparse matrix
#help(TfidfVectorizer)
# encoding='utf-8', stop_words=None, max_features=None

tfidf = TfidfVectorizer(stop_words ='english', max_features = max_feature) # object
tfidf_sparse = tfidf.fit_transform(re_texts) # 문서 -> 희소행렬 

print(tfidf_sparse.shape) # (5574, 4000) -> (doc, max_feature)
print(tfidf_sparse)
'''
  (0, 9)        0.8413381201263408 -> 우리나라
  (0, 2)        0.3393931489111758 -> 대한민국
  (0, 4)        0.4206690600631704
'''

# scipy 희소행렬 -> numpy 희소행렬 
tfidf_sparse_arr = tfidf_sparse.toarray()
print(tfidf_sparse_arr)
print(tfidf_sparse_arr.shape) # (5574, 4000)

import numpy as np

# 5. train/test split : 80 : 20
texts_train, texts_test, target_train, target_test = train_test_split(
        tfidf_sparse_arr, target, 
        test_size = 0.2, random_state = 123)

print(texts_train.shape) # (4459, 4000)
print(texts_test.shape) # (1115, 4000)
print(np.shape(target_train)) # (4459,)
print(np.shape(target_test)) # (1115,)

# 6. numpy -> save
import numpy as np
spam_train_test = (texts_train,texts_test,target_train,target_test)

# numpy save
np.save("../data/spam_train_test.npy", spam_train_test)
print('file save...')

# numpy load
x_train,x_test,y_train,y_test = np.load("../data/spam_train_test.npy",allow_pickle=True)

print(x_train.shape)
print(x_test.shape)
print(type(x_train)) # <class 'numpy.ndarray'>
print(np.shape(y_train))
print(np.shape(y_test))
print(type(y_train)) # <class 'list'>


























