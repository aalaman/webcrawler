import scrapy
from scrapy import signals
import os
import re
import sys
import pymongo
import logging
import threading

logger = logging.getLogger('webcrawler.log')
logger.handlers = []
fh = logging.FileHandler('/tmp/webcrawler.log')
fh.setLevel(logging.DEBUG)

# creating a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add to logger
logger.addHandler(fh)

class webCrawlerSpider(scrapy.Spider):

    name = 'webcrawler'


    # connection to mongodb, could have perhaps used pipelines
    def dbconnection(self):

        listing = []

        mclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mdb = mclient["spiderdata"]

        mcol = mdb["data"]

        result = list(mcol.aggregate([{ "$group": { "_id": "$url", "url" : { "$addToSet" : "$url" }, "regex" : { "$addToSet" : "$regex" }}}]))

        return result

    # start the show
    def start_requests(self):

        urls = self.dbconnection()

        for url in urls:

            addr = url['url'][0]

            for i in range(len(url['regex'])):

                meta = {'regexp' : url['regex'][i]}

                yield scrapy.Request(url=addr, meta=meta, callback=self.parse, dont_filter=True)

    # the parser
    def parse(self, response):

        regexp = response.request.meta['regexp']

        url = response.request.url

        for string in response.xpath('//text()').re(regexp):

            logger.info( '['+url+'] Found string '+string)

            yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        spider = super(webCrawlerSpider, cls).from_crawler(crawler, *args, **kwargs)

        return spider

