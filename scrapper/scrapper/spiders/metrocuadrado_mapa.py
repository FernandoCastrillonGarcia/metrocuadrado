from scrapy.spiders import Spider
import scrapy
import json
from ..items import Inmueble

base_url = "https://www.metrocuadrado.com"

atributes_xpath = "//div[contains(@class,'card-line')]/div[contains(@class,'d-none')]"#//ul[contains(@class,'inline-list-grid')]//h2"
title_xpath = "//div[contains(@class,'d-none')]//h1/text()"


class MetroCuadrado2Spider(Spider):
    name = 'MetroCuadrado'

    start_urls = [base_url]
    allowed_domains = ['metrocuadrado.com']

    custom_settings = {
        'CONCURRENT_REQUESTS': 24, # HAGA 24 SCRIPTS AL TIEMPO
        'MEMORY_LIMIT_MG': 2048, # Limite de memoria RAM
        'MEMUSAGE_NOTIFY_MAIL': ['fernandocastrillon500@gmail.com'], # Notificación por correo
        'ROBOTSTXT_OBEY': True,
        'FEEDS': {
            './results/metrocuadrado.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
    }

    payload = json.dumps({
        "queries": [
            {
            "types": [
                "propertiesByFiltersQuery"
            ],
            "filter": {
                "propertyTypeId": {
                "values": [
                    "1",
                    "2"
                ]
                },
                "businessTypeId": {
                "values": [
                    "1",
                    "3"
                ]
                },
                "status": {
                "values": [
                    "Usado"
                ]
                },
                "priceRange": {
                "values": [
                    "469999999",
                    "470000001"
                ]
                },
                "neighborhoodId": {
                "values": [
                    "1"
                ]
                },
                "builtArea": {
                "values": [
                    "0",
                    "100000000000000000"
                ]
                },
                "roomsNumber": {
                "values": [
                    "2"
                ]
                },
                "bathroomsNumber": {
                "values": [
                    "2"
                ]
                },
                "parkingNumber": {
                "values": [
                    "2"
                ]
                },
                "stratum": {
                "values": [
                    "4"
                ]
                }
            }
            }
        ]
    })

    headers = {
        'authority': 'commons-api.metrocuadrado.com',
        'accept': '*/*',
        'accept-language': 'es-419,es;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://commons.metrocuadrado.com',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-api-key': '6JgwwXGxlC921DP4SB4ST6Jo6OO7rv3t4yXn5Y8y',
        'x-audit-client-id': ''
    }

    def parse(self, response):

        url = "https://commons-api.metrocuadrado.com/v1/api/commons/queries"

        yield scrapy.Request(url = url,
                             method = 'POST',
                             headers=self.headers,
                             body=self.payload,
                             callback = self.parse_api)
    
    def parse_api(self, response):
        raw_data = json.loads(response.body)
        data = raw_data['data']['result']['propertiesByFiltersQuery']['properties']
        for result in data:
            # link = base_url + result['url']
            # yield scrapy.Request(link,
            #                      callback = self.parse_link)
            
            yield {
                'coords': result['location'],
                'commentarios': result['comments']
            }
    
    def parse_link(self, response):
        values = response.xpath(atributes_xpath)#.getall()
        print('*'*60)
        print(values)
        title = response.xpath(title_xpath)
 

        # item = Inmueble()
        # item['title'] = title
        # item['covered_surface'] = values[0]
        # item['rooms'] = values[2]
        # item['bathrooms'] = values[3]
        # item['estrato'] = values[4]

        # yield item