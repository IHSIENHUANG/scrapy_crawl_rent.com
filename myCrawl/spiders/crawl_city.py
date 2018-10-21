# -*- coding: utf-8 -*-
#from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from myCrawl.items import CrawlCityItem 
import scrapy
import re
from time import sleep
class BaiduSpider(CrawlSpider):
	name = "crawl_city"
	allowed_domains = ["rent.com"]
	#urls = [r'https://www.rent.com/california/1-19']	
	#start_urls = [val for val in urls]
	start_urls = [r'https://www.rent.com/california/1-19']
	rules = [Rule(LinkExtractor(unique=True),callback='parse_data',follow=False)]	
	def parse_data(self,response):
		#print("start process data)",response.url) 
		#if self.clock%1000==0:
		#	sleep(1)
		response.url = "https://www.rent.com/california/1-19"
		#obj = re.match(r'https://www\.rent\.com/.+/.*/[1-9]+\-[0-9]+',response.url,re.M|re.I)
		#if obj:
		print ("start crawling ",response.url)	
		item = CrawlCityItem()
		sel = Selector(response)
		#This part for split the location of the house
		cities = response.xpath("//ul[@class='col-lg-4']")
		for index,addr in enumerate(cities):
			print("number of group: ",index)
			datas= addr.extract()
			#item['streetaddr'] = addr.xpath(".//span[@itemprop='streetAddress']/text()").extract()
			#item['city'] = addr.xpath(".//span[@itemprop='addressLocality']/text()").extract()
			#item['state'] = addr.xpath(".//span[@itemprop='addressRegion']/text()").extract()
			#item['zipcode'] = addr.xpath(".//span[@itemprop='postalCode']/text()").extract()
			#print(streetaddr,city,state,zipcode)
		yield item		
	 	
