# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MycrawlPipeline(object):
	def process_item(self, item, spider):
		#return item
		print(item['title'])
		print(item['streetaddr'])
		print(item['city'])
		print(item['state'])
		print(item['zipcode'])
		print(item['phone'])
		print(item['price'])
		print(item['beds'])
		print(item['pet'])
		print(item['house_plan'])

		print(item['Kitchen'])
		print(item['Laundry'])
		print(item['Parking'])
		print(item['Pets'])
		print(item['Features'])
		print(item['Community'])
