from help.helpers import create_dict
import json
import collections
from typos.Levenshtein_distance import *
import time

TOP_SIMILAR_KGRAMMS = 4000
TOP_SIMILAR_RESULT = 20


def generate_kgramms(word, k):
    word = "${}$".format(word)
    w_l = len(word) + 1
    return [word[i:i + k] for i in range(0, max(w_l - k, 1))]


def generate_kGramm_index(dictionary, k):
    print("Kgrams index start")
    kgram_index = {}
    for i, word in enumerate(dictionary):
        splitted = generate_kgramms(word, k)
        for kgram in splitted:
            kgram_in_index = kgram_index.get(kgram)
            if kgram_in_index is not None:
                kgram_in_index.append(i)
            else:
                kgram_index[kgram] = [i]
    print("Kgrams index end")
    return kgram_index


def all_words_on_all_kgrams(kgrams_index, word_kgram):
    print("Kgrams on all words start")
    all_kgrams = collections.Counter()
    for kgram in word_kgram:
        list_ind = kgram_index.get(kgram)
        if list_ind is not None:
            for ind in list_ind:
                all_kgrams[ind] += 1
    print("Kgrams on all words end")
    return all_kgrams.most_common(TOP_SIMILAR_KGRAMMS)


def most_similar_on_kGramms(dictionary, word, k, kgrams_index):
    print("Most similar start")
    word_kgram = set(generate_kgramms(word, k))
 #   print(word_kgram)

    all_candidates = all_words_on_all_kgrams(kgrams_index, word_kgram)

    print("Most similar end")
    return top_similar([dictionary[i[0]] for i in all_candidates], word, TOP_SIMILAR_RESULT)


if __name__ == "__main__":
    # dict = create_dict()
    # kgram_index = generate_kGramm_index(dict, 3)
    # with open("../data/dictionary/kgrams.json", "w") as write_file:
    #      json.dump(kgram_index, write_file)

    dict = create_dict("../data/dictionary/dictionary_clean_unicue.txt", "utf8")
    kgram_index = generate_kGramm_index(dict, 3)
    # with open("../data/dictionary/kgrams.json", "r") as write_file:
    #     kgram_index = json.load(write_file)

    while True:
        word = input("word: ").strip().lower()
        if word == "ex": break
        t = time.time()
        rezult = most_similar_on_kGramms(dict, word,
                                 kgrams_index=kgram_index, k=3)
        print(time.time() - t)
        print("\n".join([str(i) for i in rezult]))
