# -*- coding: utf-8 -*-
#from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from myCrawl.items import FirstDemoItem 
import scrapy
import re
import pandas as pd
from time import sleep
class BaiduSpider(CrawlSpider):
	name = "rent"
	allowed_domains = ["rent.com"]
	df = pd.read_csv("state_city.csv")
	urls = []
	for col in df.columns:
		datas = df[col]
		for data in datas:
			data = str(data).replace(" ","-")
			col = str(col).replace(" ","-")	
			url = 'https://www.rent.com/'+str(col)+'/'+str(data)+'/apartments_condos_houses_townhouses?page=2'
			urls.append(url)
	all_cities = urls
	start_urls = ['https://www.rent.com/Colorado/Wheat-Ridge/apartments_condos_houses_townhouses?page=2']
	rules = [Rule(LinkExtractor(
				#allow=(r'\/california/riverside-apartments\?page[2-9]'),
				canonicalize=True,
 				unique=True),
			follow=True,
			callback="parse"
			)
			]
	'''	
	rules = [
		#将所有符合正则表达式的url加入到抓取列表中
		#Rule(LinkExtractor(allow = (r'http://www\.rent\.com/california/riverside-apartments/.+'))),
		#将所有符合正则表达式的url请求后下载网页代码, 形成response后调用自定义回调函数
		Rule(LinkExtractor(allow = (r'\?page=[2-9]',)) ,callback = 'parse',follow=True)
		]
	'''
	seen_urls = set()	
	page =1
	clock = 0
	def parse_city(self,response):
		#print ("parse city url is ",response.url)
		
		links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
		flag = False
		for link in links:
			obj = re.match(r'https://www\.rent\.com/.+/.*/.+[0-9]$',link.url,re.M|re.I)
			review = re.match(r'https://www\.rent\.com/california/riverside-apartments/.+review.+',link.url,re.M|re.I)	# review should not in link
			if obj and "reviews" not in link.url and '/tel' not in link.url and "page" not in link.url and link.url not in self.seen_urls:
				self.clock+=1
				#print(self.clock)
				if self.clock <100000:
					print(self.clock,link.url)
					flag = True
					self.seen_urls.add(link.url)
					yield scrapy.Request(link.url,callback=self.parse_data,dont_filter=True)
		next_url = response.url.split("=")
		next_url,page = next_url[0],next_url[1]
		next_url = next_url +"="+str(int(page)+1)	
		print ("next url",next_url)	
		if flag and int(page) <70:
			yield scrapy.Request(next_url,callback=self.parse_city,dont_filter=True)
			#print (len(dic_url))

	def parse(self,response):
		for url in  self.urls:
			yield scrapy.Request(url,callback=self.parse_city,dont_filter=True)
		'''
		links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
		flag = False
		for link in links:
			obj = re.match(r'https://www\.rent\.com/[a-zA-z\-]+/.*/.+[0-9]$',link.url,re.M|re.I)
			review = re.match(r'https://www\.rent\.com/california/riverside-apartments/.+review.+',link.url,re.M|re.I)	# review should not in link
			if obj and "reviews" not in link.url :
				#self.clock+=1
				flag = True
				#print(self.clock)
				if self.clock <10000 and '/tel' not in link.url and link.url not in self.seen_urls:
					print(self.clock,link.url)
					self.seen_urls.add(link.url)
					yield scrapy.Request(link.url,callback=self.parse_data,dont_filter=True)
		next_url = response.url.split("=")
		next_url,page = next_url[0],next_url[1]
		next_url = next_url +"="+str(int(page)+1)	
		print ("next url",next_url)	
		if flag and page <100:
			yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
			#print (len(dic_url))
		'''
	def parse_data(self,response):
		#print("start process data)",response.url) 
		#if self.clock%1000==0:
		#	sleep(1)
		print (response.url)	
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
			#print("round:", round_num)
			#round_num +=1		
			#item['phone'] = div.xpath(".//span[@class='pdp-heading-meta-phone hidden-xs']/a/@href").extract()
			item['price'] = div.xpath(".//span[@class='pdp-heading-meta-rent bold']/text()").extract()    
			item['beds']  = div.xpath(".//span[@class='pdp-heading-meta-beds']/text()").extract()   
			item['pet'] = div.xpath(".//span[@class='pdp-heading-meta-pets']/text()").extract()    
		homes_price = response.xpath("//div[@class='floorplan-item floorplan-rent hidden-xs hidden-sm']")#homes_price
		homes_style = response.xpath("//div[@class='floorplan-item floorplan-bed-bath hidden-xs hidden-sm']")#?B?B
		homes_size = response.xpath("//div[@class='floorplan-item floorplan-sqft hidden-xs hidden-sm']")#sqft
		res = ""
		for style,price,size in zip(homes_style,homes_price,homes_size):
			#round_num+-1
			data_style =  (style.xpath(".//text()").extract())[0]
			data_price =  (price.xpath(".//text()").extract())[0]
			data_size =  (size.xpath(".//text()").extract())[0].replace('\xa0',"")
			res =res + data_style+" "+data_price+ " "+data_size +" | "
		item['house_plan']  = res
		#parking_info = response.xpath("//div[@class='amenity-grid clearfix']")
		parking_info = response.xpath("//div[@class='amenity-group-content']")
		#amenity-group-content
		block_info = response.xpath("//div[@class='amenity-group']")
		print ("start testing")
		attribute = [] # stroe the list of attribute like pet, part and so on
		for data in (block_info):
			#name = data.xpath(".//div[@class='amenity-group']/test()").extract()
			name = data.xpath(".//h3/text()").extract()
			content = data.xpath(".//div[@class='amenity-group-content']/text()").extract()
			content2 = data.xpath(".//span[@class='sprite-text']/text()").extract()
			print ("@@@@@@@@ ",name,content,content2)
			#print (name)
			attribute.append(name)
		#print ("end testing")	
		print ("start testing")
		for index,park in enumerate(parking_info):
			attribute_name = attribute[index] #if attribute[index][-1] ==":" else attribute[index]
			attribute_name = str(attribute_name).replace(":']","")
			attribute_name = str(attribute_name).replace("['","")
			#print (str(attribute_name))
			item[attribute_name] = park.xpath(".//span[@class='sprite-text']/text()").extract()
			print (attribute_name,item[attribute_name])
			'''
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
			'''
		print ("end testin")
		yield item		
	 	
