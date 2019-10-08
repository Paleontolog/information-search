import json
import codecs
import re

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')
        self.expr_text = re.compile(r'[^\w ,.:;-–!?"<>]')
        self.expr_num = re.compile(r'[\D]')
        self.expr_description = re.compile(r'[^а-яА-ЯёЁ\d ,.:;\-–!?]')
        self.clear_start = re.compile(r"[а-яА-ЯёЁ]")

    # def process_item(self, item, spider):
    #     item["ISBN"] = self.expr_num.sub("", item["ISBN"]) if item["ISBN"] is not None else None
    #     item["language"] = self.expr_text.sub("", item["language"]).strip()
    #     item["description"] = self.expr_text.sub("", item["description"]).strip()
    #     item["publication_year"] = self.expr_num.sub("", item["publication_year"]) \
    #         if item["publication_year"] is not None else None
    #     line = json.dumps(dict(item)) + "\n"
    #     self.file.write(line)
    #     return item

    def process_item(self, item, spider):
        item["ISBN"] = self.expr_num.sub("", item["ISBN"]) if item["ISBN"] is not None else None
        str_description = self.expr_description.sub("", item["description"]).strip()
        if str_description.replace(" ", "") != "":
            item["description"] = str_description[self.clear_start.search(str_description).start():]
        else:
            item["description"] = None
        item["publication_year"] = self.expr_num.sub("", item["publication_year"]) \
            if item["publication_year"] is not None else None
        item["author"] = self.expr_text.sub("", item["author"]).strip()
        item["name"] = self.expr_text.sub("", item["name"]).strip()
        item["series"] = self.expr_text.sub("", item["series"]).strip()
        item["publisher"] = self.expr_text.sub("", item["publisher"]).strip()
        item["price"] = self.expr_num.sub("", item["price"]).strip() if item["price"] is not None else None
        item["pages"] = self.expr_num.sub("", item["pages"]).strip() if item["pages"] is not None else None
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()