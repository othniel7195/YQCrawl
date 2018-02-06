# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.crawler import Crawler
import pymongo
from YQCrawl.items import YqBookDetailItem
from YQCrawl.items import YqBookListItem
import re


class YqcrawlPipeline(object):


    """
    如果用的是MongoDB集群
    def __init__(self, mongo_url, mongo_db, replicaset):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.replicaset = replicaset
    """
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        如果用MongoDB集群
         return cls(mongo_url=crawler.settings.get("MONGO_URI"),
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'yunqi'),
                   replicaset=crawler.settings.get("REPLICASET"))
        :type crawler: Crawler
        :return: 
        """
        return cls(mongo_url=crawler.settings.get("MONGO_URI"),
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'yunqi'))

    def open_spider(self, spider):
        """
        如果用MongoDB集群
        self.client = pymongo.MongoClient(self.mongo_url, replicaset=self.replicaset)
        :param spider: 
        :return: 
        """
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        print "mongodb :%s " % self.db.last_status()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if isinstance(item, YqBookListItem):
            self._process_book_list_item(item)
        elif isinstance(item, YqBookDetailItem):
            self._process_book_detail_item(item)
        else:
            pass
        return item

    def _process_book_list_item(self, item):
        self.db["bookinfo"].insert(dict(item))

    def _process_book_detail_item(self, item):
        item["book_label"] = item["book_label"].strip().replace('\n', '')
        pattern = re.compile("\d+")
        item["book_all_click"] = pattern.findall(item["book_all_click"])
        item["book_month_click"] = pattern.findall(item["book_month_click"])
        item["book_week_click"] = pattern.findall(item["book_week_click"])

        self.db["bookhot"].insert(dict(item))

