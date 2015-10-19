# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class DeviantItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name   = Field()
    author = Field()
    date   = Field()
    url    = Field()
