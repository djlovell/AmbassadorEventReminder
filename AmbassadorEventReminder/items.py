# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class EventItem(Item):
    title = Field()
    date = Field()
    location = Field()
    startTime = Field()
    endTime = Field()
    description = Field()
    numberDesired = Field()
    numberSignedUp = Field()
    numberEmptySpots = Field()
    
