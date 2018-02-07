# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.response import Response
from parsel.selector import SelectorList
from YQCrawl.items import YqBookListItem
from YQCrawl.items import YqBookDetailItem


class YunqiQqComSpider(CrawlSpider):
    name = 'yunqi.qq.com'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n10p1']

    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n10p\d+'), callback='parse_book_list', follow=True),
    )


    def parse_book_list(self, response):
        """
        :type response: Response 
        :return: 
        """
        books = response.xpath("//div[@class='book']")  # type: list[SelectorList]

        for book in books:

            book_image_url = book.xpath("./a/img/@src").extract_first()
            print "book_url: %s" % book_image_url
            book_name = book.xpath("./div[@class='book_info']/h3/a/text()").extract_first()
            print "book_name: %s" % book_name
            book_id = book.xpath("./div[@class='book_info']/h3/a/@id").extract_first()
            print "book_id: %s" % book_id
            book_link = book.xpath("./div[@class='book_info']/h3/a/@href").extract_first()
            print "book_link: %s" % book_link
            book_infos = book.xpath("./div[@class='book_info']/dl/dd[@class='w_auth']") # type: list

            if len(book_infos) > 2:
                book_author = book_infos[0].xpath("./a/text()").extract_first()
                print "book_author: %s" % book_author
                book_status = book_infos[2].xpath("./text()").extract_first()
                print "book_status: %s" % book_status
            else:
                book_author = ""
                book_status = ""

            book_list_item = YqBookListItem(book_image_url=book_image_url, book_name=book_name, book_id=book_id,
                                            book_link=book_link, book_author=book_author, book_status=book_status)
            yield book_list_item

            request = scrapy.Request(url=book_link, callback=self.parse_book_detail)
            request.meta["book_id"] = book_id
            yield request

    def parse_book_detail(self, response):
        """
        :type response: Response
        :return: 
        """
        book_id = response.meta["book_id"]
        book_label = response.xpath("//div[@class='tags']/text()").extract_first()
        print "book_label: %s" % book_label
        book_all_click = response.xpath("//*[@id ='novelInfo']/table/tr[2]/td[1]/text()").extract_first()
        print "book_all_click: %s" % book_all_click
        book_month_click = response.xpath("//*[@id ='novelInfo']/table/tr[3]/td[1]/text()").extract_first()
        print "book_month_click: %s" % book_all_click
        book_week_click = response.xpath("//*[@id ='novelInfo']/table/tr[4]/td[1]/text()").extract_first()
        print "book_week_click :%s" % book_week_click
        book_detail_item = YqBookDetailItem(book_id=book_id, book_label=book_label, book_all_click=book_all_click,
                                            book_week_click=book_week_click, book_month_click=book_month_click)
        yield book_detail_item


















