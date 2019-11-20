import json
import pymystem3
from nltk.stem import snowball
from sklearn.feature_extraction.text import *
import numpy as np
from sklearn.linear_model import *
from sklearn.metrics import pairwise_distances
import re
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, StandardScaler
from itertools import starmap
import joblib
from regression.metric import get_NDCG

stemmer = snowball.RussianStemmer()
lemmatizer = pymystem3.Mystem()
RAW_JSON_PAH = "../data/train.json"
PATTERN = re.compile("[^а-яА-Я0-9$ ]")
W_i = [0.4, 0.4, 0.2]
SKALER = StandardScaler()
NORMALIZER = Normalizer(norm='l2')

with open(RAW_JSON_PAH, "r", encoding="utf-8") as r:
    data = json.load(r)

def rating(params):
    return sum(starmap(lambda x, w: x * w, zip(params, W_i)))

def stemm(string):
    return str([stemmer.stem(i) for i in string.split()])

def class_data_2_cosine(klass):
    vectorizer = TfidfVectorizer()
    klass_key = str(*klass.keys())
    klass_data = klass[klass_key]
    all_class_sent = [i for sample in klass_data for i in sample.values()]
    all_class_sent = "$".join(all_class_sent)
    all_class_sent = PATTERN.sub(" ", all_class_sent)
    all_class_sent = " ".join(lemmatizer.lemmatize(all_class_sent))
    all_class_sent = all_class_sent.split("$")
    all_class_sent = [stemm(sample) for sample in all_class_sent]
    tf_idf_matrix = vectorizer.fit_transform(all_class_sent)
    tf_idf_query = vectorizer.transform([stemm(klass_key)])
    cosine_similarity = pairwise_distances(tf_idf_matrix, tf_idf_query, metric='cosine')
    cosine_similarity = (lambda x: 1 - x)(cosine_similarity)
    cosine_similarity = np.array([[cosine_similarity[i + j][0] for j in range(3)] \
                                  for i in range(0, len(cosine_similarity), 3)])
    return cosine_similarity

def prepare_train_data(data):
    result_matrix = [sample for klass in data for sample in class_data_2_cosine(klass)]
    result_matrix = np.array(result_matrix)
    result_matrix = SKALER.fit_transform(result_matrix)
    result_matrix = NORMALIZER.fit_transform(result_matrix)
    joblib.dump(SKALER, 'skaler.bin', compress=1)
    joblib.dump(NORMALIZER, 'normalizer.bin', compress=1)
    data_len = len(result_matrix)
    summ_marks = sum([rating(row) for row in result_matrix])
    middle_mark = summ_marks / data_len
    noize = np.random.normal(0, scale=abs(middle_mark * 0.05), size=data_len)
    result_matrix = np.array(list(starmap(lambda row, noiz, i: (row, rating(row) + noiz, i),
                                          zip(result_matrix, noize, range(len(result_matrix))))))
    result_matrix = sorted(result_matrix, key=lambda x: x[1], reverse=True)
    data_labels = np.repeat(range(5, 0, -1), data_len // 5)
    result_matrix = [(i[0], lab, i[2]) for i, lab in zip(result_matrix, data_labels)]
    return result_matrix


def main():
    result_matrix = prepare_train_data(data)
    X_train, X_test, y_train, y_test = train_test_split([i[0] for i in result_matrix],
                                                        [i[1] for i in result_matrix],
                                                        test_size=0.33, random_state=42)
    model = Pipeline([
        ("log", LinearRegression(
        #solver='lbfgs',
        #max_iter=150,
        #multi_class='multinomial',
        n_jobs=-2))])

    model.fit(X_train, y_train)
    print("Regression coefficients: ", model.named_steps['log'].coef_)
    print("Train precision:", model.score(X_train, y_train))
    print("Test precision:", model.score(X_test, y_test))
    joblib.dump(model, 'filename.pkl', compress=1)

   # check_NDCG(sorted(result_matrix, key=lambda x:x[2])[:41])


def sample_ndsg(data):
    cosine_matrix = [sample for klass in data for sample in class_data_2_cosine(klass)]
    cosine_matrix = np.array(cosine_matrix)
    SKALER = joblib.load('skaler.bin')
    NORMALIZER = joblib.load('normalizer.bin')

    cosine_matrix = SKALER.fit_transform(cosine_matrix)
    cosine_matrix = NORMALIZER.fit_transform(cosine_matrix)

    cosine_matrix = np.array(list(starmap(lambda row, i: (row, rating(row), i),
                                          zip(cosine_matrix, range(len(cosine_matrix))))))
    cosine_matrix = sorted(cosine_matrix, key=lambda x: x[1], reverse=True)
    data_labels = np.repeat(range(5, 0, -1), len(cosine_matrix) // 5)
    cosine_matrix = [(i[0], lab, i[2]) for i, lab in zip(cosine_matrix, data_labels)]
    cosine_matrix = sorted(cosine_matrix, key=lambda x:x[2])
    return cosine_matrix

def check_NDCG(result_matrix, p=20):
    ind = [i[2] for i in result_matrix]
    tmp = [i[1] for i in result_matrix]
    tmp_predict =  [i[0] for i in result_matrix]
    print('Old NDCG: ', get_NDCG(tmp, p))
    model = joblib.load("filename.pkl")
    pred = model.predict(tmp_predict)
    res = sorted(list(zip(tmp, pred, ind)), key=lambda x: x[1], reverse=True)
    print('New NDCG: ', get_NDCG([i[0] for i in res], p))
    return res

main()
data_sample = data[2]
print(data_sample.keys())
sor = check_NDCG(sample_ndsg([data_sample]))
sor = [i[2] for i in sor]
lst = list(data_sample.values())[0]
print(lst)
result = []
for v, i in zip(lst, sor):
    print(v)
    result.append(lst[i])
print("-"*100)
for r in result:
    print(r)

