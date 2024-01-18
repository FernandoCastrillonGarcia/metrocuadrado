# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PropertyItem:
    # KEYS
    id_property: Optional[str] = field(default=None)
    id_offeror: Optional[str] = field(default=None)
    
    # NUMERIC FIELDS
    builtArea: Optional[float] = field(default=None)
    area: Optional[float] = field(default=None)
    bathroomsNumber: Optional[int] = field(default=None)
    roomsNumber: Optional[int] = field(default=None)
    parkingNumber: Optional[int] = field(default=None)
    stratum: Optional[int] = field(default=None)
    price: Optional[int] = field(default=None)
    lat: Optional[float] = field(default=None)
    lon: Optional[float] = field(default=None)

    # STRING FIELDS
    businessType: Optional[str] = field(default=None)
    propertyType: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    comments: Optional[str] = field(default=None)

#-------------------------------------------------------------------------------------#
@dataclass
class OfferorItem:
    # KEYS
    id_offeror: Optional[str]= field(default=None)

    # STRING FIELD
    url: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    offerorType: Optional[str] = field(default=None)