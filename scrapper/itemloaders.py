from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, Compose

class PropertyLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = Compose()
    businessType_in = Compose(lambda x: x.capitalize())
    url_in = Compose(lambda x: 'https://www.metrocuadrado.com'+ x)
    comments_in = Compose(lambda x: x.replace('\n',''))

class OfferorLoader(ItemLoader):
    default_output_processor = TakeFirst()