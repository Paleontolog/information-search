from math import ceil
from multiprocessing import Pool
import numpy as np
import help.helpers as h

def leven_distance(str1, str2):
    N = len(str1) + 1
    M = len(str2) + 1
    matrix = [[0] * M for _ in range(N)]
    for i in range(N):
        matrix[i][0] = i
    for j in range(M):
        matrix[0][j] = j
    for i in range(1, N):
        for j in range(1, M):
            matrix[i][j] = min(matrix[i][j - 1] + 1,
                               matrix[i - 1][j] + 1,
                               matrix[i - 1][j - 1] +
                               (str1[i - 1] != str2[j - 1]))
    return matrix[N - 1][M - 1]



def top_similar(dict, str, top):
    most_similar = []
    for i, word in enumerate(dict):
        distance = leven_distance(word, str)
        if i < top:
            most_similar.append((word, distance))
        elif most_similar[-1][1] > distance:
            most_similar[-1] = (word, distance)

        most_similar = sorted(most_similar, key=lambda x: x[1])

    return most_similar


from functools import partial

def top_similar_parallel_help(dict, step, str, top, st):
    most_similar = []
    for i, word in enumerate(dict[st:st + step]):
        distance = leven_distance(word, str)
        if i < top:
            most_similar.append((word, distance))
        elif most_similar[-1][1] > distance:
            most_similar[-1] = (word, distance)
        most_similar = sorted(most_similar, key=lambda x: x[1])
    return most_similar


def top_similar_parallel(dict, word, top):
    dict_len = len(dict)
    step = ceil(dict_len / 12)
    pool = Pool(12)
    f = partial(top_similar_parallel_help, dict, step, word, top)
    res = pool.map(f, range(0, dict_len, step))

    res = (lambda ll: [el for lst in ll for el in lst])(res)
    res = sorted(res, key=lambda x: x[1])
    print(res[:15])
    return  res


# 1601934

if __name__ == "__main__":
    # print(leven_distance("EXPONENTIAL", "POLYNOMIAL"))
    dict = h.create_dict()
    top_similar_parallel(dict, "еретик", 15)
    # print(top_similar(dict, "карова", 15))
