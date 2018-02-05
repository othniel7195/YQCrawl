# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YqBookListItem(scrapy.Item):

    book_id = scrapy.Field()
    book_name = scrapy.Field()
    book_link = scrapy.Field()
    book_author = scrapy.Field()
    book_status = scrapy.Field()
    # 书籍封面
    book_image_url = scrapy.Field()


class YqBookDetailItem(scrapy.Item):

    book_id = scrapy.Field()
    # 标签
    book_label = scrapy.Field()
    # 总点击量
    book_all_click = scrapy.Field()
    # 月点击量
    book_month_click = scrapy.Field()
    # 周点击量
    book_week_click = scrapy.Field()





