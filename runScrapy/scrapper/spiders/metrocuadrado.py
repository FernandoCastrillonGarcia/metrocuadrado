from scrapy.spiders import Spider
import scrapy
import json
from ..items import PropertyItem, OfferorItem
from ..itemloaders import OfferorLoader, PropertyLoader
import requests
from tqdm import tqdm
from .save_dicts import CUSTOM_SETTINGS, HEADERS, PAYLOAD

class MetroCuadradoSpider(Spider):

    # This counter will show use our requirments
    conteo = 0
    name = 'MetroCuadrado'
    start_urls = ["https://www.metrocuadrado.com"]
    allowed_domains = ['metrocuadrado.com']
    custom_settings = CUSTOM_SETTINGS

    # Prerequistes for Api Requests
    url_api = "https://commons-api.metrocuadrado.com/v1/api/commons/queries"
    headers = HEADERS
    payload = PAYLOAD
    
    def get_lists(self):
        """
        Method for getting the pagination list for the scrapper to do the requests
        """
        response = requests.request("POST", self.url_api, headers=self.headers, data=json.dumps(self.payload))
        r_json = json.loads(response.text)
        batch = r_json['data']['result']['propertiesByFiltersQuery']['batch']
        realEstate_pages = batch['realEstate']['pages']
        seller_pages = batch['seller']['pages']

        return realEstate_pages, seller_pages

    def parse(self, response):

        realEstate_pages, seller_pages = self.get_lists()
        
        for r, s in tqdm(zip(realEstate_pages, seller_pages)):
            
            # Modify Payload to change the request's response
            self.payload['queries'][0]['batch']['realEstate']['from'] = r
            self.payload['queries'][0]['batch']['seller']['from'] = s

            payload = json.dumps(self.payload)

            yield scrapy.Request(url = self.url_api,
                                method = 'POST',
                                headers=self.headers,
                                body=payload,
                                callback = self.parse_api)
            
    def parse_api(self, response):
        
        raw_data = json.loads(response.body)
        data = raw_data['data']['result']['propertiesByFiltersQuery']['properties']

        for property in data:
            loader = PropertyLoader(item=PropertyItem())
            lines = [
                "# LOAD KEYS",
                "loader.add_value('id_property', property['id'])",
                "loader.add_value('id_offeror', property['offeror']['id'])",
                "# LOAD NUMERIC",
                "loader.add_value('builtArea', property['builtArea'])",
                "loader.add_value('area', property['area'])",
                "loader.add_value('bathroomsNumber', property['bathroomsNumber'])",
                "loader.add_value('roomsNumber', property['roomsNumber'])",
                "loader.add_value('parkingNumber', property['parkingNumber'])",
                "loader.add_value('stratum', property['stratum'])",
                "loader.add_value('price', property['price'])",
                "loader.add_value('lon', property['location']['lon'])",
                "loader.add_value('lat', property['location']['lat'])",
                "# LOAD STRING",
                "loader.add_value('propertyType', property['propertyType']['label'])",
                "loader.add_value('businessType', property['businessType']['label'])",
                "loader.add_value('url', property['url'])",
                "loader.add_value('comments', property['comments'])"
            ]
            for line in lines:
                try:
                    exec(line)
                except:
                    new_line = line.split(',')
                    new_line[1] = 'None)'
                    exec(', '.join(new_line))
            # YIELD PROPERTY
            yield loader.load_item()
            # ------------------------------------------------------------------#
            loader = OfferorLoader(item=OfferorItem())
            lines = [
                "# LOAD KEYS",
                "loader.add_value('id_offeror', property['offeror']['id'])",
                "# LOAD STRING",
                "loader.add_value('url', property['offeror']['webSite'])",
                "loader.add_value('address', property['offeror']['address'])",
                "loader.add_value('name', property['offeror']['name'])",
                "loader.add_value('type', property['offeror']['type'])",
                "loader.add_value('offerorType', property['offerorType'])",
            ]
            for line in lines:
                try:
                    exec(line)
                except:
                    new_line = line.split(',')
                    new_line[1] = 'None)'
                    exec(', '.join(new_line))
            yield loader.load_item()