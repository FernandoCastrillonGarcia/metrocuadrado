from scrapy.spiders import Spider
import scrapy
import json
from ..items import InmuebleItem
from itemloaders import ItemLoader
import os

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

    custom_settings = custom_settings

    payload_0 = json.dumps(payload)
    headers = headers

    item_keys =['adminPrice',
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

    def parse(self, response):

        url = "https://commons-api.metrocuadrado.com/v1/api/commons/queries"
        loader = ItemLoader(item=InmuebleItem())
        
        yield scrapy.Request(url = url,
                             method = 'POST',
                             headers=self.headers,
                             body=self.payload_0,
                             callback = self.parse_api)
        self.conteo +=1
        realEstate_pages = [33,66,99,132,165,198,231,264,297,330,363,396,429,462,495,528,561,594,627,660,693,726,759,792,825,858,891,924,957,990,1023,1056,1089,1122,1155,1188,1221,1254,1287,1320,1353,1386,1419,1452,1485,1518,1551,1584,1617,1650,1683,1716,1749,1782,1815,1848,1881,1914,1947,1980,2013,2046,2079,2112,2145,2178,2211,2244,2277,2310,2343,2376,2409,2442,2475,2508,2541,2574,2607,2640,2673,2706,2739,2772,2805,2838,2871,2904,2937,2970,3003,3036,3069,3102,3135,3168,3201,3234,3267,3300,3333,3366,3399,3432,3465,3498,3531,3564,3597,3630,3663,3696,3729,3762,3795,3828,3861,3894,3927,3960,3993,4026,4059,4092,4125,4158,4197,4247,4297,4347,4397,4447,4497,4547,4597,4647,4697,4747,4797,4847,4897,4947,4997,5047,5097,5147,5197,5247,5297,5347,5397,5447,5497,5547,5597,5647,5697,5747,5797,5847,5897,5947,5997,6047,6097,6147,6197,6247,6297,6347,6397,6447,6497,6547,6597,6647,6697,6747,6797,6847,6897,6947,6997,7047,7097,7147,7197,7247,7297,7347,7397,7447,7497,7547,7597,7647,7697,7747,7797]

        seller_pages = [17,34,51,68,85,102,119,136,153,170,187,204,221,238,255,272,289,306,323,340,357,374,391,408,425,442,459,476,493,510,527,544,561,578,595,612,629,646,663,680,697,714,731,748,765,782,799,816,833,850,867,884,901,918,935,952,969,986,1003,1020,1037,1054,1071,1088,1105,1122,1139,1156,1173,1190,1207,1224,1241,1258,1275,1292,1309,1326,1343,1360,1377,1394,1411,1428,1445,1462,1479,1496,1513,1530,1547,1564,1581,1598,1615,1632,1649,1666,1683,1700,1717,1734,1751,1768,1785,1802,1819,1836,1853,1870,1887,1904,1921,1938,1955,1972,1989,2006,2023,2040,2057,2074,2091,2108,2125,2142,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153,2153]
        for r, s in zip(realEstate_pages, seller_pages):
            batch = {
                "realEstate": {
                    "from": r
                },
                "seller": {
                    "from": s
                }
            }
            payload['queries'][0]['batch'] = batch
            payload_1 = json.dumps(payload)
            terminar = False
            if r == realEstate_pages[-1] and s == seller_pages[-1]:
                terminar = True
            yield scrapy.Request(url = url,
                                method = 'POST',
                                headers=self.headers,
                                body=payload_1,
                                callback = self.parse_api,
                                cb_kwargs={'loader': loader, 'terminar': terminar})
            self.conteo+=1

    def parse_api(self, response, **kwargs):
        terminar = kwargs['terminar']
        loader = kwargs['loader']
        raw_data = json.loads(response.body)
        data = raw_data['data']['result']['propertiesByFiltersQuery']['properties']

        for result in data:
            for key in self.item_keys:
                try:
                    loader.add_value(key, result[key])
                except:
                    loader.add_value(key, '')
        
        if terminar:
            item = loader.load_item()
            yield item
            print('TOTAL DE APIS PARSEADOS: ', self.conteo)
        else:
            pass