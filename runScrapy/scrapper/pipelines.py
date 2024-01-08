# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class StorePipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = sqlite3.connect('../MapPage/assets/db/database.db')
        self.cur = self.con.cursor()
    
    def create_table(self):
        table_query = """
        CREATE TABLE IF NOT EXISTS inmuebles (
            id TEXT,
            rentType TEXT,
            comments TEXT,
            url TEXT,
            propertyType TEXT,
            builtArea REAL,
            area REAL,
            bathroomsNumber INTEGER,
            roomsNumber INTEGER,
            parkingNumber INTEGER,
            price REAL,
            stratum INTEGER,
            lat REAL,
            lon REAL
        )
        """
        self.cur.execute(table_query)
    
    def store_db(self, item):
        query = """
        INSERT INTO inmuebles VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            item['id'],
            item['rentType'],
            item['comments'],
            item['url'],
            item['propertyType'],
            item['builtArea'],
            item['area'],
            item['bathroomsNumber'],
            item['roomsNumber'],
            item['parkingNumber'],
            item['price'],
            item['stratum'],
            item['lat'],
            item['lon']
        )
        self.cur.execute(query, values)
        self.con.commit()
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item

class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item

class ForRentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter['rentPrice'] == -1:
            adapter['rentType'] = 'Venta'
        else:
            adapter['rentType'] = 'Arriendo'

        del item['rentPrice']
        del item['salePrice']

        return item
