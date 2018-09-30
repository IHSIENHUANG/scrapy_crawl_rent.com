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
		#item['phone'] = response.xpath("//div[@class='pdp-heading-meta']/text())").extract()
		sel = Selector(response)
		divs = sel.xpath("//div[@class='pdp-heading-meta']") # basic information block
		round_num = 0    
		for div in divs:
			print("round:", round_num)
			round_num +=1		
			item['phone'] = div.xpath(".//span[@class='pdp-heading-meta-phone hidden-xs']/a/@href").extract()
			item['price'] = div.xpath(".//span[@class='pdp-heading-meta-rent bold']/text()").extract()    
			item['beds']  = div.xpath(".//span[@class='pdp-heading-meta-beds']/text()").extract()   
			item['pet'] = div.xpath(".//span[@class='pdp-heading-meta-pets']/text()").extract()    
			#for href in  div.xpath(".//span[@class='pdp-heading-meta-phone hidden-xs']/a/@href").extract(): 
			#	print (href)
			#print(item['phone'])
		print ("---start working for home plans") 
		#homes = response.xpath("//div[@class='floorplans clearfix']")#homes block
		homes_price = response.xpath("//div[@class='floorplan-item floorplan-rent hidden-xs hidden-sm']")#homes_price
		homes_style = response.xpath("//div[@class='floorplan-item floorplan-bed-bath hidden-xs hidden-sm']")#homes_price
		homes_size = response.xpath("//div[@class='floorplan-item floorplan-sqft hidden-xs hidden-sm']")#homes_price
		#homes = homes.xpath(".//details[@class='floorplan-group expand'") 
		for style,price,size in zip(homes_style,homes_price,homes_size):
			print("hone round:",round_num)
			round_num+-1
			data_style =  (style.xpath(".//text()").extract())
			data_price =  (price.xpath(".//text()").extract())
			data_size =  (size.xpath(".//text()").extract())[0].replace('\xa0',"")
			print(data_style,data_price,data_size)
			#for data in datas:
			#	print(data)
				#if re.search( "Studio",data):
				#	print ("\nreg exp:",data,end=" ")
		print ("---end working for home plans")
		yield item		
