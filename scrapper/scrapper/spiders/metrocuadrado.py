from scrapy.spiders import Spider

from ..items import Inmueble
import scrapy
import os
import json

# URLS
base_url = "https://www.metrocuadrado.com"
next_url = "/apartamentos/venta/alrededores-de-bogota/"
urls_complete = base_url + next_url
apto_ejm = "/inmueble/venta-apartamento-bogota-gilmar-3-habitaciones-5-banos-2-garajes/5255-M3700985"

# Xpaths
#atributes_xpath = "//div[contains(@class, 'Card') and contains(@class, 'realstatedata')]/div/div/h3/text()"
links_xpath = "//div/ul[contains(@class, 'realestate')]//div[@class='card-header']/a/@data-gtm-productname"
atributes_xpath = "//div[contains(@class,'card-line')]/div[contains(@class,'d-none')]//ul[contains(@class,'inline-list-grid')]//h2"
title_xpath = "//div[contains(@class,'d-none')]//h1/text()"

class MetroCuadradoSpider(Spider):
    name = 'metrocuadrado'

    custom_settings = {
        'CONCURRENT_REQUESTS': 24, # HAGA 24 SCRIPTS AL TIEMPO
        'MEMORY_LIMIT_MG': 2048, # Limite de memoria RAM
        'MEMUSAGE_NOTIFY_MAIL': ['fernandocastrillon500@gmail.com'], # Notificación por correo
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'XDXDXDDXD',
        'FEEDS': {
            'results/metrocuadrado.json': {
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

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-419,es;q=0.9,en;q=0.8 ',
        'Cache-Control': 'no-cache',
        'Cookie': "mzona=; mbarrio=; disclaimerCookies=true; mubicacion=bogota; mtipoinmueble=apartamento; lastSearch=%2Fapartamentos%2Farriendo%2Fbogota%2F%3Fsearch%3Dsave%26seo%3D%2Fapartamentos%2Farriendo%2Fbogota%2F; mtiponegocio=arriendo; location=; mciudad=bogot%C3%A1%20d.c.; utag_main=v_id:018c8e378b210022afd14a5a87000506f001e06700bd0$_sn:5$_se:37$_ss:0$_st:1703211850923$dc_visit:4$ses_id:1703209343165%3Bexp-session$_pn:8%3Bexp-session$dc_event:6%3Bexp-session",
        'Pragma': 'no-cache',
        'Referer': 'https://www.metrocuadrado.com/apartamento/venta/bogota/?search=form',
        'Sec-Ch-Ua': "'Not_A Brand';v='8', 'Chromium';v='120', 'Google Chrome';v='120'",
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 ',
        'X-Api-Key': 'P1MfFHfQMOtL16Zpg36NcntJYCLFm8FqFfudnavl',
        'X-Requested-With': 'XMLHttpRequest'
    }

    start_urls = [base_url]
    allowed_domains = ['metrocuadrado.com']

    def parse(self, response):
        url = 'https://www.metrocuadrado.com/rest-search/search?realEstateBusinessList=arriendo&city=bogot%C3%A1&realEstateTypeList=apartamento&from=8900&size=1'

        yield scrapy.Request(url,
                                callback=self.parse_api,
                                headers=self.headers)
    
    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)["results"]
        for result in data:
            link = base_url + result['link']
            yield scrapy.Request(link,
                                callback=self.parse_link)
    
    def parse_link(self, response):
        values = response.xpath(f"{atributes_xpath}/text()").getall()
        title = response.xpath(title_xpath)

        item = Inmueble()
        item['title'] = title
        item['covered_surface'] = values[0]
        item['rooms'] = values[2]
        item['bathrooms'] = values[3]
        item['estrato'] = values[4]

        yield item
























