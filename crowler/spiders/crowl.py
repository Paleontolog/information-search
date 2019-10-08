from scrapy import Selector, Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import crowler.object as ob
import requests as req
import random
import re
import bs4

# class MySpider(CrawlSpider):
#     name = 'livelib_crowler'
#     allowed_domains = ['livelib.ru']
#
#     custom_settings = {
#         'CLOSESPIDER_ITEMCOUNT': 10000,
#     }
#     # max_items_count = 100
#     # current_downloads = 0
#     pattern = re.compile(r"[\D]")
#     price_pattern = re.compile(r"\w*\"price\w*\":\"(\d+.\d+)\"\w*")
#     id_pattern = re.compile(r"\w*\d+\w*")
#     visited_links = set()
#
#     start_urls = ['https://www.livelib.ru/genres']
#
#     rules = (
#
#         Rule(LinkExtractor(allow=('/book/'), restrict_xpaths=("//a[contains(@class,'brow-book-name with-cycle')]")),
#              callback="parse_item", follow=True),
#
#         # Открываем с главной страницы каждый жанр
#         Rule(LinkExtractor(allow=('/genre/'), restrict_xpaths=("//a[@class='main-genre-title']",)),
#              follow=True),
#
#         # # Открываем больше книг в каждом разделе
#         Rule(LinkExtractor(allow=('/genre/'), restrict_xpaths=("//*[contains(text(), 'Больше книг')]")),
#              follow=True),
#
#         # # Переходим по страницам
#         Rule(LinkExtractor(allow=('/listview/biglist/'), restrict_xpaths=("//a[contains(@id, 'a-list-page-next')]")),
#              follow=True),
#     )
#
#     def parse_item(self, response):
#         if response.url not in self.visited_links:
#             self.visited_links.add(response.url)
#             self.logger.info('Hi, this is an item page! %s', response.url)
#
#             book = Selector(response)
#
#             book_info = ob.Book()
#             book_info["name"] = book.xpath("//span[contains(@itemprop, 'name')]"
#                                            "/text()").extract_first() or "NotDefined"
#
#             book_info["author"] = book.xpath("//a[contains(@id, 'book-author') or "
#                                              "contains(@id, 'author-item')]/text()")\
#                                       .extract_first() or "NotDefined"
#
#             book_info["genre"] = book.xpath("//a[contains(@class, 'label-genre')]/text()")\
#                                      .extract_first() or "NotDefined"
#
#             book_info["ISBN"] = book.xpath("//span[contains(@itemprop, 'isbn')]/text()")\
#                                     .extract_first() or None
#
#             book_info["publication_year"] = book.xpath("//b[contains(text(), 'Год издания')]"
#                                                        "/parent::*//following-sibling::*/text()")\
#                                                 .extract_first() or None
#             book_info["language"] = book.xpath(
#                 "//b[contains(text(), 'Язык')]/parent::*/following-sibling::*/text()")\
#                                         .extract_first() or "NotDefined"
#
#             book_info["publisher"] = book.xpath(
#                 "//span[contains(@itemprop, 'publisher')]/a/text()").extract_first() or "NotDefined"
#
#             book_info["description"] = book.xpath("//p[contains(@id, 'description')"
#                                                   " or contains(@itemprop, 'description')]/text()")\
#                                            .extract_first() or "NotDefined"
#
#             # book_info["price"] = self.parse_shit(book.xpath("//head//link[contains(@rel, 'canonical')]")
#             #                                      .extract_first())
#             book_info["price"] = random.randint(200, 1500)
#             book_info["rating"] = book.xpath("//span[contains(@class, 'rating-book unreg block')]/span/text()")\
#                                       .extract_first() or None
#
#             yield book_info

# s2 = '"price":"159.00"'
# pat = re.compile(r"\w*\"price\w*\":\"(\d+.\d+)\"\w*")
# print(pat.findall(s)[0])


class MySpider(CrawlSpider):
    name = 'books_crowler'
    allowed_domains = ['books.ru']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10000,
    }
    # max_items_count = 100
    # current_downloads = 0
    pattern = re.compile(r"[\D]")
    price_pattern = re.compile(r"\w*\"price\w*\":\"(\d+.\d+)\"\w*")
    id_pattern = re.compile(r"\w*\d+\w*")
    visited_links = set()

    start_urls = ["https://www.books.ru/khudozhestvennaya-literatura-9001274/"]

    rules = (

        Rule(LinkExtractor(allow=('/books/'), restrict_xpaths=("//td[@class='descr']//p[@class='title']//a",)),
             callback="parse_item", follow=True),

        # # Переходим по страницам
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//div[@class='pagination']//li[@class = 'next']/a",)),
             follow=True),
    )

    def parse_item(self, response):
        if response.url not in self.visited_links:
            self.visited_links.add(response.url)
            self.logger.info('Hi, this is an item page! %s', response.url)

            book = Selector(response)

            book_info = ob.Book2()
            book_info["name"] = book.xpath("//td[contains(@class,'book-info')]//h1[contains(@itemprop, 'name')]"
                                           "/text()").extract_first() or "NotDefined"

            book_info["author"] = book.xpath("//p[contains(@class, 'author')]/a/text()")\
                                        .extract_first() or \
                                  book.xpath("//p[contains(@class, 'author')]/text()") \
                                        .extract_first() or "NotDefined"

            book_info["series"] = book.xpath("//td[contains(text(), 'Серия')]/parent::*/td/a/text()")\
                                     .extract_first() or "NotDefined"

            book_info["ISBN"] = book.xpath("//td[contains(text(), 'ISBN')]/following-sibling::*/text()")\
                                    .extract_first() or None

            book_info["publication_year"] = book.xpath("//td[contains(text(), 'Дата')]/following-sibling::*/text()")\
                                                .extract_first() or None

            book_info["publisher"] = book.xpath(
                "//td[contains(text(), 'Издательство')]/following-sibling::*/a/text()").extract_first() or "NotDefined"

            book_info["description"] =  book.xpath("//div[@class = 'all_note']").extract_first() or\
                                        book.xpath("//div[@class = 'note']").extract_first() \
                                        or "NotDefined"

            book_info["price"] = book.xpath("//div[@class = 'yprice price']/span/span[1]/text()")\
                                    .extract_first() or None

            book_info["pages"] = book.xpath("//td[contains(text(), 'Объём')]/following-sibling::*/text()")\
                                      .extract_first() or None
            yield book_info
