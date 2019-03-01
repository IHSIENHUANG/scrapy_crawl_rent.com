
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from myCrawl.items import FirstDemoItem 
import scrapy
import re
import itertools
import pandas as pd
from time import sleep
class BaiduSpider(CrawlSpider):
	name = "parse"
	df = pd.read_csv("state_city.csv")
	start_urls = ['file:///home/arishen/myCrawl/data_2019/10.html']
	rules = [Rule(LinkExtractor(
				#allow=(r'\/california/riverside-apartments\?page[2-9]'),
				canonicalize=True,
 				unique=True),
			follow=True,
			callback="parse"
			)
			]

	def parse(self,response):
		#print ("response = :",response.body)
		url = 'file:///home/arishen/myCrawl/data_2019/1.html'
		for i in range(1,185231):
			print ("round:",i)
			url ='file:///home/arishen/myCrawl/data_2019_Feb/'+str(i)+".html"
			yield scrapy.Request(url,callback=self.parse_data,dont_filter=True)

	def parse_data(self,response):
		item = FirstDemoItem()
		item['url_from'] = response.url
		item['title'] = response.xpath('/html/head/title/text()').extract()
		sel = Selector(response)
		#This part for split the location of the house
		locations = response.xpath("//div[@class='pdp-heading-address']")
		for index,addr in enumerate(locations):
			#print("number of addr: ",index)
			item['streetaddr'] = addr.xpath(".//span[@itemprop='streetAddress']/text()").extract()
			item['city'] = addr.xpath(".//span[@itemprop='addressLocality']/text()").extract()
			item['state'] = addr.xpath(".//span[@itemprop='addressRegion']/text()").extract()
			item['zipcode'] = addr.xpath(".//span[@itemprop='postalCode']/text()").extract()
			#print(streetaddr,city,state,zipcode)
		
		#This part for get basic inoformation of the hosue
		divs = sel.xpath("//div[@class='pdp-heading-meta']") # basic information block
		round_num = 0    
		for div in divs:
			item['price'] = div.xpath(".//span[@class='pdp-heading-meta-rent bold']/text()").extract()    
			item['beds']  = div.xpath(".//span[@class='pdp-heading-meta-beds']/text()").extract()   
			item['pet'] = div.xpath(".//span[@class='pdp-heading-meta-pets']/text()").extract()    
		homes_price = response.xpath("//div[@class='floorplan-item floorplan-rent hidden-xs hidden-sm']")#homes_price
		homes_style = response.xpath("//div[@class='floorplan-item floorplan-bed-bath hidden-xs hidden-sm']")#?B?B
		homes_size = response.xpath("//div[@class='floorplan-item floorplan-sqft hidden-xs hidden-sm']")#sqft
		res = ""
		for style,price,size in itertools.zip_longest(homes_style,homes_price,homes_size):
			#round_num+-1
			data_style = ""
			data_price = ""
			data_size = ""
			if style != None:
				data_style =  (style.xpath(".//text()").extract())[0]
			if price != None:
				data_price =  (price.xpath(".//text()").extract())[0]
			if size != None:
				data_size =  (size.xpath(".//text()").extract())[0].replace('\xa0',"")
			res =res + data_style+" @ "+data_price+ " @ "+data_size +" | "
		item['house_plan']  = res
		#parking_info = response.xpath("//div[@class='amenity-grid clearfix']")
		#parking_info = response.xpath("//div[@class='amenity-group-content']")
		block_info = response.xpath("//div[@class='amenity-group']")
		for data in (block_info):
			name = data.xpath(".//h3/text()").extract()
			#content = data.xpath(".//div[@class='amenity-group-content']/text()").extract()
			content= data.xpath(".//span[@class='sprite-text']/text()").extract()
			name = str(name).replace(":']","")
			name = str(name).replace("['","")	
			item[name] = content

		yield item		
	 	
