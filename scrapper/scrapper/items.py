# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import Compose, TakeFirst, Join

def parse_features(features_list):
    return {temp.split(':')[0]: temp.split(':')[1] for temp in features_list}
    
class InmuebleItem(Item):
    adminPrice = Field()
    roomsNumber = Field()
    price = Field()
    checked = Field()
    id = Field()
    area = Field()
    forSale = Field()
    forRent = Field()
    status = Field()
    rentPrice = Field()
    coments = Field()
    salePrice = Field()
    metroId = Field()
    isPublished = Field()
    url = Field()
    stratum = Field()
    bathroomsNumber = Field()
    builtArea = Field()
    parkingNumber = Field()
    offerorType = Field()
    
    # features = Field(
    #     input_processor = Compose(parse_features),
    #     output_processor = TakeFirst()
    #     )
