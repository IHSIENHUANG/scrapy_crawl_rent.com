# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
#from datablogger_scraper.items import DatabloggerScraperItem
from myCrawl.items import FirstDemoItem


class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "datablogger"
    num =0
    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["rent.com"]

    # The URLs to start with
    start_urls = ["https://www.rent.com/california/riverside-apartments/"]

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        print("OMGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        for url in self.start_urls :
            if self.num <100:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse_items(self, response):
        # The list of items that are found on the particular page
        self.num +=1
        print(self.num)
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            #print(link)
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    #print(allowed_domain)
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed and self.num<100:
                if self.start_urls[0]  in response.url:
                    item = FirstDemoItem()
                    item['url_from'] = response.url
                    print(response.url)
                    item['url_to'] = link.url
                    items.append(item)
                    print(link.url)
        # Return all the found items
        #yield items
        return items
