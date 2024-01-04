from scrapy.spiders import Spider
import scrapy
import json
from ..items import InmuebleItem
from itemloaders import ItemLoader
import os
import requests
from tqdm import tqdm

with open('scrapper/dicts/payload.json', 'r') as json_file:
    payload = json.load(json_file)

with open('scrapper/dicts/custom_settings.json', 'r') as json_file:
    custom_settings = json.load(json_file)

with open('scrapper/dicts/headers.json', 'r') as json_file:
    headers = json.load(json_file)

class MetroCuadradoSpider(Spider):

    # This counter will show use our requirments
    conteo = 0
    name = 'MetroCuadrado'
    start_urls = ["https://www.metrocuadrado.com"]
    allowed_domains = ['metrocuadrado.com']
    custom_settings = custom_settings

    # Prerequistes for Api Requests
    url_api = "https://commons-api.metrocuadrado.com/v1/api/commons/queries"
    headers = headers
    payload = payload

    item_keys_string =[
        'id',
        'forSale',
        'forRent',
        'comments',
        'status'
    ]

    item_keys_number = [
        'builtArea',
        'area',
        'bathroomsNumber',
        'roomsNumber',
        'parkingNumber',
        'adminPrice',
        'price',
        'rentPrice',
        'salePrice',
        'stratum'
    ]
    
    def get_lists(self):
        """
        Method for getting the pagination list for the scrapper to do the requests
        """
        response = requests.request("POST", self.url_api, headers=self.headers, data=json.dumps(payload))
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

        # Start the loader
        item_keys = self.item_keys_number + self.item_keys_string
        for result in data:
            loader = ItemLoader(item=InmuebleItem())
            for key in item_keys:
                loader.add_value(key, result[key])
                # Default values for missing values
                if result[key] is None:
                    if key in self.item_keys_string:
                        loader.add_value(key, 'XD')
                    else:
                        loader.add_value(key, -1)
                           
            loader.add_value('lon', result['location']['lon'])
            loader.add_value('lat', result['location']['lat'])
            loader.add_value('propertyType', result['propertyType']['label'])

            yield loader.load_item()