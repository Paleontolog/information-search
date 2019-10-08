from scrapy import Item, Field

class Book(Item):
    rating = Field()
    name = Field()
    author = Field()
    price = Field()
    ISBN = Field()
    publication_year = Field()
    publisher = Field()
    genre = Field()
    language = Field()
    description = Field()

class Book2(Item):
    name = Field()
    author = Field()
    price = Field()
    ISBN = Field()
    publication_year = Field()
    publisher = Field()
    series = Field()
    description = Field()
    pages = Field()
