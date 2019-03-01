# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item,Field
import scrapy

class FirstDemoItem(Item):
    # define the fields for your item here like:
    #name = Field()
    #description = Field()
    #url = Field()
	title = Field()
	streetaddr = Field()
	city = Field()
	state = Field()
	zipcode = Field()
	#phone = Field()
	price = Field()
	pet = Field()
	beds = Field()
	house_plan = Field()
	Parking = Field()
	Pets = Field()
	Kitchen = Field()
	Laundry = Field()
	Features = Field()
	Community = Field()
	Additional = Field()
	url_from = Field()
	#url_to = Field()
class CrawlCityItem(Item):
	cityname = Field()
	state = Field()
class MycrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    pass
