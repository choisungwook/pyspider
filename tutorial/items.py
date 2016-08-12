# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TutorialItem(Item):
    session_id = Field()
    depth = Field()
    current_url = Field()
    referring_url = Field()
    title = Field()
