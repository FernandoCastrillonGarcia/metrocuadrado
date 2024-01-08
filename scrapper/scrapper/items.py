# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join


class InmuebleItem(Item):
    # String Fields
    id = Field(output_processor = TakeFirst())
    comments = Field(input_processor = MapCompose(lambda x: x.replace('\n','')),
                     output_processor = TakeFirst())
    propertyType = Field(output_processor = TakeFirst())
    url = Field(input_processor = MapCompose(lambda x: 'https://www.metrocuadrado.com'+ x),
                output_processor = TakeFirst())
    rentType = Field(output_processor = TakeFirst())

    # Numeric Fields
    builtArea = Field(output_processor = TakeFirst())
    area = Field(output_processor = TakeFirst())
    bathroomsNumber = Field(output_processor = TakeFirst())
    roomsNumber = Field(output_processor = TakeFirst())
    parkingNumber = Field(output_processor = TakeFirst())
    price = Field(output_processor = TakeFirst())

    rentPrice = Field(output_processor = TakeFirst())
    salePrice = Field(output_processor = TakeFirst())

    stratum = Field(output_processor = TakeFirst())
    lat = Field(output_processor = TakeFirst())
    lon = Field(output_processor = TakeFirst())

