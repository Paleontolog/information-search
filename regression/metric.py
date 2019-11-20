import math

def get_DCG(array, p):
    dcg_score = 0
    for i in range(1, p):
        logPosition = math.log(i + 1, 2)
        dcgAdder = (math.pow(2, array[i - 1]) - 1) / logPosition
        dcg_score += dcgAdder
    return dcg_score

def get_NDCG(array, p):
    dcgScore = get_DCG(array, p)
    array = sorted(array, reverse=True)
    idcgScore = get_DCG(array, p)

    return dcgScore / idcgScore
