from scrapy.crawler import CrawlerProcess

from crowler.spiders.crowl import MySpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES': {'pipelines.pipel.JsonWithEncodingPipeline' : 800,},
})

process.crawl(MySpider)
process.start()
