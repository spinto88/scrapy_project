# -*- coding: utf-8 -*-
import scrapy
import datetime
from Newspapers.items import NewspapersItem

init_date = "2018-06-11"
final_date = "2018-06-18"

init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()

class ClarinSpider(scrapy.Spider):
    name = "clarin"

    def start_requests(self):
       
	links = open('Newspapers/spiders/links/Clarin_links.txt','r').read().split('\n')
        for link in set(links):
            yield scrapy.Request(url = 'http://www.clarin.com' + link, callback = self.parse, meta = {'dont_merge_cookies': True})
	
    def parse(self, response):

        try:
            title = response.selector.xpath('//*[@id = "title"]/text()')[0].extract()
        except:
            title = ''

        try:
            subtitle = response.selector.xpath('//*[@itemprop = "description"]//text()')[0].extract()
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//*[@class = "body-nota"]//text()').extract()
	    body = ' '.join(body)
        except:
            body = ''

        try:
            prefix = response.selector.xpath('//*[@class = "volanta"]/text()')[0].extract()
        except:
            prefix = ''
       
        try:
            date_time = response.selector.xpath('//*[@itemprop = "datePublished"]//@content')[0].extract()
            date = date_time.split(' ')[0] 
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date < init_date or date >= final_date:
                return None
            else:
                pass
        except:
            date = ''

        try:
            date_time = response.selector.xpath('//*[@itemprop = "datePublished"]//@content')[0].extract()
            time = date_time.split(' ')[1]
        except:
            time = ''

        try:
            author = response.selector.xpath('//*[@itemprop = "author"]/text()')[0].extract()
        except:
            author = ''

        try:
            section = response.selector.xpath('//*[@class = "header-section-name"]/text()')[0].extract()
        except:
            section = ''

        try:
            tag = response.selector.xpath('//*[@itemprop = "keywords"]//text()').extract()
            tag = ', '.join(tag)
        except:
            tag = ''
        
        item = NewspapersItem()
        item['title'] = title
        item['subtitle'] = subtitle
	item['prefix'] = prefix
	item['section'] = section
        item['author'] = author
        item['date'] = date
        item['time'] = time
        item['newspaper'] = u'clarin'
	item['url'] = response.url
        item['body'] = body
        item['tag'] = tag

        return item


