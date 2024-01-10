from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

def ChangeNone(x):
    if x is None:
        return 'xd'
    else:
        return x

class PropertyLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(ChangeNone)
    businessType_in = MapCompose(lambda x: x.capitalize())
    url_in = MapCompose(lambda x: 'https://www.metrocuadrado.com'+ x, ChangeNone)
    comments_in = MapCompose(lambda x: x.replace('\n',''), ChangeNone)

class OfferorLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = ChangeNone