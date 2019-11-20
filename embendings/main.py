#from w2v_model import w2v
#from fasttext_model import fast_text
import json
import collections
from w2v_model.w2v import train_word2vec
import pymystem3
import re
import os

DATASET_PATH = r"D:\PycharmProjects\untitled2\embendings\Final_Dataset"

def get_all_doc(paths):
    result_array = []
    for file in paths:
        with open(file.rstrip(), "r") as doc:
            result_array.append(doc.read())
    return result_array

def get_synonyms_list(words_list, model):
    result = {}
    cnt = 0
    for word in words_list:
        if cnt % 100 == 0: print(cnt)
        cnt += 1
        try:
            result[word] = model.wv.most_similar(positive=[word], topn=5)
        except KeyError:
            result[word] = None
    return result


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



model = train_word2vec(model_paths="models/w2v/new_modelka111_6.model", option="load")

#model = fast_text.train_fast_text(model_paths="models/fasttext/modelka_fast_text_Base.model", option="load")

# model = w2v.train_word2vec(data=result_array,
#                            model_paths="models/new_modelka111.model",
#                            model_save_path="models/new_modelka111_{1}.model",
#                            option="retrain", epochs=30)

# paths = ["{}\\{}".format(DATASET_PATH, file) for file in os.listdir("Final_Dataset")]
# docs = get_all_doc(paths)
# model = fast_text.train_fast_text(data=docs,
#                            model_save_path="models/fasttext/modelka_fast_text_{}.model",
#                            option="create", epochs=10)


if __name__ == "__main__":
    test(model)
    word_set = set()
    with open("scraped_data_utf8_1.json", "r") as r:
        for w in r.readlines():
            for res in json.JSONDecoder().decode(w).values():
                if res is not None:
                    word_set.update(res.split())
    
    patt = re.compile("[^а-я \-]")
    res = " ".join(word_set)
    res = patt.sub("", res).replace("  ", " ").replace("-", " ")
    res = pymystem3.Mystem().lemmatize(res)
    
    with open("stop_words.txt", "r") as r:
        r = r.read().strip().split()
        res = [i for i in res if i not in r]
    
    res = [word for word in res if word in model.wv.vocab]
    res = collections.Counter(res)
    word_set = res.most_common(15000)
    result = get_synonyms_list(word_set, model)
    result = {key[0]:[v[0] for v in val] for key, val in result.items()}
    with open("synonums_fast.json", "w") as w:
         json.dump(result, w)
