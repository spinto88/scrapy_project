# -*- coding: utf-8 -*-

import scrapy
import datetime
from Newspapers.items import NewspapersItem

init_date = "2018-01-01"
final_date = "2018-06-11"

init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()

name2month = {'enero': 1, 'febrero': 2, 'marzo': 3,\
              'abril': 4, 'mayo': 5, 'junio': 6,\
              'julio': 7, 'agosto': 8, 'septiembre': 9,\
              'octubre': 10, 'noviembre': 11, 'diciembre': 12}


# Ids de las notas tentativas: dentro de esta ventana solo se queda con las notas cuya fecha esta dentro dentro del intervalo de tiempo indicado
# Ver en la pagina...

init_id = 2090000
final_id = 2143146

class LaNacionSpider(scrapy.Spider):
    name = "lanacion"

    def start_requests(self):
        urls = []
        for i in range(init_id, final_id):
            urls.append('http://www.lanacion.com.ar/' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta = {'dont_merge_cookies': True})

    def parse(self, response):

        url = response.url

        try:
            date = response.selector.xpath('//section[@class = "fecha"]//text()')[0].extract()	
            date = date.split()
            date = "{}-{}-{}".format(date[4], name2month[date[2]], date[0]) 
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date < init_date or date >= final_date:
                return None
            else:
                pass
            
        except:
            date = ''
            time = ''

        try:
            title = response.selector.xpath('//article//*[@class = "titulo"]//text()')[0].extract()
        except:
            title = ''

        try:
            body = response.selector.xpath('//section[@id = "cuerpo"]//p//text()').extract()
            body = ' '.join(body)
            body = body.replace('\r', '')
            body = body.replace('\n', '')

        except:
            body = ''

        try:
            section = response.selector.xpath('//*[@class = "categoria"]//a//text()')[0].extract()
            section = section.replace(' ', '')
            section = section.replace('\r', '')
            section = section.replace('\n', '')
        except:
            section = ''

        try:
            tag = response.selector.xpath('//*[@class = "tag"]//a//text()')[0].extract()
            tag = tag.replace(' ', '')
            tag = tag.replace('\r', '')
            tag = tag.replace('\n', '')
        except:
            tag = ''

        try:
            author = response.selector.xpath('//section[@class = "autor"]//a//text()')[0].extract()
        except:
            author = ''

        item = NewspapersItem()
        item['title'] = title
        item['date'] = date
        item['author'] = author
        item['url'] = url
        item['newspaper'] = u'lanacion'
        item['section'] = section
        item['tag'] = tag
        item['body'] = body

        item['time'] = None
        item['subtitle'] = None
        item['prefix'] = None

        return item
