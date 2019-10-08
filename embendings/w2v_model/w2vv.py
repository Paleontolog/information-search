# from __future__ import print_function
import time
import gensim
from embendings.helpers.help import NextSentMem, BatchLogger
from help import *
import multiprocessing
from gensim.models import word2vec
from gensim.models.callbacks import CallbackAny2Vec


# final_paths - путь к файлу со списком путей к обработанным файлам
# option - создать новую модель create или открыть старую
# model_path - путь к модели если загружаем существующую
def train_word2vec(data_paths="", data=None, model_paths="", model_save_path="", epochs=1, option="create"):
    model = None
    start = time.time()
    if option == "load":
        print('Loading Word2Vec model...')
        model =gensim.models.word2vec.Word2Vec.load(model_paths)
    else:
        print("Paths reads", len(data_paths))
        if option == "create":
            print('Creating Word2Vec model...')
            model = gensim.models.Word2Vec(size=300,
                                           window=10,
                                           sg=1,
                                           sample=1e-5,
                                           workers=multiprocessing.cpu_count(),
                                           compute_loss=True,
                                           callbacks=[BatchLogger(model_save_path)])

            model.build_vocab(NextSentMem(data))
            print("Vocabulary is builded!", time.time() - start, len(model.wv.vocab))
            model.train(NextSentMem(data),
                        epochs=epochs,
                        total_examples=model.corpus_count,
                        compute_loss=True,
                        callbacks=[BatchLogger(model_save_path)])
            model.save(model_save_path.format("Base"))
        elif option == "retrain":
            print('Retraining Word2Vec model...')
            model = word2vec.Word2Vec.load(model_paths)
            model.train(NextSentMem(data),
                        epochs=epochs,
                        total_examples=model.corpus_count,
                        compute_loss=True,
                        callbacks=[BatchLogger(model_save_path)])
            model.save(model_save_path.format("Ret"))
    print("Process ended!", time.time() - start)
    return model
