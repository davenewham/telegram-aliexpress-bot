import unittest

from telegram_aliexpress_bot.aliexpress_api import AliExpressApi


class TestAliExpressApi(unittest.TestCase):
    def setUp(self):
        self.cut = AliExpressApi()

    def test_get_promotion_products(self):
        data = self.cut.get_promotion_products('something')
        self._verify_product_results(data)

    def test_get_promotion_product_detail(self):
        data = self.cut.get_promotion_product_detail(32719809585)
        self.assertTrue('https://' in data['result']['imageUrl'])
        self.assertTrue('https://' in data['result']['productUrl'])
        self.assertTrue(data['result']['productTitle'] != '')
        self.assertTrue(data['result']['salePrice'] != '')

    def test_get_hot_products(self):
        data = self.cut.get_hot_products(AliExpressApi.Category.Hardware)
        self._verify_product_results(data)

    def test_get_hot_products_without_category(self):
        data = self.cut.get_hot_products()
        self._verify_product_results(data)

    def _verify_product_results(self, data):
        self.assertTrue(data['result']['totalResults'] > 0)
        self.assertTrue('https://' in data['result']['products'][0]['imageUrl'])
        self.assertTrue('https://' in data['result']['products'][0]['productUrl'])
        self.assertTrue(data['result']['products'][0]['productTitle'] != '')
        self.assertTrue(data['result']['products'][0]['salePrice'] != '')

    def test_get_promotion_link(self):
        product_link = self.cut.get_hot_products()['result']['products'][0]['productUrl']
        link = self.cut.get_promotion_link(product_link)
        self.assertTrue('http://' in link)

    def test_get_short_promotion_link(self):
        # TODO: Mock Rebrandly API
        product_link = self.cut.get_hot_products()['result']['products'][0]['productUrl']
        link = self.cut.get_short_promotion_link(product_link)
        self.assertTrue('rebrand.ly/AliExpress_' in link)

    def test_get_product_id_from_link(self):
        product_id = self.cut.get_product_id_from_link('https://de.aliexpress.com/item/WWWOOR-Fashion-Luxury-brand-Watc'
                                                       'hes-men-Stainless-Steel-Mesh-strap-Quartz-watch-Ultra-Thin-Dial'
                                                       '-Clock/32719809585.html?aff_platform=product&cpt=1520787671494&'
                                                       'sk=3fEmAQz&aff_trace_key=f6618482534346b7bd9d6345c749ea51-15207'
                                                       '87671494-08292-3fEmAQz&terminal_id=f23f16b363201aa7ba3048638953'
                                                       '5c09')
        self.assertEqual('32719809585', product_id)

if __name__ == '__main__':
    unittest.main()
