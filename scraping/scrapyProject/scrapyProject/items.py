# Define here the models for your scraped items

import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    pubDate = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    keywords = scrapy.Field()
    robots = scrapy.Field()
    body = scrapy.Field()
    keywords1 = scrapy.Field()
