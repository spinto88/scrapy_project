# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class NewspapersPipeline(object):

    def __init__(self):
        self.setupDBCon()
 
    def setupDBCon(self):
        self.con = sqlite3.connect('data.db')
        self.cursor = self.con.cursor()
 
    def createTable(self, item):

        self.cursor.execute("create table if not exists {} \n(id int primary key, \ndate date /* Fecha */, \ntime time /* Hora de publicación */, \nprefix text /* Volanta */, \ntitle text /* Título de la nota */, \nsubtitle text /* Subtítulo o copete */, \nsection text /* Sección */, \nauthor text /* Autor de la nota */, \nnewspaper text /* Diario o portal de noticias */, \nbody text /* Cuerpo de la nota */, \ntag text /* Etiqueta propuesta por el periódico */, \nurl text /* Página web */);".format(item['newspaper']))

    def maxId(self, item):
        try:
            self.cursor.execute("select MAX(id) from {};".format(item['newspaper']))
            for i in self.cursor:
                id_note = i[0] + 1
        except:
            id_note = 0

        return id_note

    def process_item(self, item, spider):

        self.createTable(item)
        item['id_note'] = self.maxId(item)

        self.cursor.execute('insert into {} (id, date, time, prefix, \
                                             title, subtitle, section, \
                                             author, newspaper, body, \
                                             tag, url) values \
                                             ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
                                             .format(item['newspaper']),\
                                             [item['id_note'], item['date'], item['time'], item['prefix'], \
                                             item['title'], item['subtitle'], item['section'],\
                                             item['author'], item['newspaper'], item['body'],\
                                             item['tag'], item['url']])
        self.con.commit()
        return item

    def closeDB(self):
        self.con.close()
 
    def __del__(self):
        self.closeDB()

