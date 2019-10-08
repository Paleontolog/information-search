# from __future__ import print_function
import time
import gensim
import multiprocessing
from gensim.models import fasttext
from gensim.models.callbacks import CallbackAny2Vec

from embendings.helpers.help import NextSentMem


class BatchLogger(CallbackAny2Vec):
    def __init__(self, save_path):
        self.epoch = 1
        self.save_path = save_path
        self.prevloss = 0
        self.start_time = None

    def on_epoch_begin(self, model):
        self.epoch += 1
        self.start_time = time.time()

    def on_epoch_end(self, model):
        print("Epoch #{} time: {}".format(self.epoch, time.time() - self.start_time))
        try:
            if self.epoch % 5 == 0:
                model.save(self.save_path.format((self.epoch + 4) // 5))
        except: pass

# final_paths - путь к файлу со списком путей к обработанным файлам
# option - создать новую модель create или открыть старую
# model_path - путь к модели если загружаем существующую
def train_fast_text(data_paths="", data=None, model_paths="", model_save_path="", epochs=1, option="create"):
    model = None
    start = time.time()
    if option == "load":
        print('Loading FastText model...')
        model = fasttext.FastText.load(model_paths)
    else:
        print("Paths reads", len(data_paths))
        if option == "create":
            print('Creating FastText model...')
            model = fasttext.FastText(size=300,
                                           window=10,
                                           sg=1,
                                           sample=1e-5,
                                           workers=multiprocessing.cpu_count(),
                                           callbacks=[BatchLogger(model_save_path)])

            model.build_vocab(NextSentMem(data))
            print("Vocabulary is builded!", time.time() - start, len(model.wv.vocab))
            model.train(NextSentMem(data),
                        epochs=epochs,
                        total_examples=model.corpus_count,
                        compute_loss=True,
                        report_delay=1.0,
                        callbacks=[BatchLogger(model_save_path)])
            model.save(model_save_path.format("Base"))
        elif option == "retrain":
            print('Retraining FastText model...')
            model =  fasttext.FastText.load(model_paths)
            model.train(NextSentMem(data),
                        epochs=epochs,
                        total_examples=model.corpus_count,
                        compute_loss=True,
                        report_delay=1.0,
                        callbacks=[BatchLogger(model_save_path)])
            model.save(model_save_path.format("Ret"))
    print("Process ended!", time.time() - start)
    return model
