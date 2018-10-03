import json
import requests
import sys

from backports.configparser import ConfigParser
from enum import Enum

from telegram_aliexpress_bot.rebrandly_api import RebrandlyApi

class AliExpressApi(object):
    API_URL_BASE = 'http://gw.api.alibaba.com/openapi/param2/2/portals.open/'

    def __init__(self):
        self._read_config()

    def _read_config(self):
        """Reads the config file with the API keys which should be placed where aliexpress_api.py is"""
        import os
        file_path = os.path.join(os.path.dirname(__file__), './config.ini')
        config = ConfigParser()
        config.read(file_path)
        self._appkey = config.get('AliExpress', 'appkey')
        self._tracking_id = config.get('AliExpress', 'trackingId')

    @staticmethod #is this necesary?
    def _query_json_api(url, params):
        """Queries a JSON API"""
        response = requests.get(url=url, params=params)
        data = json.loads(response.text)
        return data

    def get_promotion_products(self, keyword=''):
        """Gets currently promoted products on AliExpress"""
        promotion_product_url = self.API_URL_BASE + 'api.listPromotionProduct/' + self._appkey
        params = dict(
            fields='productTitle,productUrl,imageUrl,30daysCommission,salePrice',
            keywords=keyword,
            sort='volumeDown'
        )
        return self._query_json_api(promotion_product_url, params)

    def get_promotion_product_detail(self, product_id):
        """Gets details for the product with the given product id"""
        promotion_product_detail_url = self.API_URL_BASE + 'api.getPromotionProductDetail/' + self._appkey
        params = dict(
            fields='productTitle,productUrl,imageUrl,30daysCommission,salePrice',
            productId=product_id
        )
        return self._query_json_api(promotion_product_detail_url, params)

    def get_promotion_product_detail_from_link(self, product_url):
        """Gets details for the product with the given product url"""
        product_id = self.get_product_id_from_link(product_url)
        product_details = self.get_promotion_product_detail(product_id)
        return product_details

    class Category(Enum):
        """Categories to be used with  get_hot_products()"""
        All = '',
        Apparel = '3',
        Automobiles = '34',
        Beauty = '66',
        Computer = '7',
        Home = '13',
        Electronics = '	44',
        ElectricalEquipment = '5',
        Food = '2',
        Furniture = '1503',
        Hair = '200003655',
        Hardware = '42',
        Garden = '15',
        Appliances = '6',
        Industry = '200001996',
        Jewelry = '36',
        Lights = '39',
        Luggage = '1524',
        Mother = '1501',
        Office = '21',
        Phones = '509',
        Security = '30',
        Shoes = '322',
        Sports = '18',
        Tools = '1420',
        Toys = '26',
        Travel = '200003498',
        Watches = '1511',
        Weddings = '320'

    def get_hot_products(self, category=Category.All):
        """Gets currently hot products on AliExpress"""
        hot_product_url = self.API_URL_BASE + 'api.listHotProducts/' + self._appkey
        params = dict(
            categoryId=category.value
        )
        return self._query_json_api(hot_product_url, params)

    def get_promotion_link(self, product_link):
        """Transforms a regular link into a promotion / referral link"""
        promotion_link_url = self.API_URL_BASE + 'api.getPromotionLinks/' + self._appkey

        params = dict(
            trackingId=self._tracking_id,
            urls=product_link,
        )
        result = self._query_json_api(promotion_link_url, params)['result']
        return result['promotionUrls'][0]['promotionUrl']

    def get_short_promotion_link(self, product_link):
        """Gets a shortened promotion link"""
        link = self.get_promotion_link(product_link)
        shortener = RebrandlyApi()
        return shortener.get_short_url(link, 'AliExpress_')

    @staticmethod
    def get_product_id_from_link(link):
        """Returns the product id from a regular AliExpress link"""
        import re
        match = re.search(r'.*\.aliexpress\.com/item/.*/(\d*)\.html.*', link)
        return match.group(1)
