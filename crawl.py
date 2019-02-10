
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
	name = "crawl"
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
				if self.clock < 10000 or True:
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
	file_count = 1
	def parse_data(self,response):
		url = str(response.url)
		filename = "./data_2019/"+str(self.file_count) + ".html"
		self.file_count +=1
		print ("response:",response.body)
		text = str(response.body)
		open(filename, 'w').write(text)
		#body = response.body
		#yield item		
	 	
