import os
from nltk.tokenize import sent_tokenize
import string
from pymystem3 import Mystem
import re
#import zipfile as zip
#import rarfile as rar
import time
lemmat = Mystem()
#rar.UNRAR_TOOL=r"C:\Program Files\WinRAR\UnRAR.exe"
slash = "\\"

def give_me_paths(path):
    raw_d_dirs = set()
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            if file.endswith(".html"):
                raw_d_dirs.add(root + "\\" + file)
    """
            elif zip.is_zipfile(root + "\\" + file):
                try:
                    with zip.ZipFile(root + "\\" + file, "r") as arch:
                        arch.extractall(root)
                        for f in arch.filelist:
                            if f.filename.endswith(".html"):
                                raw_d_dirs.add(root + "\\" +
                                               f.filename.replace("/", "\\"))
                except zip.BadZipfile:
                    print("Bad zip ->", root + "\\" + file)
                except:
                    print("WTF error", root + "\\" + file)
    """
    """
            elif rar.is_rarfile(root + "\\" + file):
                try:
                    with rar.RarFile(root + "\\" + file, "r") as arch:
                        arch.extractall(root)
                        for f in arch.infolist():
                            if (f.filename.endswith(".html")):
                                raw_d_dirs.add(root + "\\" +
                                               f.filename.replace("/", "\\"))
                except rar.BadRarFile:
                    print("Bad rar ->", root + "\\" + file)
                except:
                    print("Unknown Error", root + "\\" + file)
    """
    return raw_d_dirs


def normalize_text(files_path ="", stop_w_path="", res_folder="", error_files="", final_paths=""):
    with open(r"tmp_path.txt", "r") as files:
        list_files = [file for file in files.read().split()]

    with open(r"stop_words.txt", "r") as stop_w:
        stop_word = {i for i in stop_w.read().split()}

    pattern = r"[^а-яА-Я0-9.?!, ]+"
    res_folder = r"NewDataset\NewDataset"
    error_files, final_paths = [], []
    with open(r"error_files.txt", "w") as err:
        err.write("\n".join(error_files))
    for cntr, file in enumerate(list_files):
        st = time.time()
        outp_string = res_folder + slash + slash.join(file.split(slash)[1:])
        print(outp_string)
        with open(file, "r") as inp, \
                open(outp_string, "w") as outp:
            try:
                text = re.sub(pattern, " ", inp.read())
                final_paths.append(outp_string)
            except UnicodeDecodeError:
                print("IT'S ERROR FILE", file)
                error_files.append(file)
                continue
            text = sent_tokenize(text, language='russian')
            result = []
            for sent in text:
                sentence = []
                for word in sent.lower().split():
                    word = word.strip(string.punctuation)
                    if word not in stop_word:
                        sentence.append(word)
                sentence.append("\n")
                result.append(' '.join(sentence))
            rez = lemmat.lemmatize(''.join(result))
            outp.write("".join(rez))
        if cntr % 40 == 0:
            with open(r"error_files.txt", "a") as err:
                err.write("\n".join(error_files))
                error_files.clear()
        print(time.time() - st)

    new_dir = r"final_paths_new.txt"
    with open(new_dir, "w") as res:
        res.write("\n".join(final_paths))
