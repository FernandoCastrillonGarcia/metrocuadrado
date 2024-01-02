# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class InmueblePipeline:
    def __init__(self):
        self.con = sqlite3.connect('results.db')
        self.cur = self.con.cursor()
        self.create_table()
    
    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS inmuebles(id TEXT PRIMARY KEY,roomsNumber TEXT,adminPrice TEXT,price TEXT,checked TEXT,area TEXT,forSale TEXT,forRent TEXT,status TEXT,rentPrice TEXT,comentsisPublished TEXT,coments TEXT,salePrice TEXT,metroId TEXT,isPublished TEXT,url TEXT,stratum TEXT,bathroomsNumber TEXT,builtArea TEXT,parkingNumber TEXT,offerorType TEXT)""")
    
    
    
    def process_item(self, item, spider):
        self.cur.execute("""
                         INSERT OR IGNORE INTO inmuebles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                         """,
                         (
                         item['roomsNumber'], item['adminPrice'], item['price'], item['checked'],
                         item['id'], item['area'], item['forSale'], item['forRent'], item['status'],
                         item['rentPrice'], item['salePrice'], item['metroId'], item['comentsisPublished'],
                         item['url'], item['stratum'], item['bathroomsNumber'], item['builtArea'],
                         item['parkingNumber'], item['offerorType'], item['comentsisPublished']))
        self.con.commit()
        return item
