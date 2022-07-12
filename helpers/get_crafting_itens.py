import pandas as pd
import requests
from helpers.relation_item_bundles import bundle_size

API_URL = 'https://51clridw3h.execute-api.us-east-1.amazonaws.com/dev/market/get_item_by_name'

if __name__ == "__main__":
    df = pd.read_csv('../files/Crafting Itens.csv')

    all_crafting_itens = []
    crafting_item = {
        'name': '',
        'raw_itens': [],
        'raw_itens_prices': [],
        'value': 0,
        'cost': 0
    }
    for index, item in df.iterrows():
        item_name = item['Name']
        crafting_item['name'] = item_name

        for material in item['Materials'].split('\n'):
            material_name, quantity = material.split(' x')

            if material_name == 'Gold':
                crafting_item['raw_itens'].append(material_name)
                crafting_item['raw_itens_prices'].append(int(quantity))
                continue

            response = requests.post(API_URL, json={'name': material_name})

            if response:
                lowest_item_price = response.json()[-1]['lowest_price']
                crafting_item['raw_itens'].append(material_name)

                if material_name in bundle_size.keys():
                    price_per_unit = lowest_item_price / bundle_size[material_name]
                    crafting_item['raw_itens_prices'].append(price_per_unit)
                else:
                    crafting_item['raw_itens_prices'].append(lowest_item_price)







