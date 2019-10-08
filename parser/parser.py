import os
import re

def load_dataset(input_file ):
    with open(input_file, mode="r", encoding='utf-8') as f:
        dataset_words = f.read()
        dataset_words = dataset_words.lower()
    return dataset_words

def save_dataset(output_file, dataset):
    with open(output_file, mode="w", encoding='utf-8') as w:
        w.write(dataset)


def clean_dataset(dataset):
    pattern = r"[^ёа-я-\n]"
    pattern = re.compile(pattern)
    dataset = pattern.sub("", dataset)
    pattern = r"(-+(?=\s))|(\W-+(?=\w))"
    pattern = re.compile(pattern)
    dataset = pattern.sub("", dataset)
    return dataset

dataset = load_dataset("dictionary.txt")
dataset = clean_dataset(dataset)
dataset = set(dataset.split("\n"))
save_dataset("dictionary_clean_unicue.txt", "\n".join(dataset))
