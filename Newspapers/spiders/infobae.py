# -*- coding: utf-8 -*-
import scrapy
import datetime
from Newspapers.items import NewspapersItem

init_date = "2018-06-11"
final_date = "2018-06-18"

init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()

name2month = {'enero': 1, 'febrero': 2, 'marzo': 3,\
              'abril': 4, 'mayo': 5, 'junio': 6,\
              'julio': 7, 'agosto': 8, 'septiembre': 9,\
              'octubre': 10, 'noviembre': 11, 'diciembre': 12}

class InfobaeSpider(scrapy.Spider):
    name = "infobae"

    def start_requests(self):

        links = []
 	for section in ['politica', 'sociedad', 'economia']:

            links += open('Newspapers/spiders/links/Infobae_links_{}.txt'.format(section), 'r').\
                                                      read().split('\n')
        for link in set(links):
            yield scrapy.Request(url = 'http://www.infobae.com' + link, callback = self.parse, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        try:
            title = response.selector.xpath('//header[@class = "article-header hed-first col-sm-12"]/h1/text()')[0].extract()
        except:
            title = ''

        try:
            subtitle = response.selector.xpath('//span[@class = "subheadline"]/text()')[0].extract()
        except:
            subtitle = ''

        try:
            body = response.selector.xpath('//p[@class = "element element-paragraph"]//text()').extract()
            body = ' '.join(body)
        except:
            body = ''

        try:
            date = response.selector.xpath('//*[@class = "byline-date"]//text()')[0].extract()
            date = date.split()
            date = "{}-{}-{}".format(date[4], name2month[date[2]], date[0])

            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date < init_date or date >= final_date:
                return None
            else:
                pass
        except:
            date = ''

        try:
            author = response.selector.xpath('//div[@class = "byline-author"]//b//text()')[0].extract()
        except:
            author = ''

        try:
            section = response.selector.xpath('//header[@class = "article-header hed-first col-sm-12"]//a/text()')[0].extract()
        except:
            section = ''
        
        item = NewspapersItem()
        item['title'] = title
        item['subtitle'] = subtitle
	item['section'] = section
        item['author'] = author
        item['date'] = date
        item['newspaper'] = u'infobae'
	item['url'] = response.url
        item['body'] = body

        item['prefix'] = None
        item['tag'] = None
        item['time'] = None

        return item
