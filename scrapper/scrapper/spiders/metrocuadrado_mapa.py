from scrapy.spiders import Spider
import scrapy
import json
from ..items import InmuebleItem
from itemloaders import ItemLoader
import os
import requests

with open('scrapper/dicts/payload.json', 'r') as json_file:
    payload = json.load(json_file)

with open('scrapper/dicts/custom_settings.json', 'r') as json_file:
    custom_settings = json.load(json_file)

with open('scrapper/dicts/headers.json', 'r') as json_file:
    headers = json.load(json_file)

base_url = "https://www.metrocuadrado.com"

class MetroCuadradoSpider(Spider):
    conteo = 0
    name = 'MetroCuadrado'

    start_urls = [base_url]
    allowed_domains = ['metrocuadrado.com']

    url_api = "https://commons-api.metrocuadrado.com/v1/api/commons/queries"

    custom_settings = custom_settings

    headers = headers

    payload = payload

    item_keys =['url',
                'adminPrice',
                'roomsNumber',
                'price',
                'checked',
                'id',
                'area',
                'forSale',
                'forRent',
                'status',
                'rentPrice',
                'salePrice',
                'metroId',
                'coments',
                'isPublished',
                'url',
                'stratum',
                'bathroomsNumber',
                'builtArea',
                'parkingNumber',
                'offerorType'
                ]
    
    def get_lists(self):
        response = requests.request("POST", self.url_api, headers=self.headers, data=json.dumps(payload))
        
        r_json = json.loads(response.text)
        batch = r_json['data']['result']['propertiesByFiltersQuery']['batch']
        return batch['realEstate']['pages'], batch['seller']['pages']

    def parse(self, response):

        loader = ItemLoader(item=InmuebleItem())

        realEstate_pages, seller_pages = self.get_lists()

        max_apis = max([len(realEstate_pages), len(seller_pages)])
        print(max_apis)

        for r, s in zip(realEstate_pages, seller_pages):
            batch = {
                "realEstate": {
                    "from": r
                },
                "seller": {
                    "from": s
                }
            }
            self.payload['queries'][0]['batch'] = batch
            payload = json.dumps(self.payload)

            yield scrapy.Request(url = self.url_api,
                                method = 'POST',
                                headers=self.headers,
                                body=payload,
                                callback = self.parse_api,
                                cb_kwargs={'loader': loader, 'max_apis': max_apis})
            
    inmuebles = 0
    def parse_api(self, response, **kwargs):
        
        loader = kwargs['loader']
        raw_data = json.loads(response.body)
        data = raw_data['data']['result']['propertiesByFiltersQuery']['properties']
        self.inmuebles += len(raw_data['data']['result']['propertiesByFiltersQuery']['properties']
        )
        for result in data:
            for key in self.item_keys:
                try:
                    loader.add_value(key, result[key])
                except:
                    loader.add_value(key, None)
        self.conteo+=1
        if self.conteo>=kwargs['max_apis']:
            item = loader.load_item()
            print(self.inmuebles)
            print(raw_data['data']['result']['propertiesByFiltersQuery']['total'])
            yield item
        else:
            pass