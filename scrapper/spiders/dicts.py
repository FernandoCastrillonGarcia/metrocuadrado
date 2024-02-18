CUSTOM_SETTINGS = {
    'CONCURRENT_REQUESTS': 24, # HAGA 24 SCRIPTS AL TIEMPO
    'MEMORY_LIMIT_MG': 2048,
    'ROBOTSTXT_OBEY': True,
    # 'FEEDS': {
    #     '../MapPage/assets/db/metrocuadrado.json': {
    #         'format': 'json',
    #         'encoding': 'utf8',
    #         'store_empty': True,
    #         'fields': None,
    #         'indent': 4,
    #         'overwrite': True,
    #         'item_export_kwargs': {
    #             'export_empty_fields': True,
    #         },
    #     },
    # },
}

PAYLOAD = {
    "queries": [
        {
        "types": [
            "propertiesByFiltersQuery"
        ],
        "filter": {
            "propertyTypeId": {
            "values": [
                "1",
                "2",
                "3",
                "8",
                "5",
                "6",
                "4",
                "7",
                "10",
                "9"
            ]
            },
            "businessTypeId": {
            "values": [
                "1",
                "2",
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
                "0",
                "100000000000000000"
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
            }
        },
          'batch': {
                "realEstate": {
                    "from": 0
                },
                "seller": {
                    "from": 0
                }
            }  
        }
    ]
}

HEADERS = {
    'authority': 'commons-api.metrocuadrado.com',
    'user-agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
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
