# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import Compose, TakeFirst, Join

def parse_features(features_list):
    return {temp.split(':')[0]: temp.split(':')[1] for temp in features_list}
    
class InmuebleItem(Item):
    # String Fields
    id = Field(output_processor = TakeFirst())
    forSale = Field(output_processor = TakeFirst())
    forRent = Field(output_processor = TakeFirst())
    comments = Field(output_processor = TakeFirst())
    status = Field(output_processor = TakeFirst())
    propertyType = Field(output_processor = TakeFirst())

    # Numeric Fields
    builtArea = Field(output_processor = TakeFirst())
    area = Field(output_processor = TakeFirst())
    bathroomsNumber = Field(output_processor = TakeFirst())
    roomsNumber = Field(output_processor = TakeFirst())
    parkingNumber = Field(output_processor = TakeFirst())
    adminPrice = Field(output_processor = TakeFirst())
    price = Field(output_processor = TakeFirst())
    rentPrice = Field(output_processor = TakeFirst())
    salePrice = Field(output_processor = TakeFirst())
    stratum = Field(output_processor = TakeFirst())
    lat = Field(output_processor = TakeFirst())
    lon = Field(output_processor = TakeFirst())

