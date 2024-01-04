# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import Compose, TakeFirst, Join

def parse_features(features_list):
    return {temp.split(':')[0]: temp.split(':')[1] for temp in features_list}
    
class InmuebleItem(Item):
    id = Field()
    builtArea = Field()
    area = Field()
    
    bathroomsNumber = Field()
    roomsNumber = Field()
    parkingNumber = Field()

    adminPrice = Field()
    price = Field()
    rentPrice = Field()
    salePrice = Field()


    forSale = Field()
    forRent = Field()
    

    status = Field()
    stratum = Field()
    comments = Field()

    lat = Field()
    lon = Field()
    propertyType = Field()

