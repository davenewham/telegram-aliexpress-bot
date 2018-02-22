import unittest

from AliExpressApi import AliExpressApi


class AliExpressApiTest(unittest.TestCase):
    def setUp(self):
        self.cut = AliExpressApi()

    def test_get_promotion_products(self):
        data = self.cut.get_promotion_products("something")
        self._verify_results(data)

    def test_get_hot_products(self):
        data = self.cut.get_hot_products(AliExpressApi.Category.Hardware)
        self._verify_results(data)

    def test_get_hot_products_without_category(self):
        data = self.cut.get_hot_products()
        self._verify_results(data)

    def _verify_results(self, data):
        self.assertTrue(data["result"]["totalResults"] > 0)
        self.assertTrue("https://" in data["result"]["products"][0]["imageUrl"])
        self.assertTrue("https://" in data["result"]["products"][0]["productUrl"])
        self.assertTrue(data["result"]["products"][0]["productTitle"] != "")
        self.assertTrue(data["result"]["products"][0]["salePrice"] != "")


if __name__ == '__main__':
    unittest.main()
