# -*- coding: utf-8 -*-
#from scrapy.spider import Spider
from scrapy.selector import Selector
from myCrawl.items import FirstDemoItem 
import scrapy
import re
class BaiduSpider(scrapy.Spider):
	name = "rent"
	allowed_domains = ["rent.com"]
	start_urls = ['https://www.rent.com/california/riverside-apartments/berkdale-apartments-4-477789']

	def parse(self,response):
		item = FirstDemoItem()
		item['title'] = response.xpath('/html/head/title/text()').extract()
		sel = Selector(response)
		#This part for split the location of the house
		locations = response.xpath("//div[@class='pdp-heading-address']")
		for index,addr in enumerate(locations):
			print("number of addr: ",index)
			item['streetaddr'] = addr.xpath(".//span[@itemprop='streetAddress']/text()").extract()
			item['city'] = addr.xpath(".//span[@itemprop='addressLocality']/text()").extract()
			item['state'] = addr.xpath(".//span[@itemprop='addressRegion']/text()").extract()
			item['zipcode'] = addr.xpath(".//span[@itemprop='postalCode']/text()").extract()
			#print(streetaddr,city,state,zipcode)
		
		#This part for get basic inoformation of the hosue
		divs = sel.xpath("//div[@class='pdp-heading-meta']") # basic information block
		round_num = 0    
		for div in divs:
			print("round:", round_num)
			round_num +=1		
			item['phone'] = div.xpath(".//span[@class='pdp-heading-meta-phone hidden-xs']/a/@href").extract()
			item['price'] = div.xpath(".//span[@class='pdp-heading-meta-rent bold']/text()").extract()    
			item['beds']  = div.xpath(".//span[@class='pdp-heading-meta-beds']/text()").extract()   
			item['pet'] = div.xpath(".//span[@class='pdp-heading-meta-pets']/text()").extract()    
		#This part for getting all the floor plan
		print ("---start working for home plans") 
		#homes = response.xpath("//div[@class='floorplans clearfix']")#homes block
		homes_price = response.xpath("//div[@class='floorplan-item floorplan-rent hidden-xs hidden-sm']")#homes_price
		homes_style = response.xpath("//div[@class='floorplan-item floorplan-bed-bath hidden-xs hidden-sm']")#?B?B
		homes_size = response.xpath("//div[@class='floorplan-item floorplan-sqft hidden-xs hidden-sm']")#sqft
		res = ""
		for style,price,size in zip(homes_style,homes_price,homes_size):
			round_num+-1
			data_style =  (style.xpath(".//text()").extract())[0]
			data_price =  (price.xpath(".//text()").extract())[0]
			data_size =  (size.xpath(".//text()").extract())[0].replace('\xa0',"")
			res =res + data_style+" "+data_price+ " "+data_size +" | "
		item['house_plan']  = res
		print ("---end working for home plans")
		parking_info = response.xpath("//div[@class='amenity-grid clearfix']")
		for index,park in enumerate(parking_info):
			print("index",index)
			if index ==0:
				item['Kitchen'] = park.xpath(".//span[@class='sprite-text']/text()").extract()
			elif index ==1:
				item['Laundry'] = park.xpath(".//span[@class='sprite-text']/text()").extract()
			elif index ==2:
				item['Parking'] = park.xpath(".//span[@class='sprite-text']/text()").extract()
			elif index ==3:
				item['Pets'] = park.xpath(".//span[@class='sprite-text']/text()").extract()
	
			elif index ==4:
				item['Features'] = park.xpath(".//span[@class='sprite-text']/text()").extract()
			elif index ==5:
				item['Community'] = park.xpath(".//span[@class='sprite-text']/text()").extract()
		yield item		
