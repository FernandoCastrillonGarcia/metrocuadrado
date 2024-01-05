# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

class InmueblePipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = sqlite3.connect('results/database.db')
        self.cur = self.con.cursor()
    
    def create_table(self):
        table_query = """
        CREATE TABLE IF NOT EXISTS inmuebles (
            id TEXT,
            forSale TEXT,
            forRent TEXT,
            comments TEXT,
            status TEXT,
            propertyType TEXT,
            builtArea REAL,
            area REAL,
            bathroomsNumber INTEGER,
            roomsNumber INTEGER,
            parkingNumber INTEGER,
            adminPrice REAL,
            price REAL,
            rentPrice REAL,
            salePrice REAL,
            stratum INTEGER,
            lat REAL,
            lon REAL
        )
        """
        self.cur.execute(table_query)
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        query = """INSERT INTO inmuebles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            item['id'],
            item['forSale'],
            item['forRent'],
            item['comments'],
            item['status'],
            item['propertyType'],
            item['builtArea'],
            item['area'],
            item['bathroomsNumber'],
            item['roomsNumber'],
            item['parkingNumber'],
            item['adminPrice'],
            item['price'],
            item['rentPrice'],
            item['salePrice'],
            item['stratum'],
            item['lat'],
            item['lon']
        )
        self.cur.execute(query, values)
        self.con.commit()