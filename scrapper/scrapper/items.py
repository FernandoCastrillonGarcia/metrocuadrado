# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import Compose, TakeFirst

def parse_features(features_list):
            return {temp.split(':')[0]: temp.split(':')[1] for temp in features_list}
    
class InmuebleItem(Item):
    coords = Field()
    comentarios = Field()
    features = Field(
        input_processor = Compose(parse_features),
        output_processor = TakeFirst()
        )
