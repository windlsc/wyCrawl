# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WycrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'tickets'
    ticket_name = Field()
    ticket_id = Field()
    ticket_date = Field()
    ticket_price = Field()
    
