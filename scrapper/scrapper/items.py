# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Inmueble(Item):
    title = Field()
    covered_surface = Field()
    rooms = Field()
    bathrooms = Field()
    estrato = Field()
