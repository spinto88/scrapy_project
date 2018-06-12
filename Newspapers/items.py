# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewspapersItem(scrapy.Item):

    id_note = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    prefix = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
