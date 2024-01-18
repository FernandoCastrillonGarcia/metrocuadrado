# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from .items import PropertyItem, OfferorItem
import dataclasses

class DuplicatesPipeline:
    def __init__(self):
        self.id_propertys_seen = set()
        self.id_offerors_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, PropertyItem):
            adapter = ItemAdapter(item)
            if adapter['id_property'] in self.id_propertys_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.id_propertys_seen.add(adapter['id_property'])
                return item
        elif isinstance(item, OfferorItem):
            adapter = ItemAdapter(item)
            if adapter['id_offeror'] in self.id_offerors_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.id_offerors_seen.add(adapter['id_offeror'])
                return item

# class SavingPipeline(object):
#     def process_item(self, item, spider):
#         filename = None
#         if isinstance(item, OfferorItem):
#             item = dataclasses.asdict(item)
#             fields = list(item.keys())
#             filename = 'offeror.csv'
#             with open(filename, 'a', encoding='utf-8') as f:
#                 writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
#                 writer.writerow(item)
#         elif isinstance(item, PropertyItem):
#             item = dataclasses.asdict(item)
#             filename = 'propery.csv'
#             fields = list(item.keys())
#             with open(filename, 'a', encoding='utf-8') as f:
#                 writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
#                 writer.writerow(item)
#         return item

class StoreOfferorPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
    
    def create_table(self):
        table_query = """
        CREATE TABLE IF NOT EXISTS Offerors (
            id_offeror TEXT PRIMARY KEY,
            url TEXT,
            address TEXT,
            name TEXT,
            type TEXT,
            offerorType TEXT
        )
        """
        self.cur.execute(table_query)
    
    def store_db(self, item):
        item = dataclasses.asdict(item)
        query = """
        INSERT INTO Offerors VALUES 
        (?, ?, ?, ?, ?, ?)"""
        values = (
            item['id_offeror'],
            item['url'],
            item['address'],
            item['name'],
            item['type'],
            item['offerorType']
        )
        self.cur.execute(query, values)
        self.con.commit()
    
    def process_item(self, item, spider):
        if isinstance(item, OfferorItem):
            self.store_db(item)
            return item
        else:
            return item

class StorePropertyPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
    
    def create_table(self):
        table_query = """
        CREATE TABLE IF NOT EXISTS Properties (
            id_property TEXT PRIMARY KEY,
            id_offeror TEXT,
            businessType TEXT,
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
        item = dataclasses.asdict(item)
        query = """
        INSERT INTO Properties VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            item['id_property'],
            item['id_offeror'],
            item['businessType'],
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
        if isinstance(item, PropertyItem):
            self.store_db(item)
            return item
        else:
            return item

class CheckInTable:
    def __init__(self):
        self.create_connection()
    
    def create_connection(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
    
    def process_item(self, item, spider):
        if isinstance(item, PropertyItem):
            item = dataclasses.asdict(item)
            values = (
                item['id_property'],
                item['id_offeror'],
                item['businessType'],
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
            table = 'Properties'
            
        elif isinstance(item, OfferorItem):
            item = dataclasses.asdict(item)
            values = (
                item['id_offeror'],
                item['url'],
                item['address'],
                item['name'],
                item['type'],
                item['offerorType']
            )
            table = 'Offerors'

        self.cur.execute(f"SELECT * FROM {table}")
        existing_rows = set(self.cur.fetchall())

        if values in existing_rows:
            return item
        else:
            query_val = '('+', '.join(['?']*len(values))+')'
            self.cur.execute(f"INSERT INTO {table} VALUES {query_val}", values)

            # Commit the changes to the database
            self.con.commit()
            return item