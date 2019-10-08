import fasttext
import multiprocessing
import os
import io
import pymystem3
import gensim

MODEL_PATH = r"D:\PycharmProjects\untitled2\embendings\fasttext_model_no_gensim\cc.ru.300.vec"
# result_big_doc = []
# with open("data.txt", "w") as w:
#     for root, dir, files in os.walk(r"D:\PycharmProjects\untitled2\embendings\Final_Dataset"):
#         for file in files:
#             path = "{}\\{}".format(root, file)
#             print(path)
#             with open(path, "r") as r:
#                 w.write(r.read())
#                 w.write("\n")

# model = fasttext.train_unsupervised(input='data1.txt',
#                                         model='skipgram',
#                                         dim=300,
#                                         epoch=6,
#                                         thread=multiprocessing.cpu_count())

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

model =  gensim.models.word2vec.Word2VecKeyedVectors(load_vectors(MODEL_PATH))


def test(model):
    while True:
        in_word = input("Введите слово или q: ")
        if in_word == "q": break
        in_word = pymystem3.Mystem().lemmatize(in_word)[0]
        try:
            for word in model.most_similar(positive=[in_word], topn=10):
                print(word)
        except KeyError:
            print("word '{}' not in vocabulary".format(in_word))

test(model)
#model.save_model(r"D:\PycharmProjects\untitled2\embendings\models\fasttext_no_gensim\model_fasttext_no_gensim.bin")

