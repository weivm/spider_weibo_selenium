# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderWeiboSeleniumItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
