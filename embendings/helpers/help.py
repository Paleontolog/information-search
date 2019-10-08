import time

from gensim.models.callbacks import CallbackAny2Vec


class NextSent:
    def __init__(self, pathList):
        self.pathList = pathList

    def __iter__(self):
        for file in self.pathList:
            with open(file.rstrip(), "r") as doc:
                for sent in doc.read().split("\n"):
                    yield sent.split()


class NextSentMem:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for text in self.data:
            for sent in text.split("\n"):
                yield sent.split()


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
        l = abs(self.prevloss - model.get_latest_training_loss())
        print("Epoch #{} time: {} loss: {}".format(self.epoch,
                                                   time.time() - self.start_time,
                                                   l))
        self.prevloss = model.get_latest_training_loss()
        try:
            if self.epoch % 5 == 0:
                model.save(self.save_path.format((self.epoch + 4) // 5))
        except: pass

