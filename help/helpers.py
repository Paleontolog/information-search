def create_dict(path, encoding="cp1251"):
    print("Start creation dictionary")
    with open(path, "r", encoding=encoding) as dict:
        dict = [word.strip() for word in dict.read().lower().split()]
        print("Dictionary created")
        return dict